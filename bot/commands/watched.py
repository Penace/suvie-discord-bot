import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from bot.models.movie import Movie
from bot.utils.database import engine
from bot.utils.storage import (
    update_watched_channel
)

class WatchedCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="watched", description="Mark a movie or TV show as watched.")
    @app_commands.describe(
        title="The title of the movie or show you've finished watching.",
        timestamp="Optional: Timestamp when you stopped watching (e.g. 01:23:45)",
        filepath="Optional: File path or location of the file"
    )
    async def watched(
        self,
        interaction: discord.Interaction,
        title: str,
        timestamp: Optional[str] = None,
        filepath: Optional[str] = None
    ):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id
        if guild_id is None:
            await interaction.followup.send("❌ This command must be run in a server.", ephemeral=True)
            return

        try:
            with Session(engine) as session:
                movie = session.query(Movie).filter_by(guild_id=guild_id, title=title).first()
                if not movie:
                    await interaction.followup.send("❌ Movie not found in your library.", ephemeral=True)
                    return

                movie.status = "watched"
                movie.timestamp = timestamp or datetime.now().strftime("%H:%M:%S")
                if filepath:
                    movie.filepath = filepath
                session.commit()

                embed = discord.Embed(
                    title=f"✅ Marked as Watched: {movie.title}",
                    color=discord.Color.from_rgb(255, 105, 180)
                )
                embed.add_field(name="Watched At", value=movie.timestamp, inline=True)
                if movie.year:
                    embed.add_field(name="Year", value=movie.year, inline=True)
                if movie.genre:
                    embed.add_field(name="Genre", value=movie.genre, inline=True)
                if movie.filepath:
                    embed.add_field(name="File Path", value=movie.filepath, inline=False)
                if movie.imdb_url:
                    embed.add_field(name="IMDb", value=movie.imdb_url, inline=False)
                if movie.poster and movie.poster != "N/A":
                    embed.set_thumbnail(url=movie.poster)

            await update_watched_channel(self.bot, guild_id)
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"❌ Error in /watched: {e}")
            await interaction.followup.send("❌ Failed to mark as watched.", ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(WatchedCog(bot))
    print("🎞️ Watched command loaded.")
