import discord
from discord.ext import commands
from discord import app_commands
from utils.storage import load_movies, get_movies_by_status

class WatchlistCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="watchlist", description="View your current watchlist.")
    async def watchlist(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)  # Prevents timeout on longer responses

        movies = load_movies()
        watchlist = get_movies_by_status(movies, "watchlist")

        if not watchlist:
            await interaction.followup.send("📭 Your watchlist is currently empty.", ephemeral=True)
            return

        embeds = []
        for movie in watchlist:
            embed = discord.Embed(
                title=f"{movie['title']} ({movie.get('year', 'N/A')})",
                description=movie.get("plot", "No description available."),
                color=discord.Color.blue()
            )
            embed.add_field(name="Genre", value=movie.get("genre", "N/A"), inline=True)
            embed.add_field(name="IMDb", value=movie.get("imdb_url", "N/A"), inline=False)
            if movie.get("filepath"):
                embed.add_field(name="File Path", value=movie["filepath"], inline=False)
            if movie.get("poster") and movie["poster"] != "N/A":
                embed.set_thumbnail(url=movie["poster"])
            embeds.append(embed)

        for embed in embeds:
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(WatchlistCog(bot))