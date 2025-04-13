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

    category = discord.utils.get(guild.categories, name="