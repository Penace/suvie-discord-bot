# 🎬 Suvie Bot

**Suvie** is a custom-built personal movie companion Discord bot designed for private watchlists, shared viewing, file tracking, and seamless logging of everything you watch.

---

## ✨ Features

- 📺 **Watchlist Management** – Add, remove, view, and clear your watchlist with rich movie embeds.
- 🎞️ **Currently Watching** – Set and track your current movie + timestamp and filepath.
- ✅ **Watched Archive** – Log watched movies with timestamps and organize into a permanent archive.
- 📥 **Downloaded List** – Mark movies as downloaded, edit filepaths, or remove from queue.
- 📊 **Bot Status** – Shows current uptime, system stats, cogs loaded, movie count, and more.
- 🔁 **Dynamic Reloading** – Instantly load or reload any command without restarting the bot.
- 💾 **Auto Backups** – Every movie update is backed up with only the latest 5 stored.

---

## 🧠 Project Structure

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
│   └── json/…
├── suvie.png
├── suviebanner.png
├── movies.json
├── requirements.txt
└── README.md

---

## 🚀 Setup & Run

1.	**Clone & Install**
	```bash
	git clone https://github.com/yourname/suvie-bot.git
	cd suvie-bot
	python3 -m venv suvie-env
	source suvie-env/bin/activate
	pip install -r requirements.txt```

2.	**Create a .env file with:**
	DISCORD_TOKEN=your_token_here
	OMDB_API_KEY=your_omdb_key_here

3.	**Run the bot**
	python3 bot.py
	
4.	Invite it to your server with correct permissions (Read/Send/Manage Messages + Slash Commands).

---

## 🛠️ Slash Commands

	•/watchlist add
	•/watchlist remove
	•/watchlist view
	•/watchlist clear
	•/currentlywatching set
	•/currentlywatching view
	•/downloaded add/edit/remove
	•/watched
	•/status
	•/reload
	
## 🧪 Planned for V3
	•🎞️ TV show support (seasons, episodes, tracking)
	•🧠 AI assistant or chat integration (Model Context Protocol)
	•⚡ Autocompletion & interaction UIs
	•🗂️ GUI dashboard or web-based sync
	
## 🖤 Made with love, hot pink, and precision.

---

## 🧾 `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo

# Environments
suvie-env/
.env

# System
.DS_Store
Thumbs.db

# Backups
backups/json/
*.zip

# Logs
*.log

# IDE
.vscode/
.idea/
*.sublime-project
*.sublime-workspace

# Database / Media (if added later)
*.db
*.sqlite
*.mp4
*.mkv```