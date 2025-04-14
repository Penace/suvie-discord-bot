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
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="initserver", description="Set up all required Suvie channels.")
    @app_commands.checks.has_permissions(administrator=True)
    async def initserver(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        print("👀 Running /initserver")

        guild = interaction.guild
        if not guild:
            await interaction.followup.send("❌ This command must be used in a server.", ephemeral=True)
            return

        # Get or create category
        category = discord.utils.get(guild.categories, name="🎬 suvie")
        if not category:
            category = await guild.create_category("🎬 suvie")
            print(f"📁 Created category: {category.name}")

        created: list[str] = []
        existing: list[str] = []

        for name in REQUIRED_CHANNELS:
            channel = discord.utils.get(guild.text_channels, name=name)
            if not channel:
                try:
                    await guild.create_text_channel(name, category=category)
                    created.append(name)
                    print(f"✅ Created: #{name}")
                except Exception as e:
                    print(f"❌ Failed to create #{name}: {e}")
            else:
                existing.append(name)
                print(f"✔️ Already exists: #{name}")

        # Summary Embed
        embed = discord.Embed(
            title="✅ Suvie Setup Complete",
            description="All required channels are now ready.",
            color=discord.Color.green()
        )
        if created:
            embed.add_field(name="📁 Created Channels", value="\n".join(f"#{c}" for c in created), inline=False)
        if existing:
            embed.add_field(name="📂 Already Exists", value="\n".join(f"#{c}" for c in existing), inline=False)

        embed.set_footer(text="Run this again if you accidentally delete channels.")
        await interaction.followup.send(embed=embed, ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(InitServerCog(bot))
    print("🚀 Loaded cog: initserver")