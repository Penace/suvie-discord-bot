import discord
from discord.ext import commands
from discord import app_commands

class ReloadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reload", description="Reload bot cogs.")
    @app_commands.describe(
        cog="The name of the cog to reload (e.g., ping, addmovie, etc.). Use 'all' to reload all."
    )
    async def reload(self, interaction: discord.Interaction, cog: str):
        await interaction.response.defer(ephemeral=True)

        if cog.lower() == "all":
            reloaded = []
            for ext in self.bot.extensions:
                try:
                    await self.bot.reload_extension(ext)
                    reloaded.append(ext)
                except Exception as e:
                    await interaction.followup.send(f"❌ Failed to reload `{ext}`: `{e}`", ephemeral=True)
                    return
            await interaction.followup.send(
                f"🔁 Reloaded all cogs:\n" + "\n".join([f"✅ `{ext}`" for ext in reloaded]),
                ephemeral=True
            )
        else:
            cog_path = f"commands.{cog}"
            if cog_path in self.bot.extensions:
                try:
                    await self.bot.reload_extension(cog_path)
                    await interaction.followup.send(f"✅ Reloaded `{cog}` cog.", ephemeral=True)
                except Exception as e:
                    await interaction.followup.send(f"❌ Failed to reload `{cog}`: `{e}`", ephemeral=True)
            else:
                await interaction.followup.send(f"⚠️ Cog `{cog}` not found or not loaded.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ReloadCog(bot))