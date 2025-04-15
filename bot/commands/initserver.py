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

CATEGORY_NAME = "🎬 suvie"

class InitServerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="initserver", description="Set up all required Suvie channels.")
    @app_commands.checks.has_permissions(administrator=True)
    async def initserver(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        print(f"👀 Running /initserver in {interaction.guild.name} ({interaction.guild_id})")

        guild = interaction.guild
        if not guild:
            await interaction.followup.send("❌ This command must be run in a server.", ephemeral=True)
            return

        try:
            # Get or create the "🎬 suvie" category
            category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
            if not category:
                category = await guild.create_category(CATEGORY_NAME)
                print(f"📁 Created category: {category.name}")

            created = []
            existing = []

            for channel_name in REQUIRED_CHANNELS:
                existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
                
                if existing_channel:
                    # Move channel to correct category if it's not already in it
                    if existing_channel.category_id != category.id:
                        try:
                            await existing_channel.edit(category=category)
                            print(f"📦 Moved #{channel_name} to '{CATEGORY_NAME}'")
                        except discord.Forbidden:
                            print(f"🚫 Permission denied to move #{channel_name}")
                    existing.append(channel_name)
                else:
                    try:
                        await guild.create_text_channel(channel_name, category=category)
                        created.append(channel_name)
                        print(f"✅ Created #{channel_name}")
                    except discord.Forbidden:
                        print(f"🚫 Missing permissions to create #{channel_name}")
                    except Exception as e:
                        print(f"❌ Failed to create #{channel_name}: {e}")

            embed = discord.Embed(
                title="✅ Suvie Setup Complete",
                description="All required channels are ready.",
                color=discord.Color.green()
            )
            if created:
                embed.add_field(name="📁 Created Channels", value="\n".join(f"#{c}" for c in created), inline=False)
            if existing:
                embed.add_field(name="📂 Already Existing", value="\n".join(f"#{c}" for c in existing), inline=False)
            embed.set_footer(text="You can rerun this command if channels are deleted or moved.")

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"❌ Error during /initserver: {type(e).__name__}: {e}")
            await interaction.followup.send("❌ Something went wrong during initialization.", ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(InitServerCog(bot))
    print("🚀 Loaded cog: initserver")