import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI
from typing import Optional, cast

# === Load .env ===
load_dotenv()

# === API Keys ===
DISCORD_TOKEN: Optional[str] = os.getenv("DISCORD_TOKEN")
OPENAI_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

if not DISCORD_TOKEN:
    raise EnvironmentError("DISCORD_TOKEN not set in .env file")
if not OPENAI_KEY:
    raise EnvironmentError("OPENAI_API_KEY not set in .env file")

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

# === on_ready Event ===
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
    # command_dir = os.path.join(os.path.dirname(__file__), "commands")
    # print(f"📂 Loading cogs from: {command_dir}")

    # for filename in os.listdir(command_dir):
    #     if filename.endswith(".py") and not filename.startswith("__"):
    #         module_name = filename[:-3]
    #         try:
    #             await bot.load_extension(f"commands.{module_name}")
    #         except Exception as e:
    #             print(f"⚠️ Failed to load {module_name}: {type(e).__name__}: {e}")
    await bot.load_extension("bot.commands.watchlist")

# === Main Entrypoint ===
async def main():
    await load_cogs()
    await bot.start(cast(str, DISCORD_TOKEN))

if __name__ == "__main__":
    try:
        if os.name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Shutdown requested. Exiting...")
    except Exception as e:
        print(f"❌ Fatal error: {type(e).__name__}: {e}")