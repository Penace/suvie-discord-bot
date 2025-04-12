import discord
from discord import app_commands
from discord.ext import commands
from utils.storage import (
    load_movies,
    save_movies,
    get_downloaded_movie,
    update_downloaded_channel
)

class DownloadedCog(commands.GroupCog, name="downloaded"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="add", description="Add a downloaded movie by its IMDb title or ID.")
    @app_commands.describe(
        title="The title of the downloaded movie.",
        imdb_id="The IMDb ID (optional).",
        filepath="Path to the downloaded file (optional)."
    )
    async def add_downloaded(
        self,
        interaction: discord.Interaction,
        title: str,
        imdb_id: str = None,
        filepath: str = None
    ):
        movies = load_movies()

        match = next((m for m in movies if m["title"].lower() == title.lower() or m.get("imdb_id") == imdb_id), None)
        if not match:
            await interaction.response.send_message("❌ Movie not found in the main list.", ephemeral=True)
            return

        match["filepath"] = filepath if filepath else "N/A"
        match["status"] = "downloaded"

        save_movies(movies)
        await update_downloaded_channel(interaction.client, movies)

        await interaction.response.send_message(f"✅ Marked **{match['title']}** as downloaded!", ephemeral=True)

    @app_commands.command(name="edit", description="Edit the file path of a downloaded movie.")
    @app_commands.describe(
        title="The title of the movie you want to update.",
        filepath="The new file path to assign."
    )
    async def edit_filepath(
        self,
        interaction: discord.Interaction,
        title: str,
        filepath: str
    ):
        movies = load_movies()
        movie = get_downloaded_movie(movies, title)

        if not movie:
            await interaction.response.send_message("❌ Movie not found in downloaded list.", ephemeral=True)
            return

        movie["filepath"] = filepath
        save_movies(movies)
        await update_downloaded_channel(interaction.client, movies)

        await interaction.response.send_message(f"✏️ Updated filepath for **{movie['title']}**.", ephemeral=True)

    @app_commands.command(name="remove", description="Remove a movie from the downloaded list.")
    @app_commands.describe(title="The title of the movie to remove from downloaded list.")
    async def remove_downloaded(self, interaction: discord.Interaction, title: str):
        movies = load_movies()
        movie = get_downloaded_movie(movies, title)

        if not movie:
            await interaction.response.send_message("❌ Movie not found in downloaded list.", ephemeral=True)
            return

        movie.pop("filepath", None)
        movie["status"] = "watchlist"
        save_movies(movies)
        await update_downloaded_channel(interaction.client, movies)

        await interaction.response.send_message(f"🗑️ Removed **{movie['title']}** from downloaded.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(DownloadedCog(bot))