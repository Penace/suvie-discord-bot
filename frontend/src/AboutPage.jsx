import React from "react";
import Footer from "./components/Footer.jsx";
import Nav from "./components/Nav.jsx";
import KoFiWidget from "./components/KoFiWidget.jsx";

export default function AboutPage() {
  return (
    <div className="min-h-screen flex flex-col items-center px-6 pb-16 pt-12 text-zinc-800 dark:text-white bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950">
      <Nav />
      <div className="w-full max-w-3xl text-center">
        <h1 className="text-4xl font-extrabold mb-4">👋 About Suvie</h1>
        <p className="text-zinc-600 dark:text-zinc-400 mb-8">
          Suvie is a cozy open-source Discord bot that helps you track movies,
          organize watchlists, and talk casually with an AI movie companion —
          all from within your server.
        </p>

        <div className="space-y-6 text-left text-sm text-zinc-700 dark:text-zinc-300">
          <div>
            <h2 className="font-semibold text-base mb-1">🧠 Why Suvie?</h2>
            <p>
              Suvie was born from the idea that entertainment tracking should be
              lightweight, fun, and beautifully integrated with communities.
              Instead of bloated apps or noisy tools, Suvie quietly supports
              your viewing habits while respecting your space.
            </p>
          </div>

          <div>
            <h2 className="font-semibold text-base mb-1">👨‍💻 Built by Penace</h2>
            <p>
              Suvie was designed and built by{" "}
              <a
                href="https://penace.org"
                target="_blank"
                className="text-blue-500 hover:underline"
              >
                Penace
              </a>{" "}
              — a developer and designer who enjoys crafting thoughtful tools.
              This project blends creativity, minimalism, and community-first
              development.
            </p>
          </div>

          <div>
            <h2 className="font-semibold text-base mb-1">🚀 The Road Ahead</h2>
            <p>
              We're working on improving fuzzy matching, public dashboards, a
              beautiful web UI at{" "}
              <a
                href="https://suvie.me"
                className="text-blue-500 hover:underline"
                target="_blank"
              >
                suvie.me
              </a>
              , and more. Your feedback and support shape the future.
            </p>
          </div>
        </div>
      </div>
      <Footer />
      <KoFiWidget />
    </div>
  );
}
