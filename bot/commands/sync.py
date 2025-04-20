from discord.ext import commands
from discord import app_commands

class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx):
        synced = await self.bot.tree.sync()
        await ctx.send(f"🔁 Synced {len(synced)} command(s) globally.")

async def setup(bot):
    await bot.add_cog(Sync(bot))