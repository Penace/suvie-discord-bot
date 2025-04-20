# 🛠️ Local Development – Suvie Bot

This guide will help you set up Suvie Bot on your local machine for testing or development.

---

## 🔧 Requirements

- Python 3.11+
- Discord Developer Account + Bot Token
- OMDb API Key (https://www.omdbapi.com/)
- `git`, `pip`, and virtualenv

---

## 🚀 Getting Started

### 1. Clone the Repository
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

### 3. Create .env File
Inside the root of the repo:
```bash
cp .env.example .env
```

### 4. Run the Bot
```bash
./start.sh
```

---

## 📁 Structure
```bash
suvie-bot/
├── bot/              # Core command logic & cogs
├── utils/            # Helper modules (IMDB, storage, database)
├── backups/          # JSON backup files (auto-saved)
├── frontend/         # suvie.me landing site (optional)
├── backend/          # Flask API (optional/future)
├── docs/             # Project documentation
├── .env.example      # Example environment variables
├── requirements.txt  # Dependencies
├── start.sh          # Startup script (optional)
└── README.md
```

---

## ✅ Extra Notes
•	Commands are located in bot/commands/ and auto-registered at startup.
•	The bot uses JSON for storage (easily upgradeable later).
•	Backups are saved after every change (in backups/json/).
•	You can reload commands live with the /reload slash command.

---

Need help? See SUPPORT.md
