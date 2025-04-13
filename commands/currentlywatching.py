import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

from utils.storage import (
    load_movies,
    save_movies,
    update_currently_watching_channel,
    get_currently_watching_movies,
    get_movie_by_title
)

class CurrentlyWatchingCog(commands.GroupCog, name="currentlywatching"):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    # === /currentlywatching set ===
    @app_commands.command(name="set", description="Set the currently watching title (movie or TV).")
    @app_commands.describe(
        title="The title you're watching.",
        imdb_id="The IMDb ID (optional).",
        season="Season number (for series)",
        episode="Episode number (for series)",
        timestamp="Time (e.g., 00:45:32)",
        filepath="Optional file path"
    )
    async def set(
        self, interaction: discord.Interaction,
        title: str = None, imdb_id: str = None,
        season: int = None, episode: int = None,
        timestamp: str = None, filepath: str = None
    ):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()

        matched = None
        if title:
            matched = next((m for m in movies if m.get("title", "").lower() == title.lower()), None)
        elif imdb_id:
            matched = next((m for m in movies if m.get("imdb_id") == imdb_id), None)

        if not matched:
            await interaction.followup.send("❌ Title not found in your library.", ephemeral=True)
            return

        matched["status"] = "currently-watching"
        if matched.get("type") in ("series", "tv"):
            matched["season"] = season or matched.get("season", 1)
            matched["episode"] = episode or matched.get("episode", 1)
        else:
            matched["type"] = "series"  # ← Fallback for when OMDb fails
            matched["season"] = season or 1
            matched["episode"] = episode or 1

        if timestamp:
            matched["timestamp"] = timestamp
        if filepath:
            matched["filepath"] = filepath

        save_movies(movies)
        await update_currently_watching_channel(interaction.client)

        suffix = f" (S{matched['season']:02}E{matched['episode']:02})" if matched.get("type") == "series" else ""
        await interaction.followup.send(f"🎬 Set **{matched['title']}{suffix}** as currently watching.", ephemeral=True)

    # === /currentlywatching update ===
    @app_commands.command(name="update", description="Update a currently watching movie or show.")
    @app_commands.describe(
        title="Title of the entry",
        season="New season (TV only)",
        episode="New episode (TV only)",
        timestamp="New timestamp (optional)",
        filepath="New file path (optional)"
    )
    async def update(self, interaction: discord.Interaction, title: str, season: int = None, episode: int = None, timestamp: str = None, filepath: str = None):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()
        match = next((m for m in movies if m.get("title", "").lower() == title.lower()), None)

        if not match:
            await interaction.followup.send("❌ Entry not found in your library.", ephemeral=True)
            return

        # Apply series-specific updates
        if match.get("type") == "series":
            if season:
                match["season"] = season
            if episode:
                match["episode"] = episode

        # Apply universal updates
        if timestamp:
            match["timestamp"] = timestamp
        if filepath:
            match["filepath"] = filepath

        match["status"] = "currently-watching"
        save_movies(movies)
        await update_currently_watching_channel(interaction.client)

        suffix = f" (S{match.get('season', 1):02}E{match.get('episode', 1):02})" if match.get("type") == "series" else ""
        await interaction.followup.send(f"🔁 Updated **{match['title']}{suffix}**.", ephemeral=True)         
  
    # === /currentlywatching next ===            
    @app_commands.command(name="next", description="Advance to the next episode of a show.")
    @app_commands.describe(title="Title of the show")
    async def next(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()
        match = next((m for m in movies if m.get("title", "").lower() == title.lower()), None)

        if not match:
            await interaction.followup.send("❌ Show not found.", ephemeral=True)
            return

        if match.get("type") not in ("series", "tv"):
            await interaction.followup.send("❌ This command only works on TV shows.", ephemeral=True)
            return

        match["episode"] = match.get("episode", 1) + 1
        match["status"] = "currently-watching"

        save_movies(movies)
        await update_currently_watching_channel(interaction.client)
        await interaction.followup.send(f"⏭️ Now watching **{title} S{match['season']:02}E{match['episode']:02}**", ephemeral=True)

    # === /currentlywatching view ===
    @app_commands.command(name="view", description="View all currently watching movies or shows.")
    async def view(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()
        currently_watching = [m for m in movies if m.get("status") == "currently-watching"]

        if not currently_watching:
            await interaction.followup.send("📭 You're not currently watching anything.", ephemeral=True)
            return

        for show in currently_watching:
            season = show.get("season")
            episode = show.get("episode")

            if season is not None and episode is not None:
                title = f"{show['title']} (S{int(season):02}E{int(episode):02})"
            else:
                title = show["title"]

            embed = discord.Embed(title=f"🎬 {title}", color=discord.Color.orange())
            if show.get("timestamp"):
                embed.add_field(name="Timestamp", value=show["timestamp"], inline=True)
            if show.get("filepath"):
                embed.add_field(name="File", value=show["filepath"], inline=False)
            if show.get("imdb_url"):
                embed.add_field(name="IMDb", value=show["imdb_url"], inline=False)
            if show.get("poster") and show["poster"] != "N/A":
                embed.set_thumbnail(url=show["poster"])
            await interaction.followup.send(embed=embed, ephemeral=True)
            
    # === /currentlywatching remove ===
    @app_commands.command(name="remove", description="Remove a title from your currently watching list.")
    @app_commands.describe(title="The title to remove")
    async def remove(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()

        updated = False
        for entry in movies:
            if entry.get("title", "").lower() == title.lower() and entry.get("status") == "currently-watching":
                entry["status"] = "watchlist"  # or "paused" if you want to add that later
                updated = True

        if not updated:
            await interaction.followup.send("❌ Title not found in your currently watching list.", ephemeral=True)
            return

        save_movies(movies)
        await update_currently_watching_channel(interaction.client)
        await interaction.followup.send(f"🗑️ Removed **{title}** from your currently watching list.", ephemeral=True)

    # === /currentlywatching repair ===
    @app_commands.command(name="repair", description="Repair malformed library entries (type, season, episode).")
    async def repair(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        movies = load_movies()
        fixes = 0
        logs = []

        for m in movies:
            title = m.get("title", "Untitled")
            changed = False

            # Fix type if missing or incorrect
            if m.get("season") or m.get("episode"):
                if m.get("type") != "series":
                    m["type"] = "series"
                    changed = True
                    logs.append(f"🔧 Fixed type for **{title}** → series")

            # Ensure type exists
            if not m.get("type"):
                m["type"] = "movie"
                changed = True
                logs.append(f"🔧 Defaulted type for **{title}** → movie")

            # Set season/episode if missing on series
            if m.get("type") == "series":
                if "season" not in m:
                    m["season"] = 1
                    changed = True
                    logs.append(f"🧩 Set missing season for **{title}** → 1")
                if "episode" not in m:
                    m["episode"] = 1
                    changed = True
                    logs.append(f"🧩 Set missing episode for **{title}** → 1")

            if changed:
                fixes += 1

        save_movies(movies)
        await update_currently_watching_channel(interaction.client)

        if fixes == 0:
            await interaction.followup.send("✅ Everything looks good. No repairs needed!", ephemeral=True)
        else:
            summary = f"✅ Repaired **{fixes}** entries.\n" + "\n".join(logs[:10])
            if fixes > 10:
                summary += f"\n...and {fixes - 10} more."
            await interaction.followup.send(summary, ephemeral=True)
        

# === Cog Loader ===
async def setup(bot: commands.Bot):
    await bot.add_cog(CurrentlyWatchingCog(bot))
    print("📺 Loaded cog: currentlywatching")