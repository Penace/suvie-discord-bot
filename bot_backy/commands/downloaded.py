import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.movie import Movie
from utils.database import engine
from utils.storage import update_downloaded_channel

class DownloadedCog(commands.GroupCog, name="downloaded"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # === /downloaded add ===
    @app_commands.command(name="add", description="Mark a movie or show as downloaded.")
    @app_commands.describe(
        title="The title of the movie or show.",
        imdb_id="The IMDb ID (optional).",
        filepath="Path to the downloaded file (optional)."
    )
    async def add_downloaded(
        self,
        interaction: discord.Interaction,
        title: str,
        imdb_id: Optional[str] = None,
        filepath: Optional[str] = None
    ):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id or 0

        with Session(engine) as session:
            match = session.query(Movie).filter(
                (Movie.guild_id == guild_id) &
                ((func.lower(Movie.title) == title.lower()) | (Movie.imdb_id == imdb_id))
            ).first()

            if not match:
                await interaction.followup.send("❌ Title not found in your library.", ephemeral=True)
                return

            match.filepath = filepath or match.filepath or "N/A"
            match.status = "downloaded"
            session.commit()

        await update_downloaded_channel(self.bot, guild_id)

        suffix = ""
        if match.type == "series" and match.season is not None and match.episode is not None:
            suffix = f" (S{match.season:02}E{match.episode:02})"

        embed = discord.Embed(
            title=f"📥 Marked as Downloaded: {match.title}{suffix}",
            color=discord.Color.gold()
        )
        if match.filepath:
            embed.add_field(name="File", value=match.filepath, inline=False)
        if match.imdb_url:
            embed.add_field(name="IMDb", value=match.imdb_url, inline=False)
        if match.poster and match.poster != "N/A":
            embed.set_thumbnail(url=match.poster)

        await interaction.followup.send(embed=embed, ephemeral=True)

    # === /downloaded edit ===
    @app_commands.command(name="edit", description="Edit the file path of a downloaded movie.")
    @app_commands.describe(
        title="The title of the movie to update.",
        filepath="The new file path to assign."
    )
    async def edit_filepath(self, interaction: discord.Interaction, title: str, filepath: str):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id or 0

        with Session(engine) as session:
            movie = session.query(Movie).filter_by(guild_id=guild_id, title=title, status="downloaded").first()
            if not movie:
                await interaction.followup.send("❌ Movie not found in downloaded list.", ephemeral=True)
                return

            movie.filepath = filepath
            session.commit()

        await update_downloaded_channel(self.bot, guild_id)

        embed = discord.Embed(
            title=f"✏️ Filepath Updated: {movie.title}",
            color=discord.Color.gold()
        )
        embed.add_field(name="New File Path", value=filepath, inline=False)
        await interaction.followup.send(embed=embed, ephemeral=True)

    # === /downloaded remove ===
    @app_commands.command(name="remove", description="Remove a movie from downloaded list.")
    @app_commands.describe(title="The title of the movie to remove from downloaded.")
    async def remove_downloaded(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id or 0

        with Session(engine) as session:
            movie = session.query(Movie).filter_by(guild_id=guild_id, title=title, status="downloaded").first()
            if not movie:
                await interaction.followup.send("❌ Movie not found in downloaded list.", ephemeral=True)
                return

            movie.status = "watchlist"
            movie.filepath = None
            session.commit()

        await update_downloaded_channel(self.bot, guild_id)

        embed = discord.Embed(
            title=f"🗑️ Removed from Downloaded: {title}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(DownloadedCog(bot))
    print("📥 Downloaded command loaded.")