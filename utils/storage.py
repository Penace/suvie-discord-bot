import json
import os
import discord

MOVIES_FILE = "movies.json"

def load_movies() -> list:
    """Safely loads movies from the JSON file."""
    if not os.path.exists(MOVIES_FILE):
        return []
    with open(MOVIES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_movies(movies: list):
    """Saves movies to the JSON file."""
    with open(MOVIES_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, indent=4, ensure_ascii=False)

# === Movie Helpers ===

def get_movie_by_title(movies: list, title: str) -> dict:
    return next((m for m in movies if m["title"].lower() == title.lower()), None)

def get_movies_by_status(movies: list, status: str) -> list:
    return [m for m in movies if m.get("status") == status]

def get_downloaded_movie(movies: list, title: str) -> dict:
    movie = get_movie_by_title(movies, title)
    return movie if movie and movie.get("status") == "downloaded" else None

def get_watchlist_movie(movies: list, title: str) -> dict:
    movie = get_movie_by_title(movies, title)
    return movie if movie and movie.get("status") == "watchlist" else None

def get_currently_watching_movie(movies: list) -> dict:
    return next((m for m in movies if m.get("status") == "currently-watching"), None)

# === Channel Updaters ===

async def update_watchlist_channel(bot, movies: list):
    channel = discord.utils.get(bot.get_all_channels(), name="watchlist")
    if not channel:
        return

    watchlist = get_movies_by_status(movies, "watchlist")
    await channel.purge()

    if not watchlist:
        return

    embed = discord.Embed(
        title="🎬 Watchlist",
        color=discord.Color.blue(),
        description="\n".join(f"• **{m['title']}** ({m.get('year', 'N/A')})" for m in watchlist)
    )
    await channel.send(embed=embed)

async def update_downloaded_channel(bot, movies: list):
    channel = discord.utils.get(bot.get_all_channels(), name="downloaded")
    if not channel:
        return

    downloaded = get_movies_by_status(movies, "downloaded")
    await channel.purge()

    if not downloaded:
        return

    embed = discord.Embed(
        title="📥 Downloaded Movies",
        color=discord.Color.gold(),
        description="\n".join(f"• **{m['title']}** — `{m.get('filepath', 'N/A')}`" for m in downloaded)
    )
    await channel.send(embed=embed)

async def update_currently_watching_channel(bot, movies: list):
    channel = discord.utils.get(bot.get_all_channels(), name="currently-watching")
    if not channel:
        return

    currently = get_currently_watching_movie(movies)
    await channel.purge()

    if not currently:
        return

    embed = discord.Embed(
        title=f"🎞️ Currently Watching: {currently['title']}",
        color=discord.Color.green()
    )
    if currently.get("year"):
        embed.add_field(name="Year", value=currently["year"], inline=True)
    if currently.get("genre"):
        embed.add_field(name="Genre", value=currently["genre"], inline=True)
    if currently.get("filepath"):
        embed.add_field(name="File Path", value=currently["filepath"], inline=False)
    if currently.get("poster") and currently["poster"] != "N/A":
        embed.set_thumbnail(url=currently["poster"])

    await channel.send(embed=embed)
    
def update_currently_watching(movies: list, imdb_id: str):
    """Sets the movie with the given IMDb ID as currently watching, clears all others."""
    for m in movies:
        if m.get("status") == "currently-watching":
            m["status"] = "watchlist"  # or None if you want to remove status
        if m.get("imdb_id") == imdb_id:
            m["status"] = "currently-watching"