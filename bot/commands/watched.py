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
        timestamp="Optional: Timestamp when you stopped watching (e.g. 01:23:45 or auto-generated)",
        season="Optional: Season number (TV series only)",
        episode="Optional: Episode number (TV series only)",
        filepath="Optional: File path or location of the file"
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
        print(f"🎞️ /watched: {title}")

        guild_id = interaction.guild_id
        try:
            with Session(engine) as session:
                movie = session.query(Movie).filter(
                    Movie.guild_id == guild_id,
                    Movie.title.ilike(title)
                ).first()

                if not movie:
                    await interaction.followup.send("❌ Movie not found in your library.", ephemeral=True)
                    return

                # === Update movie ===
                movie.status = "watched"
                now = datetime.now()
                movie.timestamp = timestamp or now.strftime("%H:%M:%S %d/%m/%Y")
                if filepath:
                    movie.filepath = filepath
                if movie.type == "series":
                    if season:
                        movie.season = season
                    if episode:
                        movie.episode = episode

                # ✅ Cache values BEFORE closing session
                title_display = f"{movie.title} (S{int(movie.season):02}E{int(movie.episode):02})" if movie.type == "series" else movie.title
                watched_at = movie.timestamp
                year = movie.year
                genre = movie.genre
                file_path = movie.filepath
                imdb = movie.imdb_url
                poster = movie.poster

                session.commit()
                print("✅ Movie marked as watched.")

            # === Embed ===
            embed = discord.Embed(
                title=f"✅ Archived: {title_display}",
                color=discord.Color.from_rgb(255, 105, 180)
            )
            embed.add_field(name="Watched At", value=watched_at, inline=True)
            if year:
                embed.add_field(name="Year", value=year, inline=True)
            if genre:
                embed.add_field(name="Genre", value=genre, inline=True)
            if file_path:
                embed.add_field(name="File Path", value=file_path, inline=False)
            if imdb:
                embed.add_field(name="IMDb", value=imdb, inline=False)
            if poster and poster != "N/A":
                embed.set_thumbnail(url=poster)

            await update_watched_channel(self.bot, guild_id)
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"❌ Error in /watched: {type(e).__name__}: {e}")
            await interaction.followup.send("❌ Failed to mark as watched.", ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(WatchedCog(bot))
    print("🎞️ Watched command loaded.")