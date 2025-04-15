import sys
import os
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func

# === Fix import path for local + prod ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
print(f"🔍 PYTHONPATH: {sys.path[-1]}")

# === Local Imports ===
from bot.models.movie import Movie
from bot.utils.database import engine
from bot.utils.storage import (
    get_movies_by_status,
    update_watchlist_channel,
    create_embed
)
from bot.utils.imdb import fetch_movie_data

class WatchlistGroup(commands.GroupCog, name="watchlist"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="add", description="Add a movie or show to your watchlist.")
    async def add(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(ephemeral=True)
        print("✅ /watchlist add triggered with title:", title)

        guild_id = str(interaction.guild_id or 0)

        try:
            with Session(engine) as session:
                # Check for duplicates using case-insensitive matching
                duplicate = session.scalar(
                    select(Movie).where(
                        func.lower(Movie.guild_id) == func.lower(guild_id),
                        func.lower(Movie.title) == func.lower(title),
                        Movie.status == "watchlist"
                    )
                )
                if duplicate:
                    await interaction.followup.send("❌ This title is already in your watchlist.", ephemeral=True)
                    return

            movie_data = fetch_movie_data(title=title)
            print("📦 OMDb response:", movie_data)

            new_movie = Movie(
                guild_id=guild_id,
                title=movie_data["title"],
                year=movie_data.get("year"),
                genre=movie_data.get("genre"),
                plot=movie_data.get("plot"),
                poster=movie_data.get("poster"),
                imdb_url=movie_data.get("imdb_url"),
                imdb_id=movie_data.get("imdb_id"),
                imdb_rating=movie_data.get("imdb_rating"),
                director=movie_data.get("director"),
                actors=movie_data.get("actors"),
                type=movie_data.get("type", "movie"),
                status="watchlist"
            )

            with Session(engine) as session:
                session.add(new_movie)
                session.commit()
                print("💾 Movie saved to DB:", new_movie.title)

            await update_watchlist_channel(self.bot, int(interaction.guild_id))
            embed = create_embed(new_movie, title_prefix="🎬 Added to Watchlist: ", color=discord.Color.teal())
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"❌ Error in /add: {e}")
            await interaction.followup.send(f"❌ DB Error: {e}", ephemeral=True)

    @app_commands.command(name="remove", description="Remove a movie or show from your watchlist.")
    async def remove(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(ephemeral=True)
        print("🗑️ /watchlist remove triggered with title:", title)

        try:
            guild_id = str(interaction.guild_id or 0)

            with Session(engine) as session:
                # Case-insensitive fuzzy match (trimming + lower)
                stmt = select(Movie).where(
                    func.lower(Movie.guild_id) == func.lower(guild_id),
                    func.lower(Movie.title).like(f"%{title.lower()}%"),
                    Movie.status == "watchlist"
                )
                movie = session.scalar(stmt)

                if not movie:
                    await interaction.followup.send("❌ Title not found in your watchlist.", ephemeral=True)
                    return

                session.delete(movie)
                session.commit()
                print(f"🗑️ Removed: {movie.title}")

            await update_watchlist_channel(self.bot, int(interaction.guild_id))
            await interaction.followup.send(f"🗑️ Removed **{movie.title}** from your watchlist.", ephemeral=True)

        except Exception as e:
            print(f"❌ Error in /remove: {e}")
            await interaction.followup.send(f"❌ DB Error: {e}", ephemeral=True)

    @app_commands.command(name="view", description="View your current watchlist.")
    async def view(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        print("👀 /watchlist view triggered")

        try:
            guild_id = str(interaction.guild_id or 0)
            watchlist = get_movies_by_status(guild_id, "watchlist")

            if not watchlist:
                await interaction.followup.send("📭 Your watchlist is empty.", ephemeral=True)
                return

            for movie in watchlist:
                embed = create_embed(movie, color=discord.Color.teal())
                await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"❌ Error in /view: {e}")
            await interaction.followup.send(f"❌ DB Error: {e}", ephemeral=True)

    @app_commands.command(name="clear", description="Clear your watchlist completely.")
    async def clear(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        print("🧹 /watchlist clear triggered")

        try:
            guild_id = str(interaction.guild_id or 0)

            with Session(engine) as session:
                count = session.query(Movie).filter_by(guild_id=guild_id, status="watchlist").delete()
                session.commit()
                print(f"🧹 Cleared {count} entries")

            await update_watchlist_channel(self.bot, int(interaction.guild_id))

            if count:
                await interaction.followup.send("✅ Watchlist cleared.", ephemeral=True)
            else:
                await interaction.followup.send("❌ Your watchlist was already empty.", ephemeral=True)

        except Exception as e:
            print(f"❌ Error in /clear: {e}")
            await interaction.followup.send(f"❌ DB Error: {e}", ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(WatchlistGroup(bot))
    print("📁 Watchlist command loaded.")