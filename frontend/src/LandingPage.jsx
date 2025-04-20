import React from "react";
import {
  MessageCircleIcon,
  HeartIcon,
  TerminalIcon,
  BrainIcon,
  EyeIcon,
  TagIcon,
} from "lucide-react";
import { FaDiscord, FaCoffee, FaHeart, FaGithub } from "react-icons/fa";
import Footer from "./components/Footer.jsx";
import KoFiWidget from "./components/KoFiWidget.jsx";

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

      {/* Main */}
      <main className="w-full max-w-5xl space-y-10 animate-fade-in">
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
          <FeatureBox
            icon={
              <TerminalIcon className="h-6 w-6 text-pink-500 mx-auto mb-3" />
            }
            title="Quick Commands"
            desc="Add, update, and track movies and shows with a single slash command."
          />
          <FeatureBox
            icon={
              <MessageCircleIcon className="h-6 w-6 text-pink-500 mx-auto mb-3" />
            }
            title="Smart Chat"
            desc="Talk to suvie like a friend — get recommendations and more."
          />
          <FeatureBox
            icon={<HeartIcon className="h-6 w-6 text-pink-500 mx-auto mb-3" />}
            title="Personalized"
            desc="Keeps track of your current watchlist and what's next."
          />
          <FeatureBox
            icon={
              <BrainIcon className="h-6 w-6 text-indigo-500 mx-auto mb-3" />
            }
            title="Learns You"
            desc="Suvie adapts over time to better match your movie tastes."
          />
          <FeatureBox
            icon={<EyeIcon className="h-6 w-6 text-green-500 mx-auto mb-3" />}
            title="Cross-Server Sync"
            desc="Your watchlist follows you across all servers seamlessly."
          />
          <FeatureBox
            icon={<TagIcon className="h-6 w-6 text-yellow-500 mx-auto mb-3" />}
            title="Custom Tags"
            desc="Add personal tags to organize your movies your way."
          />
        </section>
      </main>

      <Footer />
      <KoFiWidget />
    </div>
  );
}

function FeatureBox({ icon, title, desc }) {
  return (
    <div className="p-4 bg-white/60 dark:bg-zinc-800/70 rounded-xl shadow hover:shadow-xl transition-all duration-300 border backdrop-blur-md">
      {icon}
      <h3 className="font-semibold text-lg">{title}</h3>
      <p className="text-sm mt-2 text-zinc-600 dark:text-zinc-300">{desc}</p>
    </div>
  );
}
