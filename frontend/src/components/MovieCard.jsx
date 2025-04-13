import React from 'react'

export default function MovieCard({ movie }) {
  const isSeries = movie.type === 'series'

  return (
    <div className="bg-zinc-900 rounded-xl shadow hover:shadow-lg transition p-4 border border-zinc-800">
      <div className="flex gap-4">
        {movie.poster && movie.poster !== 'N/A' && (
          <img
            src={movie.poster}
            alt={movie.title}
            className="w-24 h-36 object-cover rounded"
          />
        )}
        <div className="flex flex-col justify-between flex-1">
          <div>
            <h3 className="text-lg font-bold text-white">{movie.title}</h3>
            <p className="text-sm text-pink-300">{movie.year || 'N/A'} • {movie.genre || 'Unknown'}</p>
            <p className="text-sm text-gray-400 italic mt-1">{movie.plot?.slice(0, 100)}...</p>
          </div>
          {isSeries && (
            <p className="text-sm text-cyan-300 mt-2">📺 Season {movie.season || 1}, Episode {movie.episode || 1}</p>
          )}
        </div>
      </div>
    </div>
  )
}
