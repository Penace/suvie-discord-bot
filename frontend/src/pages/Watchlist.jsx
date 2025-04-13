import React, { useEffect, useState } from "react";
import MovieCard from "../components/MovieCard";

export default function Watchlist() {
  const [watchlist, setWatchlist] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/movies")
      .then((res) => res.json())
      .then((data) => {
        const active = data.filter((m) => m.status === "watchlist");
        setWatchlist(active);
      })
      .catch((err) => console.error("Failed to load movies.json", err));
  }, []);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-pink-400 mb-2">📺 Watchlist</h2>
      {watchlist.length === 0 ? (
        <p className="text-gray-400">Your watchlist is currently empty.</p>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {watchlist.map((movie, idx) => (
            <MovieCard key={idx} movie={movie} />
          ))}
        </div>
      )}
    </div>
  );
}
