import json, os, discord, shutil
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile
from typing import Union, Optional

DATA_DIR = "bot/data"
BACKUP_DIR = Path("backups/json")

# === File Handling Utilities ===
def get_data_path(guild_id: int, file_name: str) -> str:
    guild_dir = Path(DATA_DIR) / str(guild_id)
    guild_dir.mkdir(parents=True, exist_ok=True)
    return str(guild_dir / file_name)

def load_json(guild_id: int, file_name: str) -> list:
    path = get_data_path(guild_id, file_name)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_json(guild_id: int, file_name: str, data: list):
    path = get_data_path(guild_id, file_name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

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

    category = discord.utils.get(guild.categories, name="🎮 suvie")
    if not category:
        category = await guild.create_category("🎮 suvie")

    try:
        return await guild.create_text_channel(name=name, category=category)
    except Exception as e:
        print(f"❌ Failed to create channel {name}: {e}")
        return None

# === Channel Updates ===
async def update_channel(bot: discord.Client, guild_id: int, channel_name: str, status: str, title_prefix="", color=discord.Color.teal):
    path = get_data_path(guild_id, "movies.json")
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as f:
        try:
            movies = json.load(f)
        except json.JSONDecodeError:
            return

    guild = bot.get_guild(guild_id)
    if not guild:
        print("⚠️ Guild not found.")
        return

    channel = await get_or_create_text_channel(bot, guild, channel_name)
    if not channel:
        print("⚠️ Channel could not be created.")
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
    for guild in bot.guilds:
        await update_channel(bot, guild.id, "watchlist", "watchlist", color=discord.Color.teal())

async def update_currently_watching_channel(bot: discord.Client):
    for guild in bot.guilds:
        await update_channel(bot, guild.id, "currently-watching", "currently-watching", "🎬 Currently Watching: ", color=discord.Color.orange())

async def update_downloaded_channel(bot: discord.Client):
    for guild in bot.guilds:
        await update_channel(bot, guild.id, "downloaded", "downloaded", color=discord.Color.green())

async def update_watched_channel(bot: discord.Client):
    for guild in bot.guilds:
        await update_channel(bot, guild.id, "watched", "watched", color=discord.Color.purple())

# === Backup ===
def create_backup_zip(guild_id: int) -> Path:
    src = Path(get_data_path(guild_id, "movies.json"))
    zip_path = Path(f"backups/{guild_id}_backup.zip")
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(zip_path, "w") as zipf:
        if src.exists():
            zipf.write(src, arcname="movies.json")

    return zip_path

def load_movies() -> list:
    return load_json(0, "movies.json")  # Default to guild_id = 0 for legacy

def save_movies(movies: list):
    save_json(0, "movies.json", movies)  # Same here