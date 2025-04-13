import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from typing import Optional

from utils.storage import (
    load_movies,
    save_movies,
    get_movie_by_title,
    update_watched_channel
)

class WatchedCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="watched", description="Mark a movie or TV show as watched.")
    @app_commands.describe(
        title="The title of the movie or show you've finished watching.",
        timestamp="Optional: Timestamp when you stopped watching (e.g. 01:23:45)",
        filepath="Optional: File path or location of the file"
    )
    async def watched(
        self,
        interaction: discord.Interaction,
        title: str,
        timestamp: Optional[str] = None,
        filepath: Optional[str] = None
    ):
        await interaction.response.defer(ephemeral=True)

        movies = load_movies()
        movie = get_movie_by_title(movies, title)

        if not movie:
            await interaction.followup.send("❌ Movie not found in your library.", ephemeral=True)
            return

        # Update status
        movie["status"] = "watched"
        movie["timestamp"] = timestamp or datetime.now().strftime("%H:%M:%S")
        if filepath:
            movie["filepath"] = filepath

        save_movies(movies)
        await update_watched_channel(self.bot)

        # Confirmation Embed
        embed = discord.Embed(
            title=f"✅ Marked as Watched: {movie['title']}",
            color=discord.Color.from_rgb(255, 105, 180)
        )
        embed.add_field(name="Watched At", value=movie["timestamp"], inline=True)
        if movie.get("year"):
            embed.add_field(name="Year", value=movie["year"], inline=True)
        if movie.get("genre"):
            embed.add_field(name="Genre", value=movie["genre"], inline=True)
        if filepath:
            embed.add_field(name="File Path", value=filepath or "N/A", inline=False)
        if movie.get("imdb_url"):
            embed.add_field(name="IMDb", value=movie["imdb_url"], inline=False)
        if movie.get("poster") and movie["poster"] != "N/A":
            embed.set_thumbnail(url=movie["poster"])

        await interaction.followup.send(embed=embed, ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(WatchedCog(bot))
    print("📁 Watched command loaded.")