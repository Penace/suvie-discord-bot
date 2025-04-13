import os
import json
import discord
import shutil
from pathlib import Path
from zipfile import ZipFile
from datetime import datetime
from typing import Union, Optional

# === Constants ===
DATA_DIR = Path("bot/data")
BACKUP_DIR = Path("backups/json")
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# === Core File Utilities ===

def get_data_path(guild_id: int, file_name: str) -> Path:
    guild_dir = DATA_DIR / str(guild_id)
    guild_dir.mkdir(parents=True, exist_ok=True)
    return guild_dir / file_name

def load_json(guild_id: int, file_name: str) -> list:
    path = get_data_path(guild_id, file_name)
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_json(guild_id: int, file_name: str, data: list):
    path = get_data_path(guild_id, file_name)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# === Movies I/O ===

def load_movies(guild_id: int) -> list:
    return load_json(guild_id, "movies.json")

def save_movies(guild_id: int, movies: list):
    save_json(guild_id, "movies.json", movies)
    # Backup for safety
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"movies_{guild_id}_{timestamp}.json"
    shutil.copy(get_data_path(guild_id, "movies.json"), backup_file)
    limit_json_backups(BACKUP_DIR, prefix=f"movies_{guild_id}_", max_versions=5)

def limit_json_backups(directory: Union[str, Path], prefix: str, max_versions: int = 5):
    path = Path(directory)
    files = sorted(path.glob(f"{prefix}*.json"), key=os.path.getmtime, reverse=True)
    for f in files[max_versions:]:
        f.unlink()

# === Filters ===

def get_movie_by_title(movies: list, title: str) -> Optional[dict]:
    return next((m for m in movies if m.get("title", "").lower() == title.lower()), None)

def get_movies_by_status(movies: list, status: str) -> list:
    return [m for m in movies if m.get("status") == status]

def get_currently_watching_movies(movies: list) -> list:
    return get_movies_by_status(movies, "currently-watching")

# === Embeds ===

def create_embed(movie: dict, title_prefix: str = "", color=discord.Color.teal()) -> discord.Embed:
    title = movie["title"]
    if movie.get("type") == "series":
        season = movie.get("season", 1)
        episode = movie.get("episode", 1)
        title = f"{title} (S{int(season):02}E{int(episode):02})"

    embed = discord.Embed(title=f"{title_prefix}{title}", color=color)

    if movie.get("poster") and movie["poster"] != "N/A":
        embed.set_thumbnail(url=movie["poster"])

    for key in ["genre", "year", "filepath", "timestamp", "imdb_url"]:
        value = movie.get(key)
        if value:
            name = key.capitalize() if key != "imdb_url" else "IMDb"
            embed.add_field(name=name, value=value, inline=(key != "filepath"))

    return embed

# === Channel Management ===

async def get_or_create_text_channel(bot: discord.Client, guild: discord.Guild, name: str) -> Optional[discord.TextChannel]:
    existing = discord.utils.get(guild.text_channels, name=name)
    if existing:
        return existing

    category = discord.utils.get(guild.categories, name="🎬 suvie")
    if not category:
        category = await guild.create_category("🎬 suvie")

    try:
        return await guild.create_text_channel(name=name, category=category)
    except Exception as e:
        print(f"❌ Failed to create channel '{name}': {e}")
        return None

# === Channel Update Logic ===

async def update_channel(bot: discord.Client, guild_id: int, channel_name: str, status: str, title_prefix: str = "", color=discord.Color.teal()):
    movies = load_movies(guild_id)
    guild = bot.get_guild(guild_id)
    if not guild:
        print(f"⚠️ Guild not found: {guild_id}")
        return

    channel = await get_or_create_text_channel(bot, guild, channel_name)
    if not channel:
        return

    await channel.purge(limit=10)
    filtered = get_movies_by_status(movies, status)

    if not filtered:
        await channel.send("📭 Nothing to show here.")
        return

    for movie in filtered:
        embed = create_embed(movie, title_prefix, color)
        await channel.send(embed=embed)

# === Public Channel Updaters ===

async def update_watchlist_channel(bot: discord.Client, guild_id: int):
    await update_channel(bot, guild_id, "watchlist", "watchlist", color=discord.Color.teal())

async def update_currently_watching_channel(bot: discord.Client, guild_id: int):
    await update_channel(bot, guild_id, "currently-watching", "currently-watching", "🎬 Currently Watching: ", color=discord.Color.orange())

async def update_downloaded_channel(bot: discord.Client, guild_id: int):
    await update_channel(bot, guild_id, "downloaded", "downloaded", color=discord.Color.green())

async def update_watched_channel(bot: discord.Client, guild_id: int):
    await update_channel(bot, guild_id, "watched", "watched", color=discord.Color.purple())

# === Backup Command ===

def create_backup_zip() -> Path:
    zip_path = Path("backups/backup.zip")
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path, "w") as zipf:
        for guild_dir in DATA_DIR.iterdir():
            if guild_dir.is_dir():
                for f in guild_dir.glob("*.json"):
                    zipf.write(f, arcname=f"{guild_dir.name}/{f.name}")
    return zip_path