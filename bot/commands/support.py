import discord
from discord.ext import commands

class SupportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="invite")
    async def invite(self, ctx):
        embed = discord.Embed(
            title="➕ Invite Suvie to Your Server",
            description="[Click here to invite](https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=277025508352)",
            color=0xff2d84
        )
        await ctx.send(embed=embed)

    @commands.command(name="support")
    async def support(self, ctx):
        embed = discord.Embed(
            title="💖 Support Suvie",
            description="This project is fully open-source and fueled by community support.\n\n**Ways to support:**\n• [Ko-fi](https://ko-fi.com/penace)\n• [Buy Me a Coffee](https://buymeacoffee.com/penace)\n\nEvery bit helps!",
            color=0xff2d84
        )
        embed.set_footer(text="Made by Penace • suvie.me")
        await ctx.send(embed=embed)

    @commands.command(name="donate")
    async def donate(self, ctx):
        embed = discord.Embed(
            title="☕ Donate to Suvie",
            description="Choose your preferred way to support Suvie:\n\n- Ko-fi → [ko-fi.com/penace](https://ko-fi.com/penace)\n- BMC → [buymeacoffee.com/penace](https://buymeacoffee.com/penace)",
            color=0x4e5fff
        )
        embed.set_thumbnail(url="https://storage.ko-fi.com/cdn/useruploads/display/penace.png")  # optional
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SupportCog(bot))