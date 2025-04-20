import discord
from discord import app_commands
from discord.ext import commands

class SupportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="invite", description="Get the link to invite Suvie to your server")
    async def invite(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="➕ Invite Suvie to Your Server",
            description="[Click here to invite](https://discord.com/oauth2/authorize?client_id=1360281760016892066&scope=bot+applications.commands&permissions=277025508352)",
            color=0x5865F2
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="support", description="Learn how to support Suvie development")
    async def support(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="💖 Support Suvie",
            description="This project is fully open-source and fueled by community support.\n\n**Ways to support:**\n• [Ko-fi](https://ko-fi.com/penace)\n• [Buy Me a Coffee](https://buymeacoffee.com/penace)\n\nEvery bit helps!",
            color=0xff2d84
        )
        embed.set_footer(text="Made by Penace • suvie.me")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="donate", description="Show donation links for Ko-fi and Buy Me a Coffee")
    async def donate(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="☕ Donate to Suvie",
            description="Choose your preferred way to support Suvie:\n\n- Ko-fi → [ko-fi.com/penace](https://ko-fi.com/penace)\n- BMC → [buymeacoffee.com/penace](https://buymeacoffee.com/penace)",
            color=0xFBBF24
        )
        embed.set_thumbnail(url="https://storage.ko-fi.com/cdn/useruploads/display/penace.png")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(SupportCog(bot))