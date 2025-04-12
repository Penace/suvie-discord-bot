import json
import os
import discord
import shutil
import glob
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile

MOVIES_FILE = "movies.json"

# === Load & Save ===

def load_movies() -> list:
    """Load movies from the JSON file, or return empty list if missing or invalid."""
    if not os.path.exists(MOVIES_FILE):
        return []
    try:
        with open(MOVIES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_movies(movies: list):
    """Save movies to the JSON file and maintain 5 latest backups."""
    with open(MOVIES_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, indent=4, ensure_ascii=False)

    backup_dir = Path("backups/json")
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"movies_{timestamp}.json"
    shutil.copy(MOVIES_FILE, backup_path)

    limit_json_backups(backup_dir, max_versions=5)

def limit_json_backups(directory="backups/json", max_versions=5):
    """Keep only the last N JSON backups."""
    path = Path(directory)
    files = sorted(path.glob("movies_*.json"), key=os.path.getmtime, reverse=True)
    for old_file in files[max_versions:]:
        old_file.unlink()

# === Movie Helpers ===

def get_movie_by_title(movies: list, title: str) -> dict:
    """Find a movie by exact title (case-insensitive)."""
    return next((m for m in movies if m.get("title", "").lower() == title.lower()), None)

def get_movies_by_status(movies: list, status: str) -> list:
    """Filter movies by status."""
    return [m for m in movies if m.get("status") == status]

def get_currently_watching_movie(movies: list) -> dict:
    """Return the movie marked as currently-watching."""
    return next((m for m in movies if m.get("status") == "currently-watching"), None)

# === Manual Backup (.zip) ===

def create_backup_zip(output_path="backups/suvie_backup.zip"):
    """Zip movies.json and its backup history into a single archive."""
    with ZipFile(output_path, "w") as zipf:
        if Path(MOVIES_FILE).exists():
            zipf.write(MOVIES_FILE)
        for file in glob.glob("backups/json/*.json"):
            zipf.write(file)

# === Channel Display Updater ===

async def update_channel(bot, channel_name: str, movies: list, filter_func, embed_title: str, color: discord.Color):
    """Replace all messages in a channel with a single embed displaying filtered movie list."""
    channel = discord.utils.get(bot.get_all_channels(), name=channel_name)
    if not channel:
        print(f"Channel '{channel_name}' not found.")
        return

    entries = filter_func(movies)
    await channel.purge(limit=100)

    if not entries:
        await channel.send("No entries found.")
        return

    embed = discord.Embed(title=embed_title, color=color)
    for m in entries:
        info = f"**{m['title']}** ({m.get('year', 'N/A')})"
        if m.get("timestamp"):
            info += f" — `{m['timestamp']}`"
        if m.get("filepath"):
            info += f"\n`{m['filepath']}`"
        embed.add_field(name="", value=info, inline=False)

    await channel.send(embed=embed)

# === Specialized Channel Wrappers ===

async def update_watchlist_channel(bot, movies):
    await update_channel(
        bot, "watchlist", movies,
        lambda m: get_movies_by_status(m, "watchlist"),
        "🎬 Watchlist", discord.Color.teal()
    )

async def update_downloaded_channel(bot, movies):
    await update_channel(
        bot, "downloaded", movies,
        lambda m: get_movies_by_status(m, "downloaded"),
        "📥 Downloaded Movies", discord.Color.gold()
    )

async def update_watched_channel(bot, movies):
    await update_channel(
        bot, "watched", movies,
        lambda m: get_movies_by_status(m, "watched"),
        "✅ Watched Movies", discord.Color.from_rgb(255, 105, 180)  # Hot Pink
    )

async def update_currently_watching_channel(bot, movies):
    """Update the currently watching movie embed."""
    channel = discord.utils.get(bot.get_all_channels(), name="currently-watching")
    if not channel:
        print("Channel 'currently-watching' not found.")
        return

    movie = get_currently_watching_movie(movies)
    await channel.purge(limit=100)

    if not movie:
        await channel.send("No currently watching movie found.")
        return

    embed = discord.Embed(
        title=f"🎥 Currently Watching: {movie['title']}",
        color=discord.Color.green()
    )
    if movie.get("year"):
        embed.add_field(name="Year", value=movie["year"], inline=True)
    if movie.get("genre"):
        embed.add_field(name="Genre", value=movie["genre"], inline=True)
    if movie.get("timestamp"):
        embed.add_field(name="Time", value=movie["timestamp"], inline=True)
    if movie.get("filepath"):
        embed.add_field(name="File Path", value=movie["filepath"], inline=False)
    if movie.get("poster") and movie["poster"] != "N/A":
        embed.set_thumbnail(url=movie["poster"])

    await channel.send(embed=embed)

# === Special State Logic ===

def update_currently_watching(movies: list, imdb_id: str):
    """Reset all movies marked currently-watching, then set the new one."""
    for m in movies:
        if m.get("status") == "currently-watching":
            m["status"] = "watchlist"
        if m.get("imdb_id") == imdb_id:
            m["status"] = "currently-watching"
            
def get_downloaded_movie(movies: list, title: str) -> dict:
    movie = get_movie_by_title(movies, title)
    return movie if movie and movie.get("status") == "downloaded" else None