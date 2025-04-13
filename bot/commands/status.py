import discord
from discord import app_commands
from discord.ext import commands, tasks
from datetime import datetime
import os
import platform
from typing import Optional

from utils.storage import get_or_create_text_channel  # 🆕 for safe channel creation

class StatusCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.start_time = datetime.now()
        self.status_channel_name = "suvi-status"
        self.update_status_channel.start()

    def cog_unload(self):
        self.update_status_channel.cancel()

    def get_uptime(self) -> str:
        return str(datetime.now() - self.start_time).split(".")[0]

    @app_commands.command(name="status", description="View Suvie's system status.")
    async def status(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = self.generate_status_embed()
        await interaction.followup.send(embed=embed, ephemeral=True)

    def generate_status_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="🧠 Suvie Status",
            description="Current system metrics and state.",
            color=discord.Color.teal()
        )
        embed.add_field(name="⏳ Uptime", value=self.get_uptime(), inline=True)
        embed.add_field(name="⚙️ Cogs", value=len(self.bot.cogs), inline=True)
        embed.add_field(name="📜 Commands", value=len(self.bot.tree.get_commands()), inline=True)
        embed.add_field(name="🖥️ Platform", value=f"{platform.system()} {platform.release()}", inline=True)
        embed.add_field(name="📅 Last Check", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.set_footer(text="Status auto-refreshes every 5 minutes.")
        return embed

    @tasks.loop(minutes=5)
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
    print("📊 Status command loaded.")