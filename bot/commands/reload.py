import discord
from discord.ext import commands
from discord import app_commands
from pathlib import Path

class ReloadCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="reload", description="Reload or load a cog dynamically.")
    @app_commands.describe(target="Name of the cog to reload or 'all' for everything.")
    async def reload(self, interaction: discord.Interaction, target: str):
        await interaction.response.defer(ephemeral=True)

        path = Path("commands")
        available = [f.stem for f in path.glob("*.py") if not f.stem.startswith("__")]

        if target.lower() == "all":
            reloaded, loaded = [], []
            for cog in available:
                full_path = f"commands.{cog}"
                try:
                    await self.bot.reload_extension(full_path)
                    reloaded.append(cog)
                except commands.ExtensionNotLoaded:
                    await self.bot.load_extension(full_path)
                    loaded.append(cog)

            embed = discord.Embed(title="🔁 All Cogs Reloaded", color=discord.Color.blurple())
            embed.add_field(name="Reloaded", value=", ".join(reloaded) or "None", inline=False)
            embed.add_field(name="Loaded", value=", ".join(loaded) or "None", inline=False)
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        if target in available:
            full_path = f"commands.{target}"
            try:
                await self.bot.reload_extension(full_path)
                status = "🔄 Reloaded"
            except commands.ExtensionNotLoaded:
                await self.bot.load_extension(full_path)
                status = "✅ Loaded"

            embed = discord.Embed(
                title=f"{status} `{target}`",
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send(f"❌ Cog `{target}` not found.", ephemeral=True)

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(ReloadCog(bot))
    print("📁 Reload command loaded.")