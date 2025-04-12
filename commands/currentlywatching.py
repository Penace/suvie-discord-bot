import discord
from discord.ext import commands
from discord import app_commands

from utils.storage import (
    load_movies,
    save_movies,
    update_currently_watching,
    get_currently_watching_movie,
    update_currently_watching_channel
)

class CurrentlyWatchingCog(commands.GroupCog, name="currentlywatching"):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(name="set", description="Set the currently watching movie.")
    @app_commands.describe(
        title="The title of the movie to mark as currently watching.",
        imdb_id="The IMDb ID of the movie (optional).",
        timestamp="Where you left off in the movie (e.g. 01:12:43).",
        filepath="Optional path to the movie file."
    )
    async def set(
        self,
        interaction: discord.Interaction,
        title: str = None,
        imdb_id: str = None,
        timestamp: str = None,
        filepath: str = None
    ):
        movies = load_movies()

        matched = None
        if title:
            matched = next((m for m in movies if m["title"].lower() == title.lower()), None)
        elif imdb_id:
            matched = next((m for m in movies if m.get("imdb_id") == imdb_id), None)

        if not matched:
            await interaction.response.send_message("❌ Movie not found in your library.", ephemeral=True)
            return

        update_currently_watching(movies, matched["imdb_id"])

        # Save timestamp and filepath (only if this is the currently watching movie)
        matched["timestamp"] = timestamp if timestamp else None
        matched["filepath"] = filepath if filepath else matched.get("filepath", None)

        save_movies(movies)
        await update_currently_watching_channel(self.bot, movies)

        await interaction.response.send_message(
            f"🎬 Now watching: **{matched['title']} ({matched.get('year', 'N/A')})**",
            ephemeral=True
        )

    @app_commands.command(name="view", description="View the currently watching movie.")
    async def view(self, interaction: discord.Interaction):
        movies = load_movies()
        movie = get_currently_watching_movie(movies)

        if not movie:
            await interaction.response.send_message("📭 Nothing is currently being watched.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"{movie['title']} ({movie.get('year', 'N/A')})",
            color=discord.Color.green()
        )
        embed.add_field(name="Genre", value=movie.get("genre", "N/A"), inline=True)
        embed.add_field(name="IMDb", value=movie.get("imdb_url", "N/A"), inline=False)

        if movie.get("timestamp"):
            embed.add_field(name="⏱️ Timestamp", value=movie["timestamp"], inline=True)
        if movie.get("filepath"):
            embed.add_field(name="🗂️ File Path", value=movie["filepath"], inline=False)
        if movie.get("poster") and movie["poster"] != "N/A":
            embed.set_thumbnail(url=movie["poster"])

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(CurrentlyWatchingCog(bot))