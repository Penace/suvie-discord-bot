import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from bot.models.movie import Movie
from bot.utils.database import engine
from bot.utils.storage import update_watched_channel

class WatchedCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="watched", description="Mark a movie or TV show as watched (from any list).")
    @app_commands.describe(
        title="The title of the movie or show you've finished watching.",
        timestamp="Optional: Timestamp (e.g. 01:23:45 or auto-generated)",
        season="Optional: Season number (for series)",
        episode="Optional: Episode number (for series)",
        filepath="Optional: File path or location"
    )
    async def watched(
        self,
        interaction: discord.Interaction,
        title: str,
        timestamp: Optional[str] = None,
        season: Optional[int] = None,
        episode: Optional[int] = None,
        filepath: Optional[str] = None
    ):
        await interaction.response.defer(ephemeral=True)
        print(f"🎞️ /watched triggered: {title}")

        guild_id = interaction.guild_id
        if guild_id is None:
            await interaction.followup.send("❌ This command must be used in a server.", ephemeral=True)
            return

        try:
            with Session(engine) as session:
                movie = session.query(Movie).filter(
                    Movie.guild_id == guild_id,
                    Movie.title.ilike(title)
                ).first()

                if not movie:
                    await interaction.followup.send("❌ Movie not found in your library.", ephemeral=True)
                    return

                # === Update fields ===
                movie.status = "watched"
                now = datetime.now()

                # Apply episode/season only if series
                if movie.type == "series":
                    if season:
                        movie.season = season
                    if episode:
                        movie.episode = episode

                # Timestamp (custom or now)
                movie.timestamp = timestamp or now.strftime("%H:%M:%S %d/%m/%Y")

                if filepath:
                    movie.filepath = filepath

                session.commit()
                print(f"✅ Marked as watched: {movie.title} ({movie.status})")

            # === Display title for series ===
            suffix = f" (S{movie.season:02}E{movie.episode:02})" if movie.type == "series" and movie.season and movie.episode else ""
            embed = discord.Embed(
                title=f"✅ Archived: {movie.title}{suffix}",
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
            import traceback
            error_trace = traceback.format_exc()
            print(f"❌ Error in /watched: {type(e).__name__}: {e}")
            print(error_trace)
            await interaction.followup.send(f"❌ Failed to mark as watched.\nError: {type(e).__name__}: {e}", ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(WatchedCog(bot))
    print("🎞️ Watched command loaded.")