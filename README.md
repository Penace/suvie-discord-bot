[![Suvie Homepage](https://img.shields.io/badge/Visit-suvie.me-orange?style=for-the-badge)](https://suvie.me)
[![Support on Ko-fi](https://img.shields.io/badge/Support-Ko--fi-ff2d84?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/penace)
[![Built by Penace](https://img.shields.io/badge/Built%20by-Penace-4e5fff?style=for-the-badge)](https://penace.org)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/penace)

# 🌐 suvie.me – Frontend

This is the frontend source code for [suvie](https://suvie.me) — your cozy AI movie companion built for Discord.

> 🚀 Deployed live to [suvie.me](https://suvie.me) via GitHub Pages  
> 📦 Auto-deploy via GitHub Actions from `/frontend/dist`

- [📖 Full Command List](./COMMANDS.md)
- [🛣️ Roadmap](./ROADMAP.md)
- [💖 Support](./SUPPORT.md)
- [📁 Setup](./SETUP.md)

---

## ✨ Features

- 🔥 Vite + React + TailwindCSS
- 🌙 Dark/Light mode with system preference detection
- 🍿 AI companion + movie tracker integration
- 📄 Custom `/docs` page
- 🧭 Hash-based routing via React Router
- 💖 Ko-fi + Buy Me a Coffee support links
- 📄 `/404.html` with friendly fallback
- 🛠 GitHub Actions auto-deploy on push to `main`

---

## 🛠 Project Structure

```txt
frontend/
├── public/            # Static files (favicon, 404.html, CNAME)
├── src/               # Components, pages, main app logic
├── index.html         # Root HTML template
├── package.json       # Project dependencies
├── vite.config.js     # Vite config (with hash routing)
└── README.md          # You're here 👋
```

---

## 🧪 Local Dev

```bash
pnpm install
pnpm run dev
```
Make sure youre in the frontend/ directory.

---

## 🚀 Deploy
Deployment is handled via GitHub Actions:
```txt
•	Every push to main triggers a build
•	The built /frontend/dist folder is deployed to gh-pages
•	Custom domain: suvie.me
```
