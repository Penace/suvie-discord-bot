import discord
from discord.ext import commands
from discord import app_commands
import json
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile
from sqlalchemy.orm import Session

from models.movie import Movie
from bot.utils.database import engine


class BackupCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="backup", description="Create and download a full Suvie backup.")
    async def backup_now(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild_id

        if guild_id is None:
            await interaction.followup.send("❌ This command must be used in a server.", ephemeral=True)
            return

        # === Export movie data from DB ===
        with Session(engine) as session:
            movies = session.query(Movie).filter_by(guild_id=guild_id).all()
            data = [m.to_dict() for m in movies]

        # === Create temp .json file ===
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_dir = Path("temp_backups")
        temp_dir.mkdir(exist_ok=True)
        json_path = temp_dir / f"suvie_backup_{guild_id}_{timestamp}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        # === Zip it ===
        zip_path = temp_dir / f"suvie_backup_{guild_id}_{timestamp}.zip"
        with ZipFile(zip_path, "w") as zipf:
            zipf.write(json_path, arcname=json_path.name)

        # === Cleanup json after zipping ===
        json_path.unlink()

        # === Upload to Discord ===
        file = discord.File(fp=zip_path, filename=zip_path.name)
        await interaction.followup.send(content="📦 Here is your latest backup:", file=file, ephemeral=True)

        # === Optional cleanup ===
        zip_path.unlink()

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(BackupCog(bot))
    print("💾 Backup command loaded.")