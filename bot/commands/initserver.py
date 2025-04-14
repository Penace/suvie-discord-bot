import discord
from discord import app_commands
from discord.ext import commands

REQUIRED_CHANNELS = [
    "watchlist",
    "currently-watching",
    "downloaded",
    "watched",
    "suvie-status",
    "suvie-ai"
]

class InitServerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="initserver", description="Set up all required suvie channels.")
    @app_commands.checks.has_permissions(administrator=True)
    async def initserver(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        print("👀 Starting /initserver command")


        guild = interaction.guild
        if not guild:
            await interaction.followup.send("❌ This command can only be used in a server.", ephemeral=True)
            return

        # Create or get the 🎬 suvie category
        category = discord.utils.get(guild.categories, name="🎬 suvie")
        if not category:
            category = await guild.create_category("🎬 suvie")
            print(f"📁 Using category: {category.name}")

        created = []
        for name in REQUIRED_CHANNELS:
            try:
                if not discord.utils.get(guild.text_channels, name=name):
                    await guild.create_text_channel(name, category=category)
                    created.append(f"📁 #{name}")
                    print(f"✅ Created or verified #{name}")
            except Exception as e:
                print(f"❌ Failed to create #{name}: {e}")

        # Summary Embed
        embed = discord.Embed(
            title="✅ suvie Setup Complete",
            description="Your server is ready to go! Here are the channels I created or verified:",
            color=discord.Color.green()
        )
        for name in REQUIRED_CHANNELS:
            embed.add_field(name=f"#{name}", value="Ready ✅", inline=True)

        await interaction.followup.send("✅ Suvie setup command reached this point.", ephemeral=True)
# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(InitServerCog(bot))
    print("🚀 InitServer command loaded.")