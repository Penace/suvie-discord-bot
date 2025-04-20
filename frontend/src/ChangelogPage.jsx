import React from "react";
import Footer from "./components/Footer.jsx";
import Nav from "./components/Nav.jsx";
import KoFiWidget from "./components/KoFiWidget.jsx";

export default function ChangelogPage() {
  return (
    <div className="min-h-screen flex flex-col items-center px-6 pb-16 pt-12 text-zinc-800 dark:text-white bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950">
      <Nav />
      <div className="w-full max-w-3xl text-left">
        <h1 className="text-4xl font-extrabold mb-4 text-center">
          📦 Changelog
        </h1>
        <div className="space-y-8 text-sm text-zinc-700 dark:text-zinc-300">
          <div>
            <h2 className="text-base font-semibold mb-1">v3.2.0 – Apr 2025</h2>
            <ul className="list-disc list-inside">
              <li>📂 New GUI frontend for suvie.me</li>
              <li>🌓 Added system theme detection + theme toggle</li>
              <li>📄 Docs, Roadmap, Support, and Features pages live</li>
              <li>🪧 Added SEO metadata & Open Graph optimizations</li>
              <li>🔐 Added Privacy Policy and About page</li>
            </ul>
          </div>

          <div>
            <h2 className="text-base font-semibold mb-1">v3.1.0 – Mar 2025</h2>
            <ul className="list-disc list-inside">
              <li>🧠 Slash commands fully implemented</li>
              <li>📁 Per-server scoped backups + restore support</li>
              <li>💬 AI conversation command refinements</li>
              <li>🚨 Improved error handling and input validation</li>
            </ul>
          </div>

          <div>
            <h2 className="text-base font-semibold mb-1">v3.0.0 – Feb 2025</h2>
            <ul className="list-disc list-inside">
              <li>📺 Full support for TV series tracking (season + episode)</li>
              <li>🧾 Multi-entry system for currently watching</li>
              <li>🧹 UI overhaul with polished embeds</li>
              <li>🧪 Introduced command groups & fuzzy matching (beta)</li>
            </ul>
          </div>

          <div>
            <h2 className="text-base font-semibold mb-1">v2.x and earlier</h2>
            <p className="mt-1">
              Suvie began as a simple personal watchlist tracker. Earlier
              versions were built on classic command prefixes and stored data in
              flat files. The open-source era began in 2025.
            </p>
          </div>
        </div>
      </div>
      <Footer />
      <KoFiWidget />
    </div>
  );
}
