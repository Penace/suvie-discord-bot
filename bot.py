import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise EnvironmentError("DISCORD_TOKEN is not set in the .env file.")

# === Setup Intents ===
intents = discord.Intents.default()
intents.message_content = True  # REQUIRED for reading chat
intents.guilds = True
intents.members = True

# === Create Bot ===
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

# === On Ready ===
@bot.event
async def on_ready():
    print(f"✅ Suvie is online as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

# === Load Cogs ===
async def load_cogs():
    for file in os.listdir("./commands"):
        if file.endswith(".py"):
            name = file[:-3]
            try:
                await bot.load_extension(f"commands.{name}")
                print(f"📁 Loaded cog: {name}")
            except Exception as e:
                print(f"⚠️ Failed to load {name}: {type(e).__name__}: {e}")

# === Run Bot ===
async def main():
    await load_cogs()
    await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Shutting down...")
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")