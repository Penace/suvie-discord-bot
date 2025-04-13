# 🎬 Suvie Bot

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.3.2-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![OMDb API](https://img.shields.io/badge/OMDb-API-red?style=for-the-badge&logo=imdb&logoColor=white)
![JSON](https://img.shields.io/badge/JSON%20Storage-Lightgrey?style=for-the-badge&logo=json&logoColor=black)
![Markdown](https://img.shields.io/badge/Markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white)

[![Built by Penace](https://img.shields.io/badge/Built%20by-Penace-blueviolet?style=for-the-badge)](https://penace.org)
[![Suvie Homepage](https://img.shields.io/badge/View%20Live-suvie.me-orange?style=for-the-badge)](https://suvie.me)

---

**Suvie** is a personal movie and TV show companion Discord bot for managing watchlists, tracking viewing progress, and organizing your media experience with style.

---

## ✨ Features

- 📺 **Watchlist Management** – Add, remove, view, and clear your watchlist with rich movie embeds.
- 🎞️ **Currently Watching** – Track your current show or movie, including season/episode, timestamp, and filepath.
- ✅ **Watched Archive** – Archive watched titles and preserve your history.
- 📥 **Downloaded List** – Mark entries as downloaded and manage their filepaths.
- 🔁 **Dynamic Reloading** – Reload commands without restarting the bot.
- 💾 **Auto Backups** – Every change is backed up (last 5 versions preserved).
- 📊 **Bot Status** – Monitor stats, uptime, and loaded features.

---

## 🧠 Project Structure

```txt
suvie-bot/
├── commands/
│   ├── addmovie.py
│   ├── currentlywatching.py
│   ├── downloaded.py
│   ├── ping.py
│   ├── reload.py
│   ├── removemovie.py
│   ├── status.py
│   ├── watched.py
│   └── watchlist.py
├── utils/
│   ├── imdb.py
│   └── storage.py
├── backups/
│   └── json/
├── suvie.png
├── suviebanner.png
├── movies.json
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Run

### 1. Clone & Install
```bash
git clone https://github.com/yourname/suvie-bot.git
cd suvie-bot
python3 -m venv suvie-env
source suvie-env/bin/activate
pip install -r requirements.txt
```

### 2. Create a `.env` file with:
```env
DISCORD_TOKEN=your_token_here
OMDB_API_KEY=your_omdb_key_here
```

### 3. Run the bot
```bash
python3 bot.py
```

---

## 🛠️ Slash Commands

| Group | Command                      | Description                            |
|-------|------------------------------|----------------------------------------|
| 📺 `/watchlist`       | `add`, `remove`, `view`, `clear`           | Manage your watchlist                 |
| 🎞️ `/currentlywatching` | `set`, `view`, `update`, `next`, `remove`, `repair` | Track current viewing progress       |
| 📥 `/downloaded`      | `add`, `edit`, `remove`                     | Manage downloaded items               |
| ✅ `/watched`         | *(tbd)*                                     | Archive watched content               |
| ⚙️ `/status`          | —                                          | Bot status & stats                    |
| 🔁 `/reload`          | —                                          | Reload all commands live              |

👉 Full details: [docs/commands.md](docs/commands.md)

---

## 📌 Roadmap

### ✅ Version 3
- TV show support (season + episode)
- `/repair` command for malformed entries
- Multi-entry support in `currently-watching`
- Polished embedded UI and command layout

### ⏭️ Version 4
- 🔎 Comprehensive fuzzy matching
- ⚙️ CI/CD with GitHub Actions
- 🌐 GUI frontend hosted at `suvie.me`
- 🌍 Public open-source & deployable version

---

## 🧾 .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]

# Environments
suvie-env/
.env

# macOS
.DS_Store

# Backups & Data
backups/json/
*.zip
*.log
movies.json

# IDEs
.vscode/
.idea/
*.sublime-*

# Media / future
*.db
*.mp4
*.mkv
```

---

## 🖤 Made with love, hot pink, and precision.
