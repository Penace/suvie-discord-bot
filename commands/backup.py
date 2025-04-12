import discord
from discord.ext import commands
from discord import app_commands
from utils.storage import create_backup_zip
from pathlib import Path

class BackupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="backup", description="Create and download a full Suvie backup.")
    async def backup_now(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        zip_path = Path("backups/suvie_backup.zip")
        create_backup_zip(zip_path)

        if not zip_path.exists():
            await interaction.followup.send("❌ Backup failed to generate.", ephemeral=True)
            return

        file = discord.File(fp=zip_path, filename=zip_path.name)
        await interaction.followup.send(content="📦 Here is your latest backup:", file=file, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(BackupCog(bot))
    print("📁 Backup command loaded.")