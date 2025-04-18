import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from bot.models.movie import Movie
from bot.utils.database import engine
from bot.utils.storage import (
    get_movies_by_status,
    update_watched_channel
)
from bot.utils.ui import generate_movie_embed

class WatchedCog(commands.GroupCog, name="watched"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # === /watched add ===
    @app_commands.command(name="add", description="Mark a movie or TV show as watched (from any list).")
    @app_commands.describe(
        title="The title of the movie or show you've finished watching.",
        timestamp="Timestamp (e.g. 01:23:45 or will auto-generate)",
        season="Season number (for series)",
        episode="Episode number (for series)",
        filepath="Optional file path"
    )
    async def add(
        self,
        interaction: discord.Interaction,
        title: str,
        timestamp: Optional[str] = None,
        season: Optional[int] = None,
        episode: Optional[int] = None,
        filepath: Optional[str] = None
    ):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id
        print(f"🎞️ /watched add: {title}")

        try:
            with Session(engine) as session:
                movie = session.query(Movie).filter(
                    Movie.guild_id == guild_id,
                    Movie.title.ilike(title)
                ).first()

                if not movie:
                    await interaction.followup.send("❌ Movie not found in your library.", ephemeral=True)
                    return

                movie.status = "watched"
                movie.timestamp = timestamp or datetime.now().strftime("%H:%M:%S %d/%m/%Y")
                if filepath:
                    movie.filepath = filepath
                if movie.type == "series":
                    if season:
                        movie.season = season
                    if episode:
                        movie.episode = episode

                # === Cache values before session closes ===
                title_display = f"{movie.title} (S{int(movie.season):02}E{int(movie.episode):02})" if movie.type == "series" else movie.title
                watched_at = movie.timestamp
                year = movie.year
                genre = movie.genre
                file_path = movie.filepath
                imdb = movie.imdb_url
                poster = movie.poster

                session.commit()
                print("✅ Movie marked as watched.")

            embed = discord.Embed(title=f"✅ Archived: {title_display}", color=discord.Color.from_rgb(255, 105, 180))
            embed.add_field(name="Watched At", value=watched_at, inline=True)
            if year: embed.add_field(name="Year", value=year, inline=True)
            if genre: embed.add_field(name="Genre", value=genre, inline=True)
            if file_path: embed.add_field(name="File Path", value=file_path, inline=False)
            if imdb: embed.add_field(name="IMDb", value=imdb, inline=False)
            if poster and poster != "N/A": embed.set_thumbnail(url=poster)

            await update_watched_channel(self.bot, guild_id)
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"❌ Error in /watched add: {type(e).__name__}: {e}")
            await interaction.followup.send("❌ Failed to mark as watched.", ephemeral=True)

    # === /watched view ===
    @app_commands.command(name="view", description="View your watched archive.")
    async def view(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id

        try:
            movies = get_movies_by_status(guild_id, "watched")
            if not movies:
                await interaction.followup.send("📭 No watched entries found.", ephemeral=True)
                return

            for movie in movies:
                embed = generate_movie_embed(movie, title_prefix="🎞️ Watched: ")
                await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"❌ Error in /watched view: {type(e).__name__}: {e}")
            await interaction.followup.send("❌ Failed to fetch watched entries.", ephemeral=True)

    # === /watched edit ===
    @app_commands.command(name="edit", description="Edit a watched entry’s details.")
    @app_commands.describe(
        title="The watched title to update",
        timestamp="New timestamp",
        season="New season number (TV only)",
        episode="New episode number (TV only)",
        filepath="New file path"
    )
    async def edit(
        self,
        interaction: discord.Interaction,
        title: str,
        timestamp: Optional[str] = None,
        season: Optional[int] = None,
        episode: Optional[int] = None,
        filepath: Optional[str] = None
    ):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id
        print(f"✏️ /watched edit: {title}")

        try:
            with Session(engine) as session:
                movie = session.query(Movie).filter(
                    Movie.guild_id == guild_id,
                    func.lower(Movie.title) == title.lower(),
                    Movie.status == "watched"
                ).first()

                if not movie:
                    await interaction.followup.send("❌ Watched title not found.", ephemeral=True)
                    return

                if timestamp:
                    movie.timestamp = timestamp
                if filepath:
                    movie.filepath = filepath
                if movie.type == "series":
                    if season: movie.season = season
                    if episode: movie.episode = episode

                session.commit()
                print("✏️ Watched entry updated.")

            await update_watched_channel(self.bot, guild_id)
            await interaction.followup.send(f"✏️ Updated **{movie.title}**.", ephemeral=True)

        except Exception as e:
            print(f"❌ Error in /watched edit: {type(e).__name__}: {e}")
            await interaction.followup.send("❌ Failed to update watched entry.", ephemeral=True)

    # === /watched remove ===
    @app_commands.command(name="remove", description="Remove a watched item (reverts to watchlist).")
    async def remove(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id
        print(f"🗑️ /watched remove: {title}")

        try:
            with Session(engine) as session:
                movie = session.query(Movie).filter(
                    Movie.guild_id == guild_id,
                    func.lower(Movie.title) == title.lower(),
                    Movie.status == "watched"
                ).first()

                if not movie:
                    await interaction.followup.send("❌ Title not found in watched list.", ephemeral=True)
                    return

                movie.status = "watchlist"
                movie.timestamp = None
                session.commit()
                print("🗑️ Reverted to watchlist.")

            await update_watched_channel(self.bot, guild_id)

            embed = discord.Embed(
                title=f"🗑️ Removed from Watched: {movie.title}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"❌ Error in /watched remove: {type(e).__name__}: {e}")
            await interaction.followup.send("❌ Failed to remove watched item.", ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(WatchedCog(bot))
    print("🎞️ Watched command group loaded.")