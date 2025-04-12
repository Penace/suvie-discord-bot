├── bot.py                  # ✅ Bot entry point
├── requirements.txt        # ✅ Python dependencies
├── .env                    # ✅ Environment variables (including token, keys)
├── movies.json             # ✅ Movie database
├── utils/
│   ├── imdb.py             # 🔍 IMDb/OMDb fetching logic
│   └── storage.py          # 💾 Save/load logic for all states
├── commands/
│   ├── addmovie.py         # ➕ Add to watchlist
│   ├── removemovie.py      # ➖ Remove from watchlist
│   ├── currentlywatching.py# 🎬 Track current movie
│   ├── watchlist.py        # 📜 View watchlist
│   ├── downloaded.py       # 📂 View/downloaded movies
│   └── reload.py           # 🔄 Reload cogs
