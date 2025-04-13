import discord
from discord.ext import commands
from discord import app_commands
from pathlib import Path

from utils.storage import create_backup_zip

class BackupCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="backup", description="Create and download a full Suvie backup.")
    async def backup_now(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        # Create the backup first
        zip_path = create_backup_zip()

        if not zip_path.exists():
            await interaction.followup.send("❌ Backup failed to generate.", ephemeral=True)
            return

        file = discord.File(fp=zip_path, filename=zip_path.name)
        await interaction.followup.send(content="📦 Here is your latest backup:", file=file, ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(BackupCog(bot))
    print("📁 Backup command loaded.")