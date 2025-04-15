import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from bot.models.movie import Movie
from bot.utils.database import engine
from bot.utils.storage import update_downloaded_channel

class DownloadedCog(commands.GroupCog, name="downloaded"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="add", description="Mark a movie or show as downloaded.")
    @app_commands.describe(
        title="The title of the movie or show.",
        imdb_id="The IMDb ID (optional).",
        filepath="Path to the downloaded file (optional)."
    )
    async def add(
        self,
        interaction: discord.Interaction,
        title: str,
        imdb_id: Optional[str] = None,
        filepath: Optional[str] = None
    ):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id
        print(f"📥 /downloaded add: {title}")

        try:
            with Session(engine) as session:
                match = session.query(Movie).filter(
                    Movie.guild_id == guild_id,
                    (func.lower(Movie.title) == title.lower()) |
                    (Movie.imdb_id == imdb_id)
                ).first()

                if not match:
                    await interaction.followup.send("❌ Title not found in your library.", ephemeral=True)
                    return

                match.filepath = filepath or match.filepath or None
                match.status = "downloaded"

                # Cache display values before closing session
                title_display = match.title
                suffix = f" (S{match.season:02}E{match.episode:02})" if match.type == "series" and match.season and match.episode else ""
                file = match.filepath
                imdb = match.imdb_url
                poster = match.poster

                session.commit()
                print("✅ Movie marked as downloaded.")

            await update_downloaded_channel(self.bot, guild_id)

            embed = discord.Embed(
                title=f"📥 Marked as Downloaded: {title_display}{suffix}",
                color=discord.Color.gold()
            )
            if file:
                embed.add_field(name="File", value=file, inline=False)
            if imdb:
                embed.add_field(name="IMDb", value=imdb, inline=False)
            if poster and poster != "N/A":
                embed.set_thumbnail(url=poster)

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"❌ Error in /downloaded add: {type(e).__name__}: {e}")
            await interaction.followup.send("❌ Failed to mark as downloaded.", ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(DownloadedCog(bot))
    print("📥 Downloaded command loaded.")