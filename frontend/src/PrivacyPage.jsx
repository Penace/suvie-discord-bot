import React from "react";
import Footer from "./components/Footer.jsx";
import Nav from "./components/Nav.jsx";
import KoFiWidget from "./components/KoFiWidget.jsx";

export default function PrivacyPage() {
  return (
    <div className="min-h-screen flex flex-col items-center px-6 pb-16 pt-12 text-zinc-800 dark:text-white bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950">
      <Nav />
      <div className="w-full max-w-3xl text-center">
        <h1 className="text-4xl font-extrabold mb-4">🔐 Privacy Policy</h1>
        <p className="text-zinc-600 dark:text-zinc-400 mb-8">
          Suvie is designed with privacy and simplicity in mind. Here's what we
          do (and don’t do).
        </p>

        <div className="space-y-6 text-left text-sm text-zinc-700 dark:text-zinc-300">
          <div>
            <h2 className="font-semibold text-base mb-1">
              📦 No Data Harvesting
            </h2>
            <p>
              Suvie does not collect, track, or share personal data. There is no
              analytics, telemetry, or data sharing of any kind.
            </p>
          </div>

          <div>
            <h2 className="font-semibold text-base mb-1">🧠 Commands Only</h2>
            <p>
              Suvie only interacts with slash commands. It does not read
              messages, monitor channels, or log user activity beyond what is
              necessary to execute your request.
            </p>
          </div>

          <div>
            <h2 className="font-semibold text-base mb-1">
              💾 Local Storage Only
            </h2>
            <p>
              All your watchlist and AI data is stored in per-server local JSON
              files. Backups are stored on your own bot instance.
            </p>
          </div>

          <div>
            <h2 className="font-semibold text-base mb-1">
              🔓 100% Open Source
            </h2>
            <p>
              You can view, modify, and audit all source code on{" "}
              <a
                href="https://github.com/Penace/suvie-discord-bot"
                target="_blank"
                className="text-blue-500 hover:underline"
              >
                GitHub
              </a>
              . Nothing is hidden or obfuscated.
            </p>
          </div>

          <div>
            <h2 className="font-semibold text-base mb-1">❓ Questions?</h2>
            <p>
              Reach out on GitHub, open an issue, or use the{" "}
              <a href="/#/support" className="text-blue-500 hover:underline">
                Support Page
              </a>{" "}
              to contact us.
            </p>
          </div>
        </div>
      </div>
      <Footer />
      <KoFiWidget />
    </div>
  );
}
