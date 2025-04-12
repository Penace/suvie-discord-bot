import discord
from discord.ext import commands
from discord import app_commands

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
    @app_commands.command(name="add", description="Add a movie to your watchlist.")
    @app_commands.describe(
        title="The title of the movie to add.",
        imdb_id="The IMDb ID of the movie (optional).",
        filepath="Optional path to the movie file.",
        genre="The genre or tags for the movie (optional).",
        year="The year of the movie (optional)."
    )
    async def add(self, interaction: discord.Interaction, title: str, imdb_id: str = None, filepath: str = None, genre: str = None, year: str = None):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()

        if any(m.get("title", "").lower() == title.lower() for m in movies):
            await interaction.followup.send("❌ This movie is already in your library.", ephemeral=True)
            return

        try:
            movie_data = fetch_movie_data(imdb_id=imdb_id, title=title)
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to fetch movie data: {str(e)}", ephemeral=True)
            return

        movie_data["status"] = "watchlist"
        movie_data["filepath"] = filepath or None
        movie_data["genre"] = genre or movie_data.get("genre")
        movie_data["year"] = year or movie_data.get("year")

        movies.append(movie_data)
        save_movies(movies)
        await update_watchlist_channel(self.bot, movies)

        embed = discord.Embed(
            title=f"✅ {movie_data['title']} added to Watchlist",
            description=movie_data.get("plot", "No description available."),
            color=discord.Color.teal()
        )
        embed.add_field(name="Genre", value=movie_data.get("genre", "N/A"), inline=True)
        embed.add_field(name="Year", value=movie_data.get("year", "N/A"), inline=True)
        embed.add_field(name="Rating", value=movie_data.get("imdb_rating", "N/A"), inline=True)
        embed.add_field(name="Director", value=movie_data.get("director", "N/A"), inline=False)
        embed.add_field(name="Stars", value=movie_data.get("actors", "N/A"), inline=False)
        embed.add_field(name="IMDb", value=movie_data.get("imdb_url", "N/A"), inline=False)
        if filepath:
            embed.add_field(name="File Path", value=filepath, inline=False)
        if movie_data.get("poster") and movie_data["poster"] != "N/A":
            embed.set_thumbnail(url=movie_data["poster"])

        await interaction.followup.send(embed=embed, ephemeral=True)

    # === /watchlist remove ===
    @app_commands.command(name="remove", description="Remove a movie from your watchlist.")
    @app_commands.describe(title="The title of the movie to remove.")
    async def remove(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()
        filtered = [m for m in movies if m.get("title", "").lower() != title.lower()]

        if len(filtered) == len(movies):
            await interaction.followup.send("❌ That movie wasn't found in your watchlist.", ephemeral=True)
            return

        save_movies(filtered)
        await update_watchlist_channel(self.bot, filtered)
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
            embed = discord.Embed(
                title=f"🎬 {m['title']} ({m.get('year', 'N/A')})",
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
    @app_commands.command(name="clear", description="Clear all movies from your watchlist.")
    async def clear(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()
        filtered = [m for m in movies if m.get("status") != "watchlist"]

        if len(filtered) == len(movies):
            await interaction.followup.send("❌ Your watchlist is already empty.", ephemeral=True)
            return

        save_movies(filtered)
        await update_watchlist_channel(self.bot, filtered)
        await interaction.followup.send("✅ Cleared your watchlist.", ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(WatchlistGroup(bot))
    print("📁 Watchlist command loaded.")