import discord
from datetime import datetime
from zipfile import ZipFile
from sqlalchemy.orm import Session
from sqlalchemy import select
from pathlib import Path
from typing import Optional, List

from bot.utils.database import engine
from bot.models.movie import Movie
from bot.utils.ui import generate_movie_embed

BACKUP_DIR = Path("backups/json")

# === Load & Save ===

def load_movies(guild_id: int) -> List[Movie]:
    with Session(engine) as session:
        return session.scalars(select(Movie).where(Movie.guild_id == guild_id)).all()

def save_movie(movie: Movie):
    with Session(engine) as session:
        session.add(movie)
        session.commit()

def delete_movie(guild_id: int, title: str) -> bool:
    with Session(engine) as session:
        result = session.scalar(
            select(Movie).where(
                Movie.guild_id == guild_id,
                Movie.title.ilike(title)
            )
        )
        if result:
            session.delete(result)
            session.commit()
            return True
        return False

def clear_movies_by_status(guild_id: int, status: str):
    with Session(engine) as session:
        movies = session.scalars(
            select(Movie).where(
                Movie.guild_id == guild_id,
                Movie.status == status
            )
        ).all()
        for m in movies:
            session.delete(m)
        session.commit()

# === Filters ===

def get_movie_by_title(guild_id: int, title: str) -> Optional[Movie]:
    with Session(engine) as session:
        return session.scalar(
            select(Movie).where(
                Movie.guild_id == guild_id,
                Movie.title.ilike(title)
            )
        )

def get_movies_by_status(guild_id: int, status: str) -> List[Movie]:
    with Session(engine) as session:
        return session.scalars(
            select(Movie).where(
                Movie.guild_id == guild_id,
                Movie.status == status
            )
        ).all()

def get_downloaded_movies(guild_id: int) -> List[Movie]:
    with Session(engine) as session:
        return session.scalars(
            select(Movie).where(
                Movie.guild_id == guild_id,
                Movie.downloaded == True
            )
        ).all()

def get_currently_watching_movies(guild_id: int) -> List[Movie]:
    return get_movies_by_status(guild_id, "currently-watching")

# === Embeds ===

# def create_embed(movie: Movie, title_prefix="", color=discord.Color.teal()) -> discord.Embed:
#     title = movie.title
#     if movie.type == "series":
#         season = int(movie.season or 1)
#         episode = int(movie.episode or 1)
#         title = f"{title} (S{season:02}E{episode:02})"

#     embed = discord.Embed(title=f"{title_prefix}{title}", color=color)

#     if movie.poster and movie.poster != "N/A":
#         embed.set_thumbnail(url=movie.poster)

#     for key in ["genre", "year", "filepath", "timestamp", "imdb_url"]:
#         value = getattr(movie, key, None)
#         if value:
#             name = key.capitalize() if key != "imdb_url" else "IMDb"
#             embed.add_field(name=name, value=value, inline=(key != "filepath"))

#     return embed

# === Channel Updates ===

async def update_channel(bot: discord.Client, guild_id: int, channel_name: str, movies: List[Movie], title_prefix="", color=discord.Color.teal()):
    guild = bot.get_guild(guild_id)
    if not guild:
        print("⚠️ Guild not found.")
        return

    channel = discord.utils.get(guild.text_channels, name=channel_name)
    if not channel:
        try:
            category = discord.utils.get(guild.categories, name="🎬 suvie")
            if not category:
                category = await guild.create_category("🎬 suvie")
            channel = await guild.create_text_channel(channel_name, category=category)
        except Exception as e:
            print(f"❌ Failed to create channel {channel_name}: {e}")
            return

    await channel.purge(limit=10)

    if not movies:
        await channel.send("📭 Nothing to show here.")
        return

    for movie in movies:
        embed = generate_movie_embed(movie, title_prefix)
        await channel.send(embed=embed)

async def update_watchlist_channel(bot: discord.Client, guild_id: int):
    movies = get_movies_by_status(guild_id, "watchlist")
    await update_channel(bot, guild_id, "watchlist", movies, color=discord.Color.teal())

async def update_currently_watching_channel(bot: discord.Client, guild_id: int):
    movies = get_movies_by_status(guild_id, "currently-watching")
    await update_channel(bot, guild_id, "currently-watching", movies, "🎬 Currently Watching: ", color=discord.Color.orange())

async def update_downloaded_channel(bot: discord.Client, guild_id: int):
    movies = get_downloaded_movies(guild_id)
    await update_channel(bot, guild_id, "downloaded", movies, color=discord.Color.green())

async def update_watched_channel(bot: discord.Client, guild_id: int):
    movies = get_movies_by_status(guild_id, "watched")
    await update_channel(bot, guild_id, "watched", movies, color=discord.Color.purple())

# === Backup ===

def create_backup_zip():
    zip_path = Path("backups/backup.zip")
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path, "w") as zipf:
        pass
    return zip_path

async def get_or_create_text_channel(bot: discord.Client, guild: discord.Guild, name: str) -> discord.TextChannel:
    existing = discord.utils.get(guild.text_channels, name=name)
    if existing:
        return existing
    try:
        category = discord.utils.get(guild.categories, name="🎬 suvie")
        if not category:
            category = await guild.create_category("🎬 suvie")
        return await guild.create_text_channel(name, category=category)
    except Exception as e:
        print(f"[Channel Creation Error] {type(e).__name__}: {e}")
        return None
