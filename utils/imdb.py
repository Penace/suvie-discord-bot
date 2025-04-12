import os
import requests
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

def fetch_movie_data(imdb_id: str = None, title: str = None) -> dict:
    if not OMDB_API_KEY:
        raise EnvironmentError("OMDB_API_KEY is not set in the .env file.")

    base_url = "http://www.omdbapi.com/"
    params = {"apikey": OMDB_API_KEY}

    if imdb_id:
        params["i"] = imdb_id
    elif title:
        params["t"] = title
    else:
        raise ValueError("Either imdb_id or title must be provided.")

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise ConnectionError(f"OMDb API error: {response.status_code}")

    data = response.json()
    if data.get("Response") != "True":
        raise ValueError(data.get("Error", "Movie not found."))

    # Return a simplified dictionary with only what you need
    return {
        "title": data.get("Title"),
        "year": data.get("Year"),
        "genre": data.get("Genre"),
        "plot": data.get("Plot"),
        "poster": data.get("Poster"),
        "imdb_url": f"https://www.imdb.com/title/{data.get('imdbID')}",
        "imdb_id": data.get("imdbID"),
        "trailer": None  # Placeholder for future YouTube scraping or linking
    }