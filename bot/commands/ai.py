import os
import re
import discord
from discord.ext import commands
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional, Union
from openai.types.chat import ChatCompletionMessageParam

from utils.storage import get_or_create_text_channel  # ✅ Channel auto-creation

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AICompanionCog(commands.Cog):
    """suvie: Your Discord AI Companion."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel_name = "suvie-ai"
        self.memory: dict[int, list[ChatCompletionMessageParam]] = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            await get_or_create_text_channel(self.bot, guild, self.channel_name)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not isinstance(message.channel, discord.TextChannel):
            return

        if message.channel.name != self.channel_name:
            return

        guild_id = message.guild.id if message.guild else 0
        user_input = message.content.strip()
        if not user_input:
            return

        # Init memory for this guild+user combo
        self.memory.setdefault(guild_id, {})
        self.memory[guild_id].setdefault(message.author.id, [])
        convo = self.memory[guild_id][message.author.id]

        convo.append({"role": "user", "content": user_input})
        convo[:] = convo[-5:]

        detected = self.detect_command(user_input)
        if detected:
            await message.channel.send(f"🛠️ Detected command: `{detected['action']}` → **{detected['title']}**")
            return

        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": (
                    "You are suvie, a helpful and warm AI companion on Discord.\n"
                    "Speak casually, like a close friend. Avoid robotic language.\n"
                    "You love movies and TV shows. Be immersive, playful, and personal.\n"
                    "Use memory of recent context.\n"
                    "Only reply in character and stay on-topic."
                )
            }
        ] + convo

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=110,
                temperature=0.7,
                top_p=1.0,
            )

            reply_raw = response.choices[0].message.content
            reply = reply_raw.strip() if reply_raw else "🤖 (No response)"

            convo.append({"role": "assistant", "content": reply})
            convo[:] = convo[-5:]

            await message.channel.send(reply)

        except Exception as e:
            print(f"[Suvie AI Error] {type(e).__name__}: {e}")
            await message.channel.send("⚠️ Suvie had a brain freeze.")

    def detect_command(self, message: str) -> Optional[dict]:
        lowered = message.lower()

        command_keywords = {
            "add": ["add", "put", "include", "insert"],
            "remove": ["remove", "delete", "take out"],
            "watch": ["watch", "start watching", "set currently watching"],
            "download": ["download", "get", "save"],
        }

        for action, keywords in command_keywords.items():
            if any(kw in lowered for kw in keywords):
                match = re.search(r"(?:\"|')?([a-zA-Z0-9:!\-\s]+)(?:\"|')?", lowered)
                if match:
                    return {
                        "action": action,
                        "title": match.group(1).strip(),
                    }

        return None

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(AICompanionCog(bot))
    print("🤖 Suvie AI Companion loaded.")