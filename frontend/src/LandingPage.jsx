import React from "react";
import { TerminalIcon, MessageCircleIcon, HeartIcon } from "lucide-react";
import { FaDiscord, FaGithub, FaHeart, FaCoffee } from "react-icons/fa";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-between bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950 text-zinc-800 dark:text-white px-6 pb-12">
      {/* Header */}
      <header className="w-full max-w-5xl mx-auto text-center pt-10">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight dark:text-white">
          suvie
        </h1>
        <p className="mt-2 text-zinc-600 dark:text-zinc-400">
          Your cozy AI movie companion 🎬
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-wrap justify-center gap-4 mt-6">
          <a
            href="https://discord.com/oauth2/authorize?client_id=1360281760016892066&scope=bot+applications.commands"
            className="inline-flex items-center px-6 py-3 bg-[#5865F2] hover:bg-[#4752c4] text-white text-base font-medium rounded-full shadow-lg transition"
            target="_blank"
            rel="noopener noreferrer"
          >
            <FaDiscord className="mr-2 w-5 h-5" />
            Invite to Discord
          </a>
          <a
            href="https://github.com/Penace/suvie-discord-bot"
            className="inline-flex items-center px-5 py-2.5 bg-zinc-800 hover:bg-zinc-700 text-white text-sm font-semibold rounded-full shadow-md transition"
            target="_blank"
            rel="noopener noreferrer"
          >
            <FaGithub className="mr-2 w-5 h-5" />
            View on GitHub
          </a>
          <a
            href="https://suvie.me/docs"
            className="inline-flex items-center px-5 py-2.5 bg-zinc-800 hover:bg-zinc-700 text-white text-sm font-semibold rounded-full shadow-md transition"
            target="_blank"
            rel="noopener noreferrer"
          >
            Read Docs
          </a>
        </div>

        {/* Support Buttons */}
        <div className="flex flex-wrap justify-center gap-4 mt-4">
          <a
            href="https://ko-fi.com/penace"
            className="inline-flex items-center px-4 py-2 bg-[#FF5F5F] hover:bg-[#e74c3c] text-white text-sm font-semibold rounded-full shadow transition"
            target="_blank"
            rel="noopener noreferrer"
          >
            <FaHeart className="mr-2 w-5 h-5" />
            Support on Ko-fi
          </a>
          <a
            href="https://www.buymeacoffee.com/penace"
            className="inline-flex items-center px-4 py-2 bg-yellow-400 hover:bg-yellow-500 text-white text-sm font-semibold rounded-full shadow transition"
            target="_blank"
            rel="noopener noreferrer"
          >
            <FaCoffee className="mr-2 w-5 h-5" />
            Buy Me a Coffee
          </a>
        </div>
      </header>

      {/* Features */}
      <main className="w-full max-w-5xl mt-16 space-y-12 text-center">
        <section>
          <h2 className="text-2xl font-bold mb-4">
            Meet suvie — Your Cozy AI Movie Companion 🍿
          </h2>
          <p className="text-zinc-700 dark:text-zinc-300 max-w-xl mx-auto leading-relaxed">
            Track what you're watching, get personal recommendations, and chat
            with your AI movie buddy — all inside Discord.
          </p>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
          <div className="p-6 bg-white/70 dark:bg-zinc-800/60 rounded-xl shadow border">
            <TerminalIcon className="mx-auto mb-4 h-6 w-6 text-pink-500" />
            <h3 className="font-semibold text-lg">Quick Commands</h3>
            <p className="text-sm mt-2 text-zinc-600 dark:text-zinc-300">
              Add, update, and track movies and shows with a single slash
              command.
            </p>
          </div>
          <div className="p-6 bg-white/70 dark:bg-zinc-800/60 rounded-xl shadow border">
            <MessageCircleIcon className="mx-auto mb-4 h-6 w-6 text-pink-500" />
            <h3 className="font-semibold text-lg">Smart Chat</h3>
            <p className="text-sm mt-2 text-zinc-600 dark:text-zinc-300">
              Talk to suvie like a friend — get recommendations and more.
            </p>
          </div>
          <div className="p-6 bg-white/70 dark:bg-zinc-800/60 rounded-xl shadow border">
            <HeartIcon className="mx-auto mb-4 h-6 w-6 text-pink-500" />
            <h3 className="font-semibold text-lg">Personalized</h3>
            <p className="text-sm mt-2 text-zinc-600 dark:text-zinc-300">
              Keeps track of your current watchlist and what's next.
            </p>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="w-full max-w-5xl mt-20 text-center text-sm text-zinc-500 dark:text-zinc-400">
        © 2025 suvie by{" "}
        <a href="https://penace.org" className="underline">
          Penace
        </a>{" "}
        •{" "}
        <a href="https://github.com/Penace/" className="underline">
          GitHub
        </a>{" "}
        •{" "}
        <a href="https://ko-fi.com/penace" className="underline text-pink-500">
          Ko-fi
        </a>{" "}
        •{" "}
        <a
          href="https://www.buymeacoffee.com/penace"
          className="underline text-yellow-600"
        >
          Buy Me a Coffee
        </a>
      </footer>
    </div>
  );
}
