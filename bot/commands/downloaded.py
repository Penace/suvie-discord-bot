import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

from utils.storage import (
    load_movies,
    save_movies,
    update_downloaded_channel,
    get_movie_by_title
)

class DownloadedCog(commands.GroupCog, name="downloaded"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # === /downloaded add ===
    @app_commands.command(name="add", description="Mark a movie or show as downloaded.")
    @app_commands.describe(
        title="The title of the movie or show.",
        imdb_id="The IMDb ID (optional).",
        filepath="Path to the downloaded file (optional)."
    )
    async def add_downloaded(
        self,
        interaction: discord.Interaction,
        title: str,
        imdb_id: Optional[str] = None,
        filepath: Optional[str] = None
    ):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()

        match = next(
            (m for m in movies if m["title"].lower() == title.lower() or (imdb_id and m.get("imdb_id") == imdb_id)),
            None
        )

        if not match:
            await interaction.followup.send("❌ Title not found in your library.", ephemeral=True)
            return

        match["filepath"] = filepath or match.get("filepath", "N/A")
        match["status"] = "downloaded"

        save_movies(movies)
        await update_downloaded_channel(self.bot)

        suffix = f" (S{match['season']:02}E{match['episode']:02})" if match.get("type") == "series" else ""
        embed = discord.Embed(
            title=f"📥 Marked as Downloaded: {match['title']}{suffix}",
            color=discord.Color.gold()
        )
        if match.get("filepath"):
            embed.add_field(name="File", value=match["filepath"], inline=False)
        if match.get("imdb_url"):
            embed.add_field(name="IMDb", value=match["imdb_url"], inline=False)
        if match.get("poster") and match["poster"] != "N/A":
            embed.set_thumbnail(url=match["poster"])

        await interaction.followup.send(embed=embed, ephemeral=True)

    # === /downloaded edit ===
    @app_commands.command(name="edit", description="Edit the file path of a downloaded movie.")
    @app_commands.describe(
        title="The title of the movie to update.",
        filepath="The new file path to assign."
    )
    async def edit_filepath(self, interaction: discord.Interaction, title: str, filepath: str):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()
        movie = get_movie_by_title(movies, title)

        if not movie or movie.get("status") != "downloaded":
            await interaction.followup.send("❌ Movie not found in downloaded list.", ephemeral=True)
            return

        movie["filepath"] = filepath
        save_movies(movies)
        await update_downloaded_channel(self.bot)

        embed = discord.Embed(
            title=f"✏️ Filepath Updated: {movie['title']}",
            color=discord.Color.gold()
        )
        embed.add_field(name="New File Path", value=filepath, inline=False)
        await interaction.followup.send(embed=embed, ephemeral=True)

    # === /downloaded remove ===
    @app_commands.command(name="remove", description="Remove a movie from downloaded list.")
    @app_commands.describe(title="The title of the movie to remove from downloaded.")
    async def remove_downloaded(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()
        movie = get_movie_by_title(movies, title)

        if not movie or movie.get("status") != "downloaded":
            await interaction.followup.send("❌ Movie not found in downloaded list.", ephemeral=True)
            return

        movie["status"] = "watchlist"
        movie.pop("filepath", None)
        save_movies(movies)
        await update_downloaded_channel(self.bot)

        embed = discord.Embed(
            title=f"🗑️ Removed from Downloaded: {movie['title']}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(DownloadedCog(bot))
    print("📁 Downloaded command loaded.")