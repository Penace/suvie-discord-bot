import React from "react";
import {
  RocketIcon,
  MessageCircleIcon,
  HeartIcon,
  TerminalIcon,
} from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-between p-6 text-zinc-800 dark:text-white bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950">
      <header className="w-full max-w-4xl mx-auto py-8 text-center">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-black dark:text-white">
          suvie
        </h1>
        <p className="mt-2 text-zinc-600 dark:text-zinc-400">
          Your cozy AI movie companion 🎬
        </p>
        <a
          href="https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center mt-6 px-6 py-3 bg-pink-500 hover:bg-pink-600 text-white text-lg font-medium rounded-full transition shadow-lg"
        >
          Invite to Discord <RocketIcon className="ml-2 h-5 w-5" />
        </a>
      </header>

      <main className="w-full max-w-3xl space-y-8">
        <section className="text-center">
          <h2 className="text-2xl font-bold mb-4">
            Meet suvie — Your Cozy AI Movie Companion 🍿
          </h2>
          <p className="text-zinc-700 dark:text-zinc-300 leading-relaxed">
            Track what you're watching, get personal recommendations, and chat
            with your AI movie buddy — all inside Discord.
          </p>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
          <div className="p-4 bg-white/50 dark:bg-zinc-800/60 rounded-xl shadow border">
            <TerminalIcon className="mx-auto mb-3 h-6 w-6 text-pink-500" />
            <h3 className="font-semibold text-lg">Quick Commands</h3>
            <p className="text-sm mt-2 text-zinc-600 dark:text-zinc-300">
              Add, update, and track movies and shows with a single slash
              command.
            </p>
          </div>
          <div className="p-4 bg-white/50 dark:bg-zinc-800/60 rounded-xl shadow border">
            <MessageCircleIcon className="mx-auto mb-3 h-6 w-6 text-pink-500" />
            <h3 className="font-semibold text-lg">Smart Chat</h3>
            <p className="text-sm mt-2 text-zinc-600 dark:text-zinc-300">
              Talk to suvie like a friend — get recommendations and more.
            </p>
          </div>
          <div className="p-4 bg-white/50 dark:bg-zinc-800/60 rounded-xl shadow border">
            <HeartIcon className="mx-auto mb-3 h-6 w-6 text-pink-500" />
            <h3 className="font-semibold text-lg">Personalized</h3>
            <p className="text-sm mt-2 text-zinc-600 dark:text-zinc-300">
              Keeps track of your current watchlist and what's next.
            </p>
          </div>
        </section>
      </main>

      <footer className="w-full max-w-4xl mt-16 text-center text-sm text-zinc-500 dark:text-zinc-400">
        © 2025 suvie by Penace. Built with ❤️
      </footer>
    </div>
  );
}
