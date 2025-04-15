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
        print(f"👀 Running /initserver in {interaction.guild.name} ({interaction.guild_id})")

        guild = interaction.guild
        if not guild:
            await interaction.followup.send("❌ This command must be used in a server.", ephemeral=True)
            return

        try:
            # Find or create "🎬 suvie" category
            category = discord.utils.get(guild.categories, name="🎬 suvie")
            if not category:
                category = await guild.create_category("🎬 suvie")
                print(f"📁 Created category: {category.name}")

            created = []
            existing = []

            for name in REQUIRED_CHANNELS:
                # Check if channel exists under the correct category
                existing_channel = discord.utils.get(guild.text_channels, name=name, category=category)
                if not existing_channel:
                    try:
                        await guild.create_text_channel(name, category=category)
                        created.append(name)
                        print(f"✅ Created channel: #{name}")
                    except discord.Forbidden:
                        print(f"🚫 Missing permissions to create channel: #{name}")
                    except Exception as e:
                        print(f"❌ Failed to create channel #{name}: {e}")
                else:
                    existing.append(name)
                    print(f"✔️ Channel already exists: #{name}")

            # === Summary Embed ===
            embed = discord.Embed(
                title="✅ Suvie Setup Complete",
                description="Required channels have been created or confirmed.",
                color=discord.Color.green()
            )
            if created:
                embed.add_field(name="📁 Created", value="\n".join(sorted(f"#{c}" for c in created)), inline=False)
            if existing:
                embed.add_field(name="📂 Already Exists", value="\n".join(sorted(f"#{c}" for c in existing)), inline=False)

            embed.set_footer(text="Run this command again if channels are ever deleted.")
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(f"❌ Error during /initserver: {e}")
            await interaction.followup.send("❌ Something went wrong during initialization.", ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(InitServerCog(bot))
    print("🚀 Loaded cog: initserver")