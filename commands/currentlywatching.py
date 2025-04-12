import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

from utils.storage import (
    load_movies,
    save_movies,
    update_currently_watching,
    get_currently_watching_movie,
    update_currently_watching_channel,
    get_movie_by_title
)

class CurrentlyWatchingCog(commands.GroupCog, name="currentlywatching"):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    # === /currentlywatching set ===
    @app_commands.command(name="set", description="Set the currently watching movie.")
    @app_commands.describe(
        title="The title of the movie you're watching.",
        imdb_id="The IMDb ID (optional).",
        timestamp="Timestamp in the movie (e.g. 01:12:43).",
        filepath="Optional path to the movie file."
    )
    async def set(self, interaction: discord.Interaction, title: str = None, imdb_id: str = None, timestamp: str = None, filepath: str = None):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()

        matched = None
        if title:
            matched = next((m for m in movies if m.get("title", "").lower() == title.lower()), None)
        elif imdb_id:
            matched = next((m for m in movies if m.get("imdb_id") == imdb_id), None)

        if not matched:
            await interaction.followup.send("❌ Movie not found in your library.", ephemeral=True)
            return

        update_currently_watching(movies, matched.get("imdb_id"))

        matched["timestamp"] = timestamp or datetime.now().strftime("%H:%M:%S")
        if filepath:
            matched["filepath"] = filepath

        save_movies(movies)
        await update_currently_watching_channel(self.bot, movies)

        embed = discord.Embed(
            title=f"🎬 Now Watching: {matched['title']}",
            color=discord.Color.green()
        )
        embed.add_field(name="Year", value=matched.get("year", "N/A"), inline=True)
        embed.add_field(name="Genre", value=matched.get("genre", "N/A"), inline=True)
        embed.add_field(name="IMDb", value=matched.get("imdb_url", "N/A"), inline=False)
        embed.add_field(name="Timestamp", value=matched["timestamp"], inline=True)
        if matched.get("filepath"):
            embed.add_field(name="File Path", value=matched["filepath"], inline=False)
        if matched.get("poster") and matched["poster"] != "N/A":
            embed.set_thumbnail(url=matched["poster"])

        await interaction.followup.send(embed=embed, ephemeral=True)

    # === /currentlywatching view ===
    @app_commands.command(name="view", description="View the currently watching movie.")
    async def view(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()
        movie = get_currently_watching_movie(movies)

        if not movie:
            await interaction.followup.send("📭 Nothing is currently being watched.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"🎬 Currently Watching: {movie['title']}",
            color=discord.Color.green()
        )
        embed.add_field(name="Year", value=movie.get("year", "N/A"), inline=True)
        embed.add_field(name="Genre", value=movie.get("genre", "N/A"), inline=True)
        embed.add_field(name="IMDb", value=movie.get("imdb_url", "N/A"), inline=False)
        if movie.get("timestamp"):
            embed.add_field(name="Timestamp", value=movie["timestamp"], inline=True)
        if movie.get("filepath"):
            embed.add_field(name="File Path", value=movie["filepath"], inline=False)
        if movie.get("poster") and movie["poster"] != "N/A":
            embed.set_thumbnail(url=movie["poster"])

        await interaction.followup.send(embed=embed, ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(CurrentlyWatchingCog(bot))
    print("📁 Currently Watching command loaded.")