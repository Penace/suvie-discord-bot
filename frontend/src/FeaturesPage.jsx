import React from "react";
import Footer from "./components/Footer.jsx";
import Nav from "./components/Nav.jsx";
import KoFiWidget from "./components/KoFiWidget.jsx";
import {
  TerminalIcon,
  MessageCircleIcon,
  HeartIcon,
  DatabaseIcon,
  BotIcon,
  RefreshCwIcon,
} from "lucide-react";

export default function FeaturesPage() {
  return (
    <div className="min-h-screen flex flex-col items-center px-6 pb-16 pt-12 text-zinc-800 dark:text-white bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950">
      <Nav />
      <div className="w-full max-w-5xl text-center">
        <h1 className="text-4xl font-extrabold mb-4">✨ Suvie Bot Features</h1>
        <p className="text-zinc-600 dark:text-zinc-400 mb-10">
          Explore what Suvie can do for your movie tracking, server workflow,
          and everyday entertainment.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <FeatureBox
            icon={<TerminalIcon className="h-6 w-6 text-pink-500 mx-auto" />}
            title="Slash Commands"
            desc="Interact with Suvie using clean, Discord-native commands."
          />
          <FeatureBox
            icon={
              <MessageCircleIcon className="h-6 w-6 text-pink-500 mx-auto" />
            }
            title="Smart Chat"
            desc="Use /ai to talk to your movie buddy, ask for recommendations, or explore mood-based suggestions."
          />
          <FeatureBox
            icon={<HeartIcon className="h-6 w-6 text-pink-500 mx-auto" />}
            title="Personalized Tracking"
            desc="Track your watchlist, downloads, and currently watching titles, all synced per server."
          />
          <FeatureBox
            icon={<DatabaseIcon className="h-6 w-6 text-pink-500 mx-auto" />}
            title="Backup System"
            desc="Auto-saves after every change, with a local backup JSON you can restore anytime."
          />
          <FeatureBox
            icon={<RefreshCwIcon className="h-6 w-6 text-pink-500 mx-auto" />}
            title="Hot Reloading"
            desc="Dynamically reload features without restarting the bot."
          />
          <FeatureBox
            icon={<BotIcon className="h-6 w-6 text-pink-500 mx-auto" />}
            title="Open Source & Expandable"
            desc="Built in modular cogs, Suvie is easy to maintain, fork, or enhance."
          />
        </div>

        <p className="mt-10 text-sm text-zinc-500 dark:text-zinc-400">
          Need help getting started?{" "}
          <a href="/#/docs" className="text-blue-500 hover:underline">
            Read the Docs
          </a>
        </p>
      </div>
      <Footer />
      <KoFiWidget />
    </div>
  );
}

function FeatureBox({ icon, title, desc }) {
  return (
    <div className="bg-white/60 dark:bg-zinc-800/60 backdrop-blur p-5 rounded-xl shadow hover:shadow-lg transition border text-center">
      {icon}
      <h3 className="font-semibold text-lg mt-3">{title}</h3>
      <p className="text-sm mt-1 text-zinc-600 dark:text-zinc-300">{desc}</p>
    </div>
  );
}
