import json, os, discord, shutil
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile
from typing import Union

MOVIES_FILE = "movies.json"
BACKUP_DIR = Path("backups/json")

# === Load & Save ===

def load_movies():
    if not os.path.exists(MOVIES_FILE):
        return []
    try:
        with open(MOVIES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_movies(movies: list):
    with open(MOVIES_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, indent=4, ensure_ascii=False)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy(MOVIES_FILE, BACKUP_DIR / f"movies_{timestamp}.json")
    limit_json_backups(BACKUP_DIR, max_versions=5)

def limit_json_backups(directory: Union[str, Path] = "backups/json", max_versions: int = 5):
    path = Path(directory)
    files = sorted(path.glob("movies_*.json"), key=os.path.getmtime, reverse=True)
    for f in files[max_versions:]:
        f.unlink()

# === Filters ===

def get_movie_by_title(movies, title: str):
    return next((m for m in movies if m["title"].lower() == title.lower()), None)

def get_movies_by_status(movies, status: str):
    return [m for m in movies if m.get("status") == status]

def get_currently_watching_movies(movies):
    return get_movies_by_status(movies, "currently-watching")

# === Embeds ===

def create_embed(movie, title_prefix="", color=discord.Color.teal):
    title = movie["title"]
    if movie.get("type") == "series":
        season = movie.get("season", 1)
        episode = movie.get("episode", 1)
        title = f"{title} (S{season:02}E{episode:02})"

    embed = discord.Embed(
        title=f"{title_prefix}{title}",
        color=color
    )
    if movie.get("poster") and movie["poster"] != "N/A":
        embed.set_thumbnail(url=movie["poster"])

    for key in ["genre", "year", "filepath", "timestamp", "imdb_url"]:
        value = movie.get(key)
        if value:
            name = key.capitalize() if key != "imdb_url" else "IMDb"
            embed.add_field(name=name, value=value, inline=(key != "filepath"))

    return embed

# === Channel Updates ===

async def update_channel(bot: discord.Client, channel_name: str, status: str, title_prefix="", color=discord.Color.teal):
    movies = load_movies()
    channel = discord.utils.get(bot.get_all_channels(), name=channel_name)

    if not channel or not isinstance(channel, discord.TextChannel):
        return

    await channel.purge(limit=10)
    filtered = get_movies_by_status(movies, status)

    if not filtered:
        await channel.send("📭 Nothing to show here.")
        return

    for movie in filtered:
        embed = create_embed(movie, title_prefix, color)
        await channel.send(embed=embed)

async def update_watchlist_channel(bot: discord.Client):
    await update_channel(bot, "watchlist", "watchlist", color=discord.Color.teal())

async def update_currently_watching_channel(bot: discord.Client):
    await update_channel(bot, "currently-watching", "currently-watching", "🎬 Currently Watching: ", color=discord.Color.orange())

async def update_downloaded_channel(bot: discord.Client):
    await update_channel(bot, "downloaded", "downloaded", color=discord.Color.green())

async def update_watched_channel(bot: discord.Client):
    await update_channel(bot, "watched", "watched", color=discord.Color.purple())

# === Backup ===

def create_backup_zip():
    zip_path = Path("backups/backup.zip")
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path, "w") as zipf:
        if os.path.exists(MOVIES_FILE):
            zipf.write(MOVIES_FILE)
    return zip_path