import discord
from bot.models.movie import Movie

# === Channel-specific themes ===
CHANNEL_THEMES = {
    "watchlist": {
        "color": discord.Color.teal(),
        "prefix": "🎬 Watchlist: "
    },
    "currently-watching": {
        "color": discord.Color.orange(),
        "prefix": "👀 Watching: "
    },
    "downloaded": {
        "color": discord.Color.gold(),
        "prefix": "📥 Downloaded: "
    },
    "watched": {
        "color": discord.Color.from_rgb(255, 105, 180),  # Hot pink
        "prefix": "✅ Watched: "
    },
    "default": {
        "color": discord.Color.blue(),
        "prefix": ""
    }
}

def generate_movie_embed(movie: Movie, channel: str = "default") -> discord.Embed:
    theme = CHANNEL_THEMES.get(channel, CHANNEL_THEMES["default"])
    prefix = theme["prefix"]
    color = theme["color"]

    # Handle TV series title formatting
    title = movie.title
    if movie.type == "series":
        season = int(movie.season or 1)
        episode = int(movie.episode or 1)
        title = f"{title} (S{season:02}E{episode:02})"

    embed = discord.Embed(
        title=f"{prefix}{title}",
        color=color
    )

    if movie.poster and movie.poster != "N/A":
        embed.set_thumbnail(url=movie.poster)

    # Ordered, styled fields
    fields = [
        ("Genre", movie.genre),
        ("Year", movie.year),
        ("Watched At", movie.timestamp),
        ("File Path", movie.filepath),
        ("IMDb", movie.imdb_url)
    ]

    for name, value in fields:
        if value:
            inline = name not in ["File Path", "IMDb"]
            embed.add_field(name=name, value=value, inline=inline)

    return embed