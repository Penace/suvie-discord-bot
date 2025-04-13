import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

from utils.storage import (
    load_movies, save_movies, get_movie_by_title,
    get_movies_by_status, update_watchlist_channel
)
from utils.imdb import fetch_movie_data

class WatchlistGroup(commands.GroupCog, name="watchlist"):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    # === /watchlist add ===
    @app_commands.command(name="add", description="Add a movie or TV show to your watchlist.")
    @app_commands.describe(
        title="The title of the movie or TV show to add.",
        imdb_id="The IMDb ID (optional).",
        filepath="Path to the file (optional).",
        genre="Genre or tags (optional).",
        year="Release year (optional).",
        season="Season number (TV only, optional).",
        episode="Episode number (TV only, optional)."
    )
    async def add(
        self,
        interaction: discord.Interaction,
        title: str,
        imdb_id: Optional[str] = None,
        filepath: Optional[str] = None,
        genre: Optional[str] = None,
        year: Optional[str] = None,
        season: Optional[int] = None,
        episode: Optional[int] = None
    ):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()

        if any((m.get("title") or "").lower() == title.lower() for m in movies):
            await interaction.followup.send("❌ This title is already in your library.", ephemeral=True)
            return

        try:
            movie_data = fetch_movie_data(
                imdb_id=imdb_id or "",
                title=title
            )
            media_type = (movie_data.get("Type") or "movie").lower()
            if season or episode:
                media_type = "series"

            movie_data["type"] = media_type
            movie_data["status"] = "watchlist"

            if media_type == "series":
                movie_data["season"] = str(season or 1)
                movie_data["episode"] = str(episode or 1)

        except Exception as e:
            await interaction.followup.send(f"❌ Failed to fetch data: {str(e)}", ephemeral=True)
            return

        if filepath: movie_data["filepath"] = filepath
        if genre: movie_data["genre"] = genre
        if year: movie_data["year"] = year

        movies.append(movie_data)
        save_movies(movies)
        await update_watchlist_channel(interaction.client)

        title_text = f"{movie_data['title']} (Season {movie_data.get('season')})" if media_type == "series" else movie_data["title"]
        embed = discord.Embed(
            title=f"🎬 Added to Watchlist: {title_text}",
            color=discord.Color.teal()
        )
        if movie_data.get("genre"):
            embed.add_field(name="Genre", value=movie_data["genre"], inline=True)
        if movie_data.get("year"):
            embed.add_field(name="Year", value=movie_data["year"], inline=True)
        if filepath:
            embed.add_field(name="File", value=filepath, inline=False)
        if movie_data.get("imdb_url"):
            embed.add_field(name="IMDb", value=movie_data["imdb_url"], inline=False)
        if movie_data.get("poster") and movie_data["poster"] != "N/A":
            embed.set_thumbnail(url=movie_data["poster"])

        await interaction.followup.send(embed=embed, ephemeral=True)

    # === /watchlist remove ===
    @app_commands.command(name="remove", description="Remove a movie or show from your watchlist.")
    @app_commands.describe(title="The title to remove.")
    async def remove(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()
        filtered = [m for m in movies if (m.get("title") or "").lower() != title.lower()]

        if len(filtered) == len(movies):
            await interaction.followup.send("❌ That title wasn't found in your watchlist.", ephemeral=True)
            return

        save_movies(filtered)
        await update_watchlist_channel(self.bot)
        await interaction.followup.send(f"🗑️ Removed **{title}** from your watchlist.", ephemeral=True)

    # === /watchlist view ===
    @app_commands.command(name="view", description="View your watchlist.")
    async def view(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()
        watchlist = get_movies_by_status(movies, "watchlist")

        if not watchlist:
            await interaction.followup.send("📭 Your watchlist is empty.", ephemeral=True)
            return

        for m in watchlist:
            title = f"{m['title']} (Season {m.get('season')})" if m.get("type") == "series" else f"{m['title']} ({m.get('year', 'N/A')})"
            embed = discord.Embed(
                title=f"🎬 {title}",
                description=m.get("plot", "No description available."),
                color=discord.Color.teal()
            )
            embed.add_field(name="Genre", value=m.get("genre", "N/A"), inline=True)
            embed.add_field(name="Rating", value=m.get("imdb_rating", "N/A"), inline=True)
            embed.add_field(name="Director", value=m.get("director", "N/A"), inline=False)
            embed.add_field(name="Stars", value=m.get("actors", "N/A"), inline=False)
            if m.get("filepath"):
                embed.add_field(name="File Path", value=m["filepath"], inline=False)
            if m.get("imdb_url"):
                embed.add_field(name="IMDb", value=m["imdb_url"], inline=False)
            if m.get("poster") and m["poster"] != "N/A":
                embed.set_thumbnail(url=m["poster"])
            await interaction.followup.send(embed=embed, ephemeral=True)

    # === /watchlist clear ===
    @app_commands.command(name="clear", description="Clear all movies or shows from your watchlist.")
    async def clear(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()
        filtered = [m for m in movies if m.get("status") != "watchlist"]

        if len(filtered) == len(movies):
            await interaction.followup.send("❌ Your watchlist is already empty.", ephemeral=True)
            return

        save_movies(filtered)
        await update_watchlist_channel(self.bot)
        await interaction.followup.send("✅ Cleared your watchlist.", ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(WatchlistGroup(bot))
    print("📁 Watchlist command loaded.")