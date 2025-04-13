# 🧠 Suvie Bot — Full Slash Command Reference

This document provides a detailed list of all available slash commands in **Suvie**, categorized by function.

---

## 📺 Watchlist

| Command                     | Description                                 |
|----------------------------|---------------------------------------------|
| `/watchlist add`           | Add a movie or TV show to the watchlist     |
| `/watchlist remove`        | Remove a title from the watchlist           |
| `/watchlist view`          | View all titles currently in your watchlist |
| `/watchlist clear`         | Clear the entire watchlist                  |

---

## 🎞️ Currently Watching

| Command                          | Description                                                 |
|----------------------------------|-------------------------------------------------------------|
| `/currentlywatching set`        | Mark a title as currently watching                          |
| `/currentlywatching update`     | Update season, episode, timestamp, or file path             |
| `/currentlywatching next`       | Advance to the next episode of a show                       |
| `/currentlywatching remove`     | Remove a title from currently watching                      |
| `/currentlywatching view`       | View all currently watching entries                         |
| `/currentlywatching repair`     | Auto-repair missing or malformed data in your movie list    |

---

## 📥 Downloaded

| Command                   | Description                                |
|---------------------------|--------------------------------------------|
| `/downloaded add`        | Mark a movie or show as downloaded         |
| `/downloaded edit`       | Edit a downloaded entry's file path        |
| `/downloaded remove`     | Remove a downloaded entry                  |

---

## ✅ Watched

| Command           | Description               |
|------------------|---------------------------|
| `/watched`       | (Coming soon) View archive|

---

## ⚙️ System Commands

| Command         | Description                               |
|----------------|-------------------------------------------|
| `/status`      | Show bot statistics and status info       |
| `/reload`      | Reload bot commands without restarting    |

---

## 💾 Backup & Auto-Sync

- Auto backups are performed every time your list changes
- Latest 5 backups stored in `backups/json/`
