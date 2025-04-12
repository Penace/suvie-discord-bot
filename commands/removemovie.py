import discord
from discord.ext import commands
from discord import app_commands
from utils.storage import load_movies, save_movies

class RemoveMovieCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="removemovie", description="Remove a movie from your watchlist.")
    @app_commands.describe(
        title="The title of the movie you want to remove."
    )
    async def removemovie(self, interaction: discord.Interaction, title: str):
        movies = load_movies()
        updated_movies = [m for m in movies if m.get("title", "").lower() != title.lower()]

        if len(updated_movies) == len(movies):
            await interaction.response.send_message("⚠️ No movie with that title found in your watchlist.", ephemeral=True)
            return

        save_movies(updated_movies)
        await interaction.response.send_message(f"🗑️ Removed **{title}** from your watchlist.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(RemoveMovieCog(bot))