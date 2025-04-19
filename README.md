# 🎬 Suvie Bot

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.3.2-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![JSON](https://img.shields.io/badge/JSON%20Storage-Lightgrey?style=for-the-badge&logo=json&logoColor=black)
![Open Source](https://img.shields.io/badge/Open%20Source-MIT-green?style=for-the-badge)
[![Suvie Homepage](https://img.shields.io/badge/Visit-suvie.me-orange?style=for-the-badge)](https://suvie.me)
[![Support on Ko-fi](https://img.shields.io/badge/Support-Ko--fi-ff2d84?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/penace)
[![Built by Penace](https://img.shields.io/badge/Built%20by-Penace-4e5fff?style=for-the-badge)](https://penace.org)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/penace)

---

**Suvie** is a sleek, personal Discord bot for tracking your movies and shows.  
Add to your server to manage watchlists, currently watching, downloaded media, and more — all with rich embedded responses and JSON storage.

---

## ✨ Features

- 📺 **Watchlist Management** – Add, remove, view, and clear titles.
- 🎞️ **Currently Watching** – Track current show/movie with episode, time, and path.
- ✅ **Watched Archive** – Archive what you’ve finished for reference.
- 📥 **Downloaded List** – Log and manage local media and filepaths.
- 🔁 **Dynamic Reloading** – Reload commands without restarting the bot.
- 💾 **Auto Backups** – Changes saved with versioned JSON backups.
- 📊 **Bot Status** – Uptime, memory, loaded commands, and stats.

> All data is stored locally in `movies.json` — no database required.

---

## 🧠 Project Structure

```txt
suvie-bot/
├── bot/              # Core logic and command cogs
│   ├── commands/     # Slash command modules
│   └── utils/        # Storage, IMDB, backups
├── docs/             # Setup + command references
├── backups/          # Auto-saved JSON versions
├── assets/           # Logo & banner files
├── frontend/         # suvie.me (optional)
├── backend/          # API support (optional)
├── .env.example
├── requirements.txt
├── README.md
└── start.sh
```
---
## 🚀 Quick Start

### 1. Clone the Repo

```bash
git clone https://github.com/yourname/suvie-bot.git
cd suvie-bot
```
### 2. Create Virtual Environment

```bash
python3 -m venv suvie-env
source suvie-env/bin/activate
pip3 install -r requirements.txt
```

### 3. Set up Environment Variables

Create a .env file:
```bash
cp .env.example .env
```
Then insert your api keys into .env.

### 4. Run the Bot

```bash
./start.sh
```
Full setup guide: docs/SETUP.md

---

## 🧾 Slash Commands Overview
```text
Command Group       Subcommands
/watchlist          add, remove, view, clear
/currentlywatching  set, view, update, next, remove, repair
/downloaded         add, edit, remove, clear, view
/watched            add, edit, remove, view
/status             status, ping
/dev                for dev only. 
```
More: docs/COMMANDS.md

---

## 📌 Roadmap

### ✅ Version 3

```text
•	TV show support (season/episode)
•	Multi-entry currentlywatching
•	/repair command
•	Refactored UI embed system
```
### ⏭️ Version 4
```text
•	Fuzzy title matching
•	GUI frontend @ suvie.me
•	Slash command sync helper
•	Public SaaS-ready backend
```

---

## 💖 Support & Contribute
```text
If you like the project and want to support it:
```
[![Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/P5P51DOQ6D), [![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/penace)
```text
•	⭐ Star this repo
•	🛠️ Submit a PR or suggestion
```
See docs/SUPPORT.md for full contributor info.

---

## 🖤 Built by [![Penace](https://img.shields.io/badge/Built%20by-Penace-4e5fff?style=for-the-badge)](https://penace.org)

Open-source, cleanly engineered, obsessively polished.
This bot runs on caffeine, code, and the love of media.

“Watch smarter. Track smoother. Suvie.”
