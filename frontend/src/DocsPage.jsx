import React from "react";
import { Link } from "react-router-dom";
import Footer from "./components/Footer.jsx";
import Nav from "./components/Nav.jsx";
import KoFiWidget from "./components/KoFiWidget.jsx";

export default function DocsPage() {
  return (
    <div className="min-h-screen flex flex-col items-center px-6 pb-16 pt-12 text-zinc-800 dark:text-white bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950">
      <Nav />
      <div className="w-full max-w-4xl">
        <h1 className="text-4xl font-extrabold mb-2">
          📘 Suvie Discord Bot Documentation
        </h1>
        <p className="text-zinc-600 dark:text-zinc-400 mb-6">
          Official documentation for <strong>suvie</strong>, the cozy AI movie
          companion bot for Discord. Learn all the available features, commands,
          and how to make the most of your experience.
        </p>

        <nav className="mb-12 text-sm space-x-2">
          <a href="#features" className="text-blue-500 hover:underline">
            Features
          </a>
          <a href="#ai" className="text-blue-500 hover:underline">
            AI
          </a>
          <a href="#setup" className="text-blue-500 hover:underline">
            Setup
          </a>
          <a href="#support" className="text-blue-500 hover:underline">
            Support
          </a>
          <a href="#commands" className="text-blue-500 hover:underline">
            Commands
          </a>
        </nav>

        <section id="features" className="mb-10">
          <h2 className="text-2xl font-semibold mb-2">🧩 Core Features</h2>
          <p className="mb-2 text-zinc-700 dark:text-zinc-300">
            Suvie helps you track and manage your movies and shows with simple
            Discord slash commands.
          </p>
          <ul className="list-disc list-inside text-zinc-700 dark:text-zinc-300 space-y-1">
            <li>
              Track what you're watching with <code>/currentlywatching</code>
            </li>
            <li>
              Add or remove titles from your <code>/watchlist</code>
            </li>
            <li>
              Mark downloads with <code>/downloaded</code>
            </li>
            <li>
              Archive items with <code>/watched</code>
            </li>
            <li>
              Monitor bot status with <code>/status</code>
            </li>
          </ul>
        </section>

        <section id="ai" className="mb-10">
          <h2 className="text-2xl font-semibold mb-2">🤖 AI & Interaction</h2>
          <p className="text-zinc-700 dark:text-zinc-300">
            Talk to suvie like a friend. Ask for recommendations, keep track of
            your mood, and explore new films with conversational AI. Use{" "}
            <code>/ai</code> to chat.
          </p>
        </section>

        <section id="setup" className="mb-10">
          <h2 className="text-2xl font-semibold mb-2">🛠 Setup & Tips</h2>
          <p className="mb-2 text-zinc-700 dark:text-zinc-300">
            Getting started is easy. Follow the tips below or view the full
            setup guide.
          </p>
          <ul className="list-disc list-inside text-zinc-700 dark:text-zinc-300 space-y-1">
            <li>Invite Suvie to your server via the homepage</li>
            <li>
              Use commands in any text channel or set a dedicated bot channel
            </li>
            <li>
              Everything is saved automatically — no need to worry about losing
              data
            </li>
          </ul>
          <p className="mt-2">
            <a
              href="https://github.com/Penace/suvie-discord-bot/blob/main/docs/SETUP.md"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              View Setup Guide ↗
            </a>
          </p>
        </section>

        <section id="support" className="mb-10">
          <h2 className="text-2xl font-semibold mb-2">💖 Support</h2>
          <p className="text-zinc-700 dark:text-zinc-300">
            If you enjoy using Suvie, consider supporting development through:
          </p>
          <ul className="list-disc list-inside text-zinc-700 dark:text-zinc-300 space-y-1 mt-2">
            <li>
              <a
                href="https://ko-fi.com/penace"
                target="_blank"
                rel="noopener noreferrer"
                className="text-pink-500 hover:underline"
              >
                Ko-fi
              </a>
            </li>
            <li>
              <a
                href="https://www.buymeacoffee.com/penace"
                target="_blank"
                rel="noopener noreferrer"
                className="text-yellow-500 hover:underline"
              >
                Buy Me a Coffee
              </a>
            </li>
          </ul>
          <p className="mt-2 text-zinc-700 dark:text-zinc-300">
            ⭐️ Don't forget to{" "}
            <a
              href="https://github.com/Penace/suvie-discord-bot"
              className="text-blue-500 hover:underline"
              target="_blank"
            >
              star the repo
            </a>{" "}
            and share it with your friends!
          </p>
        </section>
      </div>
      <Footer />
      <KoFiWidget />
    </div>
  );
}
