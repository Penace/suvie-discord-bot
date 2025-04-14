import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = datetime.now()

    def get_uptime(self) -> str:
        delta = datetime.now() - self.start_time
        return str(delta).split(".")[0]

    @app_commands.command(name="ping", description="Check if Suvie is alive.")
    async def ping(self, interaction: discord.Interaction):
        latency_ms = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: `{latency_ms}ms`",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Uptime: {self.get_uptime()}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
    print("📶 Ping command loaded.")