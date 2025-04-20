import React from "react";
import {
  RocketIcon,
  MessageCircleIcon,
  HeartIcon,
  TerminalIcon,
} from "lucide-react";
import { FaDiscord, FaCoffee, FaHeart, FaGithub } from "react-icons/fa";
import Footer from "./components/Footer.jsx";
import KoFiWidget from "./components/KoFiWidget.jsx";
import ThemeToggle from "./components/ThemeToggle.jsx";
import Nav from "./components/Nav.jsx";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-between p-6 pb-6 text-zinc-800 dark:text-white bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950 transition-colors duration-300">
      {/* Header */}
      <header className="w-full max-w-5xl mx-auto py-6 text-center">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-black dark:text-white">
          suvie
        </h1>
        <p className="mt-2 text-zinc-600 dark:text-zinc-400">
          Your cozy AI movie companion 🎬
        </p>

        <div className="flex flex-wrap justify-center gap-4 mt-6">
          <a
            href="https://discord.com/oauth2/authorize?client_id=1360281760016892066&scope=bot+applications.commands"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center px-6 py-3 bg-[#5865F2] hover:bg-[#4752c4] text-white text-lg font-medium rounded-full shadow-md hover:shadow-lg transition-all duration-200"
          >
            <FaDiscord className="w-6 h-6 mr-2" />
            Invite to Discord
          </a>

          <a
            href="https://github.com/Penace/suvie-discord-bot"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center px-5 py-2.5 bg-zinc-800 hover:bg-zinc-700 text-white text-sm font-semibold rounded-full shadow-md hover:shadow-lg transition-all duration-200"
          >
            <FaGithub className="w-6 h-6 mr-2" />
            View on GitHub
          </a>

          <a
            href="/#/docs"
            className="inline-flex items-center px-5 py-2.5 bg-zinc-800 hover:bg-zinc-700 text-white text-sm font-semibold rounded-full shadow-md hover:shadow-lg transition-all duration-200"
          >
            Read Docs
          </a>

          <a
            href="/#/support"
            className="inline-flex items-center px-4 py-2 bg-pink-500 hover:bg-pink-600 text-white text-sm font-semibold rounded-full shadow-md hover:shadow-lg transition-all duration-200"
          >
            <FaHeart className="w-5 h-5 mr-2" />
            Support
          </a>

          <a
            href="/#/roadmap"
            className="inline-flex items-center px-4 py-2 bg-yellow-400 hover:bg-yellow-500 text-white text-sm font-semibold rounded-full shadow-md hover:shadow-lg transition-all duration-200"
          >
            <FaCoffee className="w-5 h-5 mr-2" />
            Roadmap
          </a>
        </div>
      </header>
      <Nav />
      {/* Main */}
      <main className="w-full max-w-4xl space-y-10">
        <section className="text-center">
          <h2 className="text-2xl font-bold mb-3">
            Meet suvie — Your Cozy AI Movie Companion 🍿
          </h2>
          <p className="text-zinc-700 dark:text-zinc-300 leading-relaxed">
            Track what you're watching, get personal recommendations, and chat
            with your AI movie buddy — all inside Discord.
          </p>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
          <div className="p-4 bg-white/60 dark:bg-zinc-800/70 rounded-xl shadow hover:shadow-xl transition-all duration-300 border">
            <TerminalIcon className="mx-auto mb-3 h-6 w-6 text-pink-500" />
            <h3 className="font-semibold text-lg">Quick Commands</h3>
            <p className="text-sm mt-2 text-zinc-600 dark:text-zinc-300">
              Add, update, and track movies and shows with a single slash
              command.
            </p>
          </div>
          <div className="p-4 bg-white/60 dark:bg-zinc-800/70 rounded-xl shadow hover:shadow-xl transition-all duration-300 border">
            <MessageCircleIcon className="mx-auto mb-3 h-6 w-6 text-pink-500" />
            <h3 className="font-semibold text-lg">Smart Chat</h3>
            <p className="text-sm mt-2 text-zinc-600 dark:text-zinc-300">
              Talk to suvie like a friend — get recommendations and more.
            </p>
          </div>
          <div className="p-4 bg-white/60 dark:bg-zinc-800/70 rounded-xl shadow hover:shadow-xl transition-all duration-300 border">
            <HeartIcon className="mx-auto mb-3 h-6 w-6 text-pink-500" />
            <h3 className="font-semibold text-lg">Personalized</h3>
            <p className="text-sm mt-2 text-zinc-600 dark:text-zinc-300">
              Keeps track of your current watchlist and what's next.
            </p>
          </div>
        </section>
      </main>
      <Footer />
      <KoFiWidget />
      <ThemeToggle />
    </div>
  );
}
