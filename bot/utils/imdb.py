import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
from typing import Optional, Dict
from dotenv import load_dotenv

from bot.models.movie import Movie

load_dotenv()

OMDB_API_KEY: Optional[str] = os.getenv("OMDB_API_KEY")


def fetch_movie_data(imdb_id: Optional[str] = None, title: Optional[str] = None) -> Dict[str, Optional[str]]:
    if not OMDB_API_KEY:
        raise EnvironmentError("OMDB_API_KEY is not set in the .env file.")

    if not imdb_id and not title:
        raise ValueError("Either imdb_id or title must be provided.")

    base_url = "http://www.omdbapi.com/"
    params: Dict[str, str] = {"apikey": OMDB_API_KEY}

    if imdb_id:
        params["i"] = imdb_id
    else:
        params["t"] = title.strip()

    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"❌ OMDb API request failed: {e}")

    data = response.json()
    if data.get("Response") != "True":
        raise ValueError(f"❌ OMDb Error: {data.get('Error', 'Movie not found.')}")

    return {
        "title": data.get("Title"),
        "year": data.get("Year"),
        "genre": data.get("Genre"),
        "plot": data.get("Plot"),
        "poster": data.get("Poster"),
        "imdb_url": f"https://www.imdb.com/title/{data.get('imdbID')}" if data.get("imdbID") else None,
        "imdb_id": data.get("imdbID"),
        "imdb_rating": data.get("imdbRating"),
        "director": data.get("Director"),
        "actors": data.get("Actors"),
        "type": data.get("Type", "movie").lower(),
        "trailer": None  # 📺 Placeholder for future trailer fetching
    }


# ✅ NEW: Return a Movie model instance directly
def fetch_movie_model(
    imdb_id: Optional[str] = None,
    title: Optional[str] = None,
    guild_id: Optional[int] = None,
    status: str = "watchlist",
    season: Optional[int] = None,
    episode: Optional[int] = None,
    filepath: Optional[str] = None
) -> Movie:
    data = fetch_movie_data(imdb_id=imdb_id, title=title)

    return Movie(
        guild_id=guild_id or 0,
        title=data.get("title"),
        year=data.get("year"),
        genre=data.get("genre"),
        plot=data.get("plot"),
        poster=data.get("poster"),
        imdb_url=data.get("imdb_url"),
        imdb_id=data.get("imdb_id"),
        imdb_rating=data.get("imdb_rating"),
        director=data.get("director"),
        actors=data.get("actors"),
        type=data.get("type", "movie"),
        season=season if data.get("type") == "series" else None,
        episode=episode if data.get("type") == "series" else None,
        timestamp=None,
        filepath=filepath,
        status=status
    )