import discord
from discord.ext import commands
from discord import app_commands
from pathlib import Path
import platform
import psutil
from datetime import datetime
from bot.utils.database import SessionLocal
from bot.models.movie import Movie

ALLOWED_DEV_IDS = [249144051402670081]  # Replace with your Discord user ID

class DevCog(commands.GroupCog, name="dev"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = datetime.now()

    def get_uptime(self) -> str:
        return str(datetime.now() - self.start_time).split(".")[0]

    def get_total_movies(self) -> int:
        try:
            with SessionLocal() as session:
                return session.query(Movie).count()
        except Exception as e:
            print(f"[Dev DB Error] {type(e).__name__}: {e}")
            return -1

    def is_dev(self, user_id: int) -> bool:
        return user_id in ALLOWED_DEV_IDS

    @app_commands.command(name="status", description="View detailed dev system status.")
    async def dev_status(self, interaction: discord.Interaction):
        if not self.is_dev(interaction.user.id):
            await interaction.response.send_message("❌ You are not authorized to use this command.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        process = psutil.Process()
        mem_usage = process.memory_info().rss / 1024**2
        cpu_percent = psutil.cpu_percent(interval=1)
        total_movies = self.get_total_movies()

        embed = discord.Embed(
            title="🧪 Suvie Developer Status",
            description="Internal diagnostics and metrics.",
            color=discord.Color.fuchsia()
        )
        embed.add_field(name="⏳ Uptime", value=self.get_uptime(), inline=True)
        embed.add_field(name="🧠 Memory Usage", value=f"{mem_usage:.2f} MB", inline=True)
        embed.add_field(name="🖥️ CPU Usage", value=f"{cpu_percent:.1f}%", inline=True)
        embed.add_field(name="🎞️ Movies Tracked", value=str(total_movies), inline=True)
        embed.add_field(name="⚙️ Cogs Loaded", value=str(len(self.bot.cogs)), inline=True)
        embed.add_field(name="📜 Commands Registered", value=str(len(self.bot.tree.get_commands())), inline=True)
        embed.add_field(name="📂 Platform", value=f"{platform.system()} {platform.release()}", inline=True)
        embed.set_footer(text="Only visible to bot developers.")

        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="reload", description="Reload or load a cog dynamically.")
    @app_commands.describe(target="Name of the cog to reload, or 'all' for everything.")
    async def reload(self, interaction: discord.Interaction, target: str):
        if not self.is_dev(interaction.user.id):
            await interaction.response.send_message("❌ You are not authorized to use this command.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        path = Path("bot/commands")
        if not path.exists():
            await interaction.followup.send("❌ The `bot/commands/` folder does not exist.", ephemeral=True)
            return

        available = [f.stem for f in path.glob("*.py") if not f.stem.startswith("__")]
        target = target.lower()

        if target == "all":
            reloaded, loaded, failed = [], [], []
            for cog in available:
                full_path = f"bot.commands.{cog}"
                try:
                    await self.bot.reload_extension(full_path)
                    reloaded.append(cog)
                except commands.ExtensionNotLoaded:
                    try:
                        await self.bot.load_extension(full_path)
                        loaded.append(cog)
                    except Exception as e:
                        failed.append(f"{cog} ❌ ({type(e).__name__})")
                        print(f"[Reload] ❌ Failed to load {cog}: {e}")
                except Exception as e:
                    failed.append(f"{cog} ❌ ({type(e).__name__})")
                    print(f"[Reload] ❌ Failed to reload {cog}: {e}")

            embed = discord.Embed(title="🔁 Cogs Reload Summary", color=discord.Color.blurple())
            embed.add_field(name="Reloaded", value=", ".join(reloaded) or "None", inline=False)
            embed.add_field(name="Loaded", value=", ".join(loaded) or "None", inline=False)
            if failed:
                embed.add_field(name="Errors", value="\n".join(failed), inline=False)

            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        matches = [c for c in available if c.lower() == target]
        if matches:
            cog = matches[0]
            full_path = f"bot.commands.{cog}"
            try:
                await self.bot.reload_extension(full_path)
                status = "🔄 Reloaded"
            except commands.ExtensionNotLoaded:
                try:
                    await self.bot.load_extension(full_path)
                    status = "✅ Loaded"
                except Exception as e:
                    await interaction.followup.send(f"❌ Failed to load `{cog}`: {type(e).__name__}", ephemeral=True)
                    return

            embed = discord.Embed(title=f"{status} `{cog}`", color=discord.Color.green())
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send(f"❌ Cog `{target}` not found in `bot/commands/`.", ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(DevCog(bot))
    print("🛠️ Loaded cog: dev")
