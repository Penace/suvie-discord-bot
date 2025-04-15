import sys
import os
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from sqlalchemy.orm import Session

from bot.models.movie import Movie
from bot.utils.database import engine
from bot.utils.storage import (
    get_movie_by_title,
    get_currently_watching_movies,
    update_currently_watching_channel,
    create_embed
)

class CurrentlyWatchingCog(commands.GroupCog, name="currentlywatching"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="set", description="Set the currently watching title (movie or TV).")
    async def set(
        self,
        interaction: discord.Interaction,
        title: str,
        imdb_id: Optional[str] = None,
        season: Optional[int] = None,
        episode: Optional[int] = None,
        timestamp: Optional[str] = None,
        filepath: Optional[str] = None
    ):
        await interaction.response.defer(ephemeral=True)
        print(f"✨ /currentlywatching set: {title}")

        guild_id = interaction.guild_id
        if guild_id is None:
            await interaction.followup.send("❌ This command must be used in a server.", ephemeral=True)
            return

        try:
            movie = get_movie_by_title(guild_id, title)
            if not movie:
                await interaction.followup.send("❌ Title not found in your library.", ephemeral=True)
                return

            movie.status = "currently-watching"
            movie.type = movie.type or "series"
            if movie.type == "series":
                movie.season = season or movie.season or 1
                movie.episode = episode or movie.episode or 1
            if timestamp:
                movie.timestamp = timestamp
            if filepath:
                movie.filepath = filepath

            with Session(engine) as session:
                session.merge(movie)
                session.commit()

            await update_currently_watching_channel(self.bot, guild_id)

            suffix = f" (S{int(movie.season):02}E{int(movie.episode):02})" if movie.type == "series" else ""
            await interaction.followup.send(f"🎬 Set **{movie.title}{suffix}** as currently watching.", ephemeral=True)

        except Exception as e:
            print(f"❌ Error in set: {e}")
            await interaction.followup.send(f"⚠️ Failed to set currently watching title. Error: {e}", ephemeral=True)

    @app_commands.command(name="update", description="Update a currently watching movie or show.")
    async def update(
        self,
        interaction: discord.Interaction,
        title: str,
        season: Optional[int] = None,
        episode: Optional[int] = None,
        timestamp: Optional[str] = None,
        filepath: Optional[str] = None
    ):
        await interaction.response.defer(ephemeral=True)
        print(f"🛠️ /currentlywatching update: {title}")

        guild_id = interaction.guild_id
        if guild_id is None:
            await interaction.followup.send("❌ This command must be used in a server.", ephemeral=True)
            return

        try:
            movie = get_movie_by_title(guild_id, title)
            if not movie:
                await interaction.followup.send("❌ Entry not found in your library.", ephemeral=True)
                return

            if movie.type == "series":
                if season:
                    movie.season = season
                if episode:
                    movie.episode = episode
            if timestamp:
                movie.timestamp = timestamp
            if filepath:
                movie.filepath = filepath

            movie.status = "currently-watching"

            with Session(engine) as session:
                session.merge(movie)
                session.commit()

            await update_currently_watching_channel(self.bot, guild_id)

            suffix = f" (S{int(movie.season):02}E{int(movie.episode):02})" if movie.type == "series" else ""
            await interaction.followup.send(f"🔁 Updated **{movie.title}{suffix}**.", ephemeral=True)

        except Exception as e:
            print(f"❌ Error in update: {e}")
            await interaction.followup.send(f"⚠️ Failed to update entry. Error: {e}", ephemeral=True)

    @app_commands.command(name="remove", description="Remove a title from your currently watching list.")
    async def remove(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(ephemeral=True)
        print(f"🗑️ /currentlywatching remove: {title}")

        guild_id = interaction.guild_id
        if guild_id is None:
            await interaction.followup.send("❌ This command must be used in a server.", ephemeral=True)
            return

        try:
            movie = get_movie_by_title(guild_id, title)
            if not movie or movie.status != "currently-watching":
                await interaction.followup.send("❌ Title not found in your currently watching list.", ephemeral=True)
                return

            movie.status = "watchlist"

            with Session(engine) as session:
                session.merge(movie)
                session.commit()

            await update_currently_watching_channel(self.bot, guild_id)
            await interaction.followup.send(f"🗑️ Removed **{movie.title}** from currently watching.", ephemeral=True)

        except Exception as e:
            print(f"❌ Error in remove: {e}")
            await interaction.followup.send(f"⚠️ Failed to remove from currently watching. Error: {e}", ephemeral=True)

    @app_commands.command(name="view", description="View all currently watching movies or shows.")
    async def view(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        print("👀 /currentlywatching view triggered")

        guild_id = interaction.guild_id
        if guild_id is None:
            await interaction.followup.send("❌ This command must be used in a server.", ephemeral=True)
            return

        try:
            currently_watching = get_currently_watching_movies(guild_id)
            if not currently_watching:
                await interaction.followup.send("📭 You're not currently watching anything.", ephemeral=True)
                return

            for movie in currently_watching:
                embed = create_embed(movie, color=discord.Color.orange())
                await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"❌ Error in view: {e}")
            await interaction.followup.send(f"⚠️ Failed to fetch currently watching list. Error: {e}", ephemeral=True)

    @app_commands.command(name="next", description="Advance to the next episode of a show.")
    async def next(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(ephemeral=True)
        print(f"⏭️ /currentlywatching next: {title}")

        guild_id = interaction.guild_id
        if guild_id is None:
            await interaction.followup.send("❌ This command must be used in a server.", ephemeral=True)
            return

        try:
            movie = get_movie_by_title(guild_id, title)
            if not movie:
                await interaction.followup.send("❌ Show not found.", ephemeral=True)
                return

            if movie.type != "series":
                await interaction.followup.send("❌ This command only works on TV shows.", ephemeral=True)
                return

            movie.episode = (movie.episode or 1) + 1
            movie.status = "currently-watching"

            with Session(engine) as session:
                session.merge(movie)
                session.commit()

            await update_currently_watching_channel(self.bot, guild_id)
            await interaction.followup.send(f"⏭️ Now watching **{movie.title} S{int(movie.season):02}E{int(movie.episode):02}**", ephemeral=True)

        except Exception as e:
            print(f"❌ Error in next: {e}")
            await interaction.followup.send(f"⚠️ Failed to advance episode. Error: {e}", ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(CurrentlyWatchingCog(bot))
    print("📺 Loaded cog: currentlywatching")