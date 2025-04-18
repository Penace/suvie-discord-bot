import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from bot.models.movie import Movie
from bot.utils.database import engine
from bot.utils.storage import update_downloaded_channel

class DownloadedCog(commands.GroupCog, name="downloaded"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="add", description="Mark a movie or show as downloaded.")
    @app_commands.describe(
        title="The title of the movie or show.",
        imdb_id="The IMDb ID (optional).",
        filepath="Path to the downloaded file (optional)."
    )
    async def add(
        self,
        interaction: discord.Interaction,
        title: str,
        imdb_id: Optional[str] = None,
        filepath: Optional[str] = None
    ):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id
        print(f"📥 /downloaded add: {title}")

        try:
            with Session(engine) as session:
                match = session.query(Movie).filter(
                    Movie.guild_id == guild_id,
                    (func.lower(Movie.title) == title.lower()) |
                    (Movie.imdb_id == imdb_id)
                ).first()

                if not match:
                    await interaction.followup.send("❌ Title not found in your library.", ephemeral=True)
                    return

                match.downloaded = True
                match.filepath = filepath or match.filepath or None

                title_display = match.title
                suffix = f" (S{match.season:02}E{match.episode:02})" if match.type == "series" and match.season and match.episode else ""
                file = match.filepath
                imdb = match.imdb_url
                poster = match.poster

                session.commit()
                print("✅ Movie marked as downloaded.")

            await update_downloaded_channel(self.bot, guild_id)

            embed = discord.Embed(
                title=f"📥 Marked as Downloaded: {title_display}{suffix}",
                color=discord.Color.gold()
            )
            if file:
                embed.add_field(name="File", value=file, inline=False)
            if imdb:
                embed.add_field(name="IMDb", value=imdb, inline=False)
            if poster and poster != "N/A":
                embed.set_thumbnail(url=poster)

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"❌ Error in /downloaded add: {type(e).__name__}: {e}")
            await interaction.followup.send("❌ Failed to mark as downloaded.", ephemeral=True)

    @app_commands.command(name="edit", description="Edit the file path of a downloaded movie.")
    async def edit(self, interaction: discord.Interaction, title: str, filepath: str):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id
        print(f"✏️ /downloaded edit: {title} → {filepath}")

        try:
            with Session(engine) as session:
                movie = session.query(Movie).filter(
                    Movie.guild_id == guild_id,
                    func.lower(Movie.title) == title.lower(),
                    Movie.downloaded.is_(True)
                ).first()

                if not movie:
                    await interaction.followup.send("❌ Movie not found in downloaded list.", ephemeral=True)
                    return

                movie.filepath = filepath
                session.commit()

            await update_downloaded_channel(self.bot, guild_id)

            embed = discord.Embed(
                title=f"✏️ Filepath Updated: {movie.title}",
                color=discord.Color.gold()
            )
            embed.add_field(name="New File Path", value=filepath, inline=False)
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"❌ Error in /downloaded edit: {type(e).__name__}: {e}")
            await interaction.followup.send("❌ Failed to update file path.", ephemeral=True)

    @app_commands.command(name="remove", description="Remove a movie from downloaded list.")
    async def remove(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id
        print(f"🗑️ /downloaded remove: {title}")

        try:
            with Session(engine) as session:
                movie = session.query(Movie).filter(
                    Movie.guild_id == guild_id,
                    func.lower(Movie.title) == title.lower(),
                    Movie.downloaded.is_(True)
                ).first()

                if not movie:
                    await interaction.followup.send("❌ Movie not found in downloaded list.", ephemeral=True)
                    return

                movie.downloaded = False
                movie.filepath = None
                session.commit()

            await update_downloaded_channel(self.bot, guild_id)

            embed = discord.Embed(
                title=f"🗑️ Removed from Downloaded: {movie.title}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"❌ Error in /downloaded remove: {type(e).__name__}: {e}")
            await interaction.followup.send("❌ Failed to remove from downloaded.", ephemeral=True)

    @app_commands.command(name="view", description="View all downloaded movies or shows.")
    async def view(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id
        print(f"👀 /downloaded view")

        try:
            with Session(engine) as session:
                movies = session.query(Movie).filter(
                    Movie.guild_id == guild_id,
                    Movie.downloaded.is_(True)
                ).all()

            if not movies:
                await interaction.followup.send("📭 No downloaded content found.", ephemeral=True)
                return

            for movie in movies:
                suffix = f" (S{movie.season:02}E{movie.episode:02})" if movie.type == "series" and movie.season and movie.episode else ""
                embed = discord.Embed(
                    title=f"📥 {movie.title}{suffix}",
                    color=discord.Color.gold()
                )
                if movie.filepath:
                    embed.add_field(name="File", value=movie.filepath, inline=False)
                if movie.imdb_url:
                    embed.add_field(name="IMDb", value=movie.imdb_url, inline=False)
                if movie.poster and movie.poster != "N/A":
                    embed.set_thumbnail(url=movie.poster)
                await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"❌ Error in /downloaded view: {type(e).__name__}: {e}")
            await interaction.followup.send("❌ Failed to fetch downloaded list.", ephemeral=True)


    @app_commands.command(name="clear", description="Clear all downloaded items from the list.")
    async def clear(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id
        print("🧹 /downloaded clear triggered")

        try:
            with Session(engine) as session:
                count = session.query(Movie).filter(
                    Movie.guild_id == guild_id,
                    Movie.downloaded.is_(True)
                ).update({Movie.downloaded: False})
                session.commit()
                print(f"🧹 Cleared {count} downloaded entries")

            await update_downloaded_channel(self.bot, guild_id)

            if count:
                await interaction.followup.send("✅ Downloaded list cleared.", ephemeral=True)
            else:
                await interaction.followup.send("📭 No downloaded content to clear.", ephemeral=True)

        except Exception as e:
            print(f"❌ Error in /downloaded clear: {type(e).__name__}: {e}")
            await interaction.followup.send("❌ Failed to clear downloaded list.", ephemeral=True)


# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(DownloadedCog(bot))
    print("📥 Downloaded command loaded.")
