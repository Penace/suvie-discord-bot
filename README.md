# 🎬 Suvie Bot

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.3.2-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![OMDb API](https://img.shields.io/badge/OMDb-API-red?style=for-the-badge&logo=imdb&logoColor=white)
![JSON](https://img.shields.io/badge/JSON%20Storage-Lightgrey?style=for-the-badge&logo=json&logoColor=black)
![Markdown](https://img.shields.io/badge/Markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white)

[![Built by Penace](https://img.shields.io/badge/Built%20by-Penace-blueviolet?style=for-the-badge)](https://penace.org)
[![Suvie Homepage](https://img.shields.io/badge/View%20Live-suvie.me-orange?style=for-the-badge)](https://suvie.me)

---

**Suvie** is a stylish and intuitive Discord bot for managing your movie and TV show experiences. With seamless watchlist tracking, AI conversations, and organized embeds, it's your personal viewing companion.

---

## ✨ Features

- 📺 **Watchlist Management** – Add, remove, view, and clear movies with season/episode support.
- 🎞️ **Currently Watching** – Track what's being watched, with S/E, file path, and timestamp.
- ✅ **Watched Archive** – Keep a permanent record of completed media.
- 📥 **Downloaded Tracker** – Manage and label downloaded files.
- 💬 **Suvie AI** – Casual conversation and smart interaction in a dedicated channel.
- 🔁 **Live Cog Reloading** – Reload modules without restarting.
- 💾 **Auto Backup** – Movie history is stored in JSON backups.
- 📊 **Bot Status Panel** – Get real-time stats in `#suvie-status`.

---

## 🧠 Directory Structure

```txt
suvie-bot/
├── bot/
│   ├── bot.py
│   ├── commands/
│   │   ├── ai.py
│   │   ├── backup.py
│   │   ├── currentlywatching.py
│   │   ├── dev.py
│   │   ├── downloaded.py
│   │   ├── initserver.py
│   │   ├── status.py
│   │   ├── watched.py
│   │   └── watchlist.py
│   ├── models/
│   │   └── movie.py
│   ├── utils/
│   │   ├── database.py
│   │   ├── imdb.py
│   │   ├── storage.py
│   │   └── ui.py
├── backups/
│   └── json/
├── docs/
│   └── commands.md
├── create_tables.py
├── requirements.txt
└── README.md
```

---

## 🚀 Quickstart

### 1. Setup
```bash
git clone https://github.com/yourname/suvie-bot.git
cd suvie-bot
python3 -m venv suvie-env
source suvie-env/bin/activate
pip install -r requirements.txt
```

### 2. Configure
Create a `.env` file:
```env
DISCORD_TOKEN=your_token_here
OMDB_API_KEY=your_omdb_key_here
```

### 3. Launch
```bash
python3 bot/bot.py
```

---

## 🛠️ Slash Command Overview

| Group | Command Set | Description |
|-------|-------------|-------------|
| `/watchlist` | add, remove, view, clear | Manage entries to be watched |
| `/currentlywatching` | set, update, next, view, remove | Live show/movie tracking |
| `/downloaded` | add, edit, remove, view, clear | Track downloaded files |
| `/watched` | mark as watched (archive) | Record viewing history |
| `/status` | summary panel | Bot diagnostics |
| `/dev` | reload, sync | Admin-only tools |
| `#suvie-ai` | natural conversation | Chat with your bot companion |

---

## 📌 Roadmap

### ✅ Current Goals
- Fully themed rich embeds
- Synced channel display updates
- Suvie AI single-response fix

### ⏭️ Next Steps
- 🔎 Fuzzy matching for all commands
- 🌍 Public launch + frontend at `suvie.me`
- 🧪 CI/CD + test coverage
- 💸 Monetization prep for freemium open-source

---

## 🖤 Made with hot pink, care, and caffeine.

> Designed & built by [penace.org](https://penace.org) • [suvie.me](https://suvie.me)

---

> For updates, issues, and deployment notes, see [docs/commands.md](docs/commands.md)
