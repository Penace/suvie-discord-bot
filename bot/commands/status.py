import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import discord
from discord import app_commands
from discord.ext import commands, tasks
from datetime import datetime
import platform

from sqlalchemy.orm import Session
from bot.utils.database import SessionLocal
from bot.models.movie import Movie
from bot.utils.storage import get_or_create_text_channel

class StatusCog(commands.GroupCog, name="status"):  # 👈 Make it a GroupCog
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = datetime.now()
        self.status_channel_name = "suvie-status"
        self.update_status_channel.start()

    def cog_unload(self):
        self.update_status_channel.cancel()

    def get_uptime(self) -> str:
        return str(datetime.now() - self.start_time).split(".")[0]

    def get_total_movies(self) -> int:
        try:
            with SessionLocal() as session:
                return session.query(Movie).count()
        except Exception as e:
            print(f"[Status DB Error] {type(e).__name__}: {e}")
            return -1

    def generate_status_embed(self) -> discord.Embed:
        total_movies = self.get_total_movies()
        embed = discord.Embed(
            title="🧠 Suvie Status",
            description="Live system metrics & runtime diagnostics.",
            color=discord.Color.teal()
        )
        embed.add_field(name="⏳ Uptime", value=self.get_uptime(), inline=True)
        embed.add_field(name="🎞️ Movies Tracked", value=f"{total_movies if total_movies >= 0 else '⚠️ Error'}", inline=True)
        embed.add_field(name="⚙️ Cogs", value=str(len(self.bot.cogs)), inline=True)
        embed.add_field(name="📜 Commands", value=str(len(self.bot.tree.get_commands())), inline=True)
        embed.add_field(name="🖥️ Platform", value=f"{platform.system()} {platform.release()}", inline=True)
        embed.add_field(name="📅 Last Check", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.set_footer(text="Auto-refreshes every 12 minutes. Try /status ping to test latency.")
        return embed

    @app_commands.command(name="status", description="View Suvie's system status.")
    async def status(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = self.generate_status_embed()
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="ping", description="Check Suvie's response time.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        latency_ms = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: `{latency_ms}ms`",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Uptime: {self.get_uptime()}")
        await interaction.followup.send(embed=embed, ephemeral=True)

    @tasks.loop(minutes=12)
    async def update_status_channel(self):
        for guild in self.bot.guilds:
            channel = await get_or_create_text_channel(self.bot, guild, self.status_channel_name)
            if not channel:
                continue

            embed = self.generate_status_embed()
            async for msg in channel.history(limit=5):
                if msg.author == self.bot.user:
                    await msg.edit(embed=embed)
                    break
            else:
                await channel.send(embed=embed)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(StatusCog(bot))
    print("📊 Loaded cog: status group")