import traceback
import discord
from discord import app_commands
from discord.ext import commands
from utils.storage import load_movies, save_movies
from utils.imdb import fetch_movie_data

class AddMovieCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="addmovie", description="Add a movie to your watchlist.")
    @app_commands.describe(
        title="The title of the movie you want to add.",
        imdb_id="The IMDb ID of the movie (optional).",
        year="The release year of the movie (optional).",
        filepath="The path to the movie file (optional).",
        genre="The genre of the movie (optional)."
    )
    async def add_movie(
        self,
        interaction: discord.Interaction,
        title: str,
        imdb_id: str = None,
        year: str = None,
        filepath: str = None,
        genre: str = None
    ):
        try:
            await interaction.response.defer(ephemeral=False)

            movie_data = fetch_movie_data(imdb_id=imdb_id, title=title)
            if not movie_data:
                raise ValueError("Could not fetch movie details.")

            movie_data["year"] = year or movie_data.get("year", "N/A")
            movie_data["genre"] = genre or movie_data.get("genre", "N/A")
            movie_data["filepath"] = filepath or None

            movies = load_movies()
            if any(m.get("imdb_id") == movie_data.get("imdb_id") for m in movies):
                await interaction.followup.send("⚠️ This movie is already in your watchlist.", ephemeral=True)
                return

            movies.append(movie_data)
            save_movies(movies)

            embed = discord.Embed(
                title=f"{movie_data['title']} ({movie_data['year']})",
                description=movie_data.get("plot", "No description available."),
                color=discord.Color.teal()
            )
            embed.add_field(name="Genre", value=movie_data["genre"], inline=True)
            embed.add_field(name="IMDb", value=movie_data["imdb_url"], inline=False)
            if filepath:
                embed.add_field(name="File Path", value=filepath, inline=False)
            if movie_data.get("poster") and movie_data["poster"] != "N/A":
                embed.set_thumbnail(url=movie_data["poster"])

            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(
                f"❌ Something went wrong while adding the movie:\n`{str(e)}`",
                ephemeral=True
            )
            traceback.print_exc()

async def setup(bot: commands.Bot):
    await bot.add_cog(AddMovieCog(bot))