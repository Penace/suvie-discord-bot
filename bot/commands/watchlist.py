import sys
import os
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from sqlalchemy.orm import Session

# === Fix import path for local + prod ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
print(f"🔍 PYTHONPATH: {sys.path[-1]}")

# === Local Imports ===
from bot.models.movie import Movie
from bot.utils.database import engine
from bot.utils.storage import (
    get_movie_by_title,
    get_movies_by_status,
    update_watchlist_channel,
    create_embed
)
from bot.utils.imdb import fetch_movie_data


class WatchlistGroup(commands.GroupCog, name="watchlist"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="add", description="Add a movie or show to your watchlist.")
    # async def add(
    #     self,
    #     interaction: discord.Interaction,
    #     title: str,
    #     imdb_id: Optional[str] = None,
    #     filepath: Optional[str] = None,
    #     genre: Optional[str] = None,
    #     year: Optional[str] = None,
    #     season: Optional[int] = None,
    #     episode: Optional[int] = None
    # ):
    #     print("🚀 /watchlist add triggered")
    #     await interaction.response.defer(ephemeral=True)
    #     guild_id = interaction.guild_id or 0

    #     if get_movie_by_title(guild_id, title):
    #         await interaction.followup.send("❌ This title is already in your library.", ephemeral=True)
    #         return

    #     try:
    #         movie_data = fetch_movie_data(imdb_id=imdb_id or "", title=title)
    #         print("📦 OMDb data fetched")
    #     except Exception as e:
    #         print(f"❌ OMDb fetch failed: {e}")
    #         await interaction.followup.send(f"❌ Failed to fetch movie data: {e}", ephemeral=True)
    #         return

    #     media_type = "series" if season or episode else (movie_data.get("type") or "movie").lower()

    #     new_movie = Movie(
    #         guild_id=guild_id,
    #         title=movie_data["title"],
    #         year=year or movie_data.get("year"),
    #         genre=genre or movie_data.get("genre"),
    #         plot=movie_data.get("plot"),
    #         poster=movie_data.get("poster"),
    #         imdb_url=movie_data.get("imdb_url"),
    #         imdb_id=movie_data.get("imdb_id"),
    #         imdb_rating=movie_data.get("imdb_rating"),
    #         director=movie_data.get("director"),
    #         actors=movie_data.get("actors"),
    #         type=media_type,
    #         season=season if media_type == "series" else None,
    #         episode=episode if media_type == "series" else None,
    #         filepath=filepath,
    #         status="watchlist"
    #     )

    #     with Session(engine) as session:
    #         session.add(new_movie)
    #         session.commit()
    #         print("💾 Movie saved to DB")

    #     await update_watchlist_channel(self.bot, guild_id)
    #     print("📡 Channel updated")

    #     # === Confirmation Embed ===
    #     title_display = f"{new_movie.title} (S{new_movie.season})" if media_type == "series" else new_movie.title
    #     embed = discord.Embed(title=f"🎬 Added to Watchlist: {title_display}", color=discord.Color.teal())
    #     if new_movie.genre:
    #         embed.add_field(name="Genre", value=new_movie.genre, inline=True)
    #     if new_movie.year:
    #         embed.add_field(name="Year", value=new_movie.year, inline=True)
    #     if new_movie.filepath:
    #         embed.add_field(name="File", value=new_movie.filepath, inline=False)
    #     if new_movie.imdb_url:
    #         embed.add_field(name="IMDb", value=new_movie.imdb_url, inline=False)
    #     if new_movie.poster and new_movie.poster != "N/A":
    #         embed.set_thumbnail(url=new_movie.poster)

    #     await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="add", description="Add a movie or show to your watchlist.")
    async def add(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(ephemeral=True)
        print("✅ /watchlist add triggered with title:", title)
        await interaction.followup.send(f"Title received: **{title}**", ephemeral=True)
    @app_commands.command(name="remove", description="Remove a movie or show from your watchlist.")
    async def remove(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id or 0

        with Session(engine) as session:
            movie = session.query(Movie).filter_by(guild_id=guild_id, title=title, status="watchlist").first()
            if not movie:
                await interaction.followup.send("❌ Title not found in your watchlist.", ephemeral=True)
                return
            session.delete(movie)
            session.commit()
            print(f"🗑️ Deleted '{title}' from watchlist")

        await update_watchlist_channel(self.bot, guild_id)
        await interaction.followup.send(f"🗑️ Removed **{title}** from your watchlist.", ephemeral=True)

    @app_commands.command(name="view", description="View your current watchlist.")
    async def view(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id or 0
        watchlist = get_movies_by_status(guild_id, "watchlist")

        if not watchlist:
            await interaction.followup.send("📭 Your watchlist is empty.", ephemeral=True)
            return

        for movie in watchlist:
            embed = create_embed(movie, color=discord.Color.teal())
            await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="clear", description="Clear your watchlist completely.")
    async def clear(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id or 0

        with Session(engine) as session:
            deleted = session.query(Movie).filter_by(guild_id=guild_id, status="watchlist").delete()
            session.commit()
            print(f"🧹 Cleared {deleted} watchlist entries")

        if not deleted:
            await interaction.followup.send("❌ Your watchlist is already empty.", ephemeral=True)
        else:
            await update_watchlist_channel(self.bot, guild_id)
            await interaction.followup.send("✅ Watchlist cleared.", ephemeral=True)


# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(WatchlistGroup(bot))
    print("📁 Watchlist command loaded.")