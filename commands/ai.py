import os
import re
import discord
from discord.ext import commands
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AICompanionCog(commands.Cog):
    """suvie: Your Discord AI Companion."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel_name = "suvie-ai"  # Suvie only responds in this channel
        self.memory = {}  # Per-user short-term memory

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore bot messages or messages not in the target channel
        if message.author.bot or message.channel.name != self.channel_name:
            return

        user_input = message.content.strip()
        if not user_input:
            return

        user_id = str(message.author.id)
        self.memory.setdefault(user_id, [])
        self.memory[user_id].append({"role": "user", "content": user_input})
        self.memory[user_id] = self.memory[user_id][-5:]  # Retain only last 5 entries
        
        # Detect command intent
        detected_command = self.detect_command(user_input)
        if detected_command:
            await message.channel.send(f"🛠️ Detected command: `{detected_command['action']}` → **{detected_command['title']}**")
            return

        # Define Suvie’s tone and personality
        system_prompt = {
            "role": "system",
            "content": (
                "You are suvie, a helpful and warm AI companion on Discord.\n"
                "Speak casually, like a close friend. Avoid robotic language.\n"
                "You love movies and TV shows. Be immersive, playful, and personal.\n"
                "Use memory of recent context."
            )
        }

        messages = [system_prompt] + self.memory[user_id]

        try:
            # Request a chat completion from OpenAI
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=110,
                temperature=0.7,
                top_p=1.0,
                n=1,
                stop=None,
            )

            reply = response.choices[0].message.content.strip()

            # Track Suvie’s response
            self.memory[user_id].append({"role": "assistant", "content": reply})
            self.memory[user_id] = self.memory[user_id][-5:]

            await message.channel.send(reply)

        except Exception as e:
            print(f"[Suvie AI Error] {type(e).__name__}: {e}")
            await message.channel.send("⚠️ Suvie had a brain freeze.")
            
    def detect_command(self, message: str) -> dict | None:
        """Detects if the message is a command and returns its details."""
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

# Cog registration
async def setup(bot: commands.Bot):
    await bot.add_cog(AICompanionCog(bot))
    print("🤖 Suvie AI Companion loaded.")