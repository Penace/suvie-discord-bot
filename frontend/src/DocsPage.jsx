import React from "react";
import { Link } from "react-router-dom";

export default function DocsPage() {
  return (
    <div className="min-h-screen flex flex-col items-center px-6 pb-16 pt-12 text-zinc-800 dark:text-white bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950">
      <div className="w-full max-w-4xl">
        <h1 className="text-4xl font-extrabold mb-2">📘 Documentation</h1>
        <p className="text-zinc-600 dark:text-zinc-400 mb-6">
          Everything you need to know about using <strong>suvie</strong>, your
          cozy AI movie companion.
        </p>

        <nav className="mb-12 text-sm">
          <Link to="/" className="text-blue-500 hover:underline">
            ← Back to Home |{" "}
            <a
              href="https://github.com/Penace/suvie-discord-bot/blob/main/docs/COMMANDS.md"
              target="_blank"
            >
              View raw markdown →
            </a>
          </Link>
        </nav>

        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-2">🧩 Core Features</h2>
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

        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-2">🤖 AI & Interaction</h2>
          <p className="text-zinc-700 dark:text-zinc-300">
            Talk to suvie like a friend. Ask for recommendations, keep track of
            your mood, and explore new films with conversational AI. Use{" "}
            <code>/ai</code> to chat.
          </p>
        </section>

        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-2">🛠 Setup & Tips</h2>
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
        </section>

        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-2">💖 Support</h2>
          <p className="text-zinc-700 dark:text-zinc-300">
            If you enjoy suvie, consider supporting on{" "}
            <a
              href="https://ko-fi.com/penace"
              target="_blank"
              rel="noopener noreferrer"
              className="text-pink-500 hover:underline"
            >
              Ko-fi
            </a>{" "}
            or{" "}
            <a
              href="https://www.buymeacoffee.com/penace"
              target="_blank"
              rel="noopener noreferrer"
              className="text-yellow-500 hover:underline"
            >
              Buy Me a Coffee
            </a>
            .
          </p>
        </section>
      </div>
    </div>
  );
}
