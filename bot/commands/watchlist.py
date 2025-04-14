import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from sqlalchemy.orm import Session

from models.movie import Movie
from utils.database import engine
from utils.storage import (
    get_movie_by_title,
    get_movies_by_status,
    update_watchlist_channel,
    create_embed
)
from utils.imdb import fetch_movie_model  # ✅ Use model-based fetch

class WatchlistGroup(commands.GroupCog, name="watchlist"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="add", description="Add a movie or TV show to your watchlist.")
    async def add(
        self,
        interaction: discord.Interaction,
        title: str,
        imdb_id: Optional[str] = None,
        filepath: Optional[str] = None,
        genre: Optional[str] = None,
        year: Optional[str] = None,
        season: Optional[int] = None,
        episode: Optional[int] = None
    ):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id or 0

        if get_movie_by_title(guild_id, title):
            await interaction.followup.send("❌ This title is already in your library.", ephemeral=True)
            return

        try:
            new_movie = fetch_movie_model(
                title=title,
                imdb_id=imdb_id,
                guild_id=guild_id,
                status="watchlist",
                season=season,
                episode=episode,
                filepath=filepath
            )

            # Allow overrides
            if genre: new_movie.genre = genre
            if year: new_movie.year = year

        except Exception as e:
            await interaction.followup.send(f"❌ Failed to fetch movie data: {e}", ephemeral=True)
            return

        with Session(engine) as session:
            session.add(new_movie)
            session.commit()

        await update_watchlist_channel(self.bot, guild_id)

        display = f"{new_movie.title} (S{new_movie.season})" if new_movie.type == "series" else new_movie.title
        embed = create_embed(new_movie, title_prefix="🎬 Added to Watchlist: ", color=discord.Color.teal())
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="remove", description="Remove a movie or show from your watchlist.")
    async def remove(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id or 0

        with Session(engine) as session:
            movie = session.query(Movie).filter_by(guild_id=guild_id, title=title, status="watchlist").first()
            if not movie:
                await interaction.followup.send("❌ Title not found in your watchlist.", ephemeral=True)
                return
            session.delete(movie)
            session.commit()

        await update_watchlist_channel(self.bot, guild_id)
        await interaction.followup.send(f"🗑️ Removed **{title}** from your watchlist.", ephemeral=True)

    @app_commands.command(name="view", description="View your watchlist.")
    async def view(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id or 0
        watchlist = get_movies_by_status(guild_id, "watchlist")

        if not watchlist:
            await interaction.followup.send("📭 Your watchlist is empty.", ephemeral=True)
            return

        for movie in watchlist:
            embed = create_embed(movie, color=discord.Color.teal())
            await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="clear", description="Clear your entire watchlist.")
    async def clear(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id or 0

        with Session(engine) as session:
            deleted = session.query(Movie).filter_by(guild_id=guild_id, status="watchlist").delete()
            session.commit()

        if not deleted:
            await interaction.followup.send("❌ Your watchlist is already empty.", ephemeral=True)
        else:
            await update_watchlist_channel(self.bot, guild_id)
            await interaction.followup.send("✅ Watchlist cleared.", ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(WatchlistGroup(bot))
    print("📁 Watchlist command loaded.")