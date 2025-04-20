import React from "react";
import Footer from "./components/Footer.jsx";
import Nav from "./components/Nav.jsx";
import KoFiWidget from "./components/KoFiWidget.jsx";

export default function FAQPage() {
  return (
    <div className="min-h-screen flex flex-col items-center px-6 pb-16 pt-12 text-zinc-800 dark:text-white bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950">
      <Nav />
      <div className="w-full max-w-3xl">
        <h1 className="text-4xl font-extrabold mb-4 text-center">
          ❓ Frequently Asked Questions
        </h1>
        <div className="space-y-8 text-zinc-700 dark:text-zinc-300 text-sm">
          <Question
            q="How does Suvie store data?"
            a="Suvie uses lightweight JSON files saved per server. Every change is backed up automatically, and your data stays within your server environment."
          />
          <Question
            q="Can I use Suvie in multiple servers?"
            a="Yes! Suvie is scoped per server, meaning each community gets its own independent watchlist, AI memory, and backups."
          />
          <Question
            q="How do I reset or clear my watchlist?"
            a="Use /watchlist clear to wipe your list. You can also remove individual items using /watchlist remove."
          />
          <Question
            q="Does Suvie track or store personal messages?"
            a="No. Suvie only responds to explicit slash commands. It does not collect user data, track messages, or monitor channels."
          />
          <Question
            q="Can I restore previous backups?"
            a="Yes. Suvie automatically backs up after every change. The latest versions are stored and can be reloaded manually (coming soon via /backup restore)."
          />
          <Question
            q="What’s the deal with Suvie’s AI?"
            a="Suvie’s optional /ai command lets you chat with a friendly movie-focused AI. It doesn’t use message history and respects all bot privacy boundaries."
          />
        </div>
      </div>
      <Footer />
      <KoFiWidget />
    </div>
  );
}

function Question({ q, a }) {
  return (
    <div>
      <h3 className="text-base font-semibold mb-1">{q}</h3>
      <p className="text-sm text-zinc-600 dark:text-zinc-300">{a}</p>
    </div>
  );
}
