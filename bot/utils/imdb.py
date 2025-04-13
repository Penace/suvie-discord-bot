import os
import requests
from typing import Optional, Dict
from dotenv import load_dotenv

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