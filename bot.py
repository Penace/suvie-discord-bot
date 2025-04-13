import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI
from typing import Optional, cast

load_dotenv()

# === API KEYS ===
OPENAI_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN: Optional[str] = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    raise EnvironmentError("DISCORD_TOKEN is not set in the .env file.")
if not OPENAI_KEY:
    raise EnvironmentError("OPENAI_API_KEY is not set in the .env file.")

# === OpenAI Init ===
client = OpenAI(api_key=OPENAI_KEY)

# === Discord Intents ===
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# === Bot Setup ===
bot: commands.Bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

# === Ready Event ===
@bot.event
async def on_ready():
    if bot.user:
        print(f"✅ Suvie is online as {bot.user} (ID: {bot.user.id})")
    else:
        print("⚠️ Bot user not available yet.")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Failed to sync commands: {type(e).__name__}: {e}")

# === Load Cogs ===
async def load_cogs():
    command_dir = "./commands"
    for filename in os.listdir(command_dir):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            try:
                await bot.load_extension(f"commands.{module_name}")
                print(f"📁 Loaded cog: {module_name}")
            except Exception as e:
                print(f"⚠️ Failed to load {module_name}: {type(e).__name__}: {e}")

# === Main Runner ===
async def main():
    await load_cogs()
    await bot.start(cast(str, DISCORD_TOKEN))

if __name__ == "__main__":
    try:
        # Fix for Windows event loop policy
        if os.name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Shutting down...")
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")