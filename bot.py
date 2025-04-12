import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# 🔧 Load environment
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise EnvironmentError("DISCORD_TOKEN is not set in the .env file.")

# 🧠 Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")  # Optional: removes default help command

# 🌐 Sync and status
@bot.event
async def on_ready():
    print(f"✅ Suvie is online as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

# 📦 Load all command cogs
async def load_cogs():
    command_dir = "./commands"
    for filename in os.listdir(command_dir):
        if filename.endswith(".py"):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f"commands.{cog_name}")
                print(f"📁 Loaded cog: {cog_name}")
            except Exception as e:
                print(f"⚠️ Failed to load {cog_name}: {e}")

# 🚀 Launch bot
async def main():
    await load_cogs()
    await bot.start(TOKEN)

# ⏯️ Entrypoint
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 Gracefully shutting down...")
        asyncio.run(bot.close())
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        asyncio.run(bot.close())