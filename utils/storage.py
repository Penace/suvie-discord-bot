import json, os, discord, shutil, glob
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile

MOVIES_FILE = "movies.json"

# === Load & Save ===

def load_movies():
    if not os.path.exists(MOVIES_FILE):
        return []
    with open(MOVIES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_movies(movies: list):
    with open(MOVIES_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, indent=4, ensure_ascii=False)
    backup_dir = Path("backups/json")
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy(MOVIES_FILE, backup_dir / f"movies_{timestamp}.json")
    limit_json_backups(backup_dir, max_versions=5)

def limit_json_backups(directory="backups/json", max_versions=5):
    path = Path(directory)
    files = sorted(path.glob("movies_*.json"), key=os.path.getmtime, reverse=True)
    for f in files[max_versions:]:
        f.unlink()

# === General Filters ===

def get_movie_by_title(movies, title: str):
    return next((m for m in movies if m["title"].lower() == title.lower()), None)

def get_movies_by_status(movies, status: str):
    return [m for m in movies if m.get("status") == status]

def get_currently_watching_movies(movies):
    return [m for m in movies if m.get("status") == "currently-watching"]

# === Channel Update ===

async def update_watchlist_channel(bot: discord.Client, movies=None):
    if not movies:
        movies = load_movies()
    channel = discord.utils.get(bot.get_all_channels(), name="watchlist")
    if not channel or not isinstance(channel, discord.TextChannel):
        return
    await channel.purge(limit=10)
    watchlist = get_movies_by_status(movies, "watchlist")

    for m in watchlist:
        title = f"{m['title']} (S{m['season']:02}E{m['episode']:02})" if m.get("type") == "series" else m["title"]
        embed = discord.Embed(title=title, color=discord.Color.teal())
        if m.get("poster") and m["poster"] != "N/A":
            embed.set_thumbnail(url=m["poster"])
        if m.get("genre"): embed.add_field(name="Genre", value=m["genre"], inline=True)
        if m.get("year"): embed.add_field(name="Year", value=m["year"], inline=True)
        if m.get("filepath"): embed.add_field(name="File", value=m["filepath"], inline=False)
        if m.get("imdb_url"): embed.add_field(name="IMDb", value=m["imdb_url"], inline=False)
        await channel.send(embed=embed)

async def update_currently_watching_channel(bot: discord.Client):
    movies = load_movies()
    currently_watching = get_currently_watching_movies(movies)
    channel = discord.utils.get(bot.get_all_channels(), name="currently-watching")
    if not channel or not isinstance(channel, discord.TextChannel):
        return
    await channel.purge(limit=10)

    if not currently_watching:
        await channel.send("📭 Not watching anything right now.")
        return

    for show in currently_watching:
        season = show.get("season")
        episode = show.get("episode")

        if season is not None and episode is not None:
            title = f"{show['title']} (S{int(season):02}E{int(episode):02})"
        else:
            title = show["title"]

        embed = discord.Embed(title=f"🎬 Currently Watching: {title}", color=discord.Color.orange())
        if show.get("timestamp"):
            embed.add_field(name="Timestamp", value=show["timestamp"], inline=True)
        if show.get("filepath"):
            embed.add_field(name="File", value=show["filepath"], inline=False)
        if show.get("imdb_url"):
            embed.add_field(name="IMDb", value=show["imdb_url"], inline=False)
        if show.get("poster") and show["poster"] != "N/A":
            embed.set_thumbnail(url=show["poster"])
        await channel.send(embed=embed)
        
def create_backup_zip():
    zip_path = Path("backups/backup.zip")
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path, "w") as zipf:
        if os.path.exists(MOVIES_FILE):
            zipf.write(MOVIES_FILE)
    return zip_path

async def update_downloaded_channel(bot: discord.Client):
    movies = load_movies()
    downloaded = get_movies_by_status(movies, "downloaded")
    channel = discord.utils.get(bot.get_all_channels(), name="downloaded")
    if not channel or not isinstance(channel, discord.TextChannel):
        return
    await channel.purge(limit=10)
    for m in downloaded:
        embed = discord.Embed(title=m["title"], color=discord.Color.green())
        if m.get("filepath"): embed.add_field(name="File", value=m["filepath"], inline=False)
        if m.get("imdb_url"): embed.add_field(name="IMDb", value=m["imdb_url"], inline=False)
        if m.get("poster") and m["poster"] != "N/A": embed.set_thumbnail(url=m["poster"])
        await channel.send(embed=embed)
    
async def update_watched_channel(bot: discord.Client):
    movies = load_movies()
    watched = get_movies_by_status(movies, "watched")
    channel = discord.utils.get(bot.get_all_channels(), name="watched")
    if not channel or not isinstance(channel, discord.TextChannel):
        return
    await channel.purge(limit=10)
    for m in watched:
        embed = discord.Embed(title=m["title"], color=discord.Color.purple())
        if m.get("filepath"): embed.add_field(name="File", value=m["filepath"], inline=False)
        if m.get("imdb_url"): embed.add_field(name="IMDb", value=m["imdb_url"], inline=False)
        if m.get("poster") and m["poster"] != "N/A": embed.set_thumbnail(url=m["poster"])
        await channel.send(embed=embed)
    
