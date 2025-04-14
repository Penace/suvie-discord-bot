import discord
from discord.ext import commands
from discord import app_commands
from pathlib import Path

class ReloadCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="reload", description="Reload or load a cog dynamically.")
    @app_commands.describe(target="Name of the cog to reload, or 'all' for everything.")
    async def reload(self, interaction: discord.Interaction, target: str):
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
                full_path = f"bot/commands.{cog}"
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

        # Targeted reload
        matches = [c for c in available if c.lower() == target]
        if matches:
            cog = matches[0]
            full_path = f"bot/commands.{cog}"
            try:
                await self.bot.reload_extension(full_path)
                status = "🔄 Reloaded"
            except commands.ExtensionNotLoaded:
                try:
                    await self.bot.load_extension(full_path)
                    status = "✅ Loaded"
                except Exception as e:
                    await interaction.followup.send(f"❌ Failed to load `{cog}`: {type(e).__name__}", ephemeral=True)
                    print(f"[Reload] ❌ {type(e).__name__}: {e}")
                    return

            embed = discord.Embed(
                title=f"{status} `{cog}`",
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send(f"❌ Cog `{target}` not found in `bot/commands/`.", ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(ReloadCog(bot))
    print("♻️ Reload command loaded.")