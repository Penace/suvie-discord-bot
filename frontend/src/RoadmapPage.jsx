import Footer from "./components/Footer.jsx";
import Nav from "./components/Nav.jsx";
import KoFiWidget from "./components/KoFiWidget.jsx";

export default function RoadmapPage() {
  return (
    <div className="min-h-screen flex flex-col items-center px-6 pb-16 pt-12 text-zinc-800 dark:text-white bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950">
      <Nav />
      <div className="w-full max-w-3xl text-center">
        <h1 className="text-4xl font-extrabold mb-3">🛣️ Suvie Bot Roadmap</h1>
        <p className="text-zinc-600 dark:text-zinc-400 mb-8">
          Here's a transparent look at the development journey of Suvie — what's
          shipped, what's being built, and what's on the horizon.
        </p>

        <ul className="text-left text-zinc-700 dark:text-zinc-300 space-y-4 text-sm">
          <li>
            ✅ <strong>Version 3</strong> — TV show support, multi-entry
            tracking, polished embedded UI, per-server scoped data, and backups.
          </li>
          <li>
            🚧 <strong>Version 4</strong> — Fuzzy matching, slash command
            builder UI, external data sync, and quality-of-life improvements.
          </li>
          <li>
            🔮 <strong>Future Plans</strong> — GUI frontend at{" "}
            <a
              href="https://suvie.me"
              className="text-blue-500 hover:underline"
              target="_blank"
            >
              suvie.me
            </a>
            , public stats/dashboard, and an optional premium supporter tier.
          </li>
        </ul>

        <p className="mt-6 text-sm text-zinc-500 dark:text-zinc-400">
          Have a feature request or idea?{" "}
          <a
            href="https://github.com/Penace/suvie-discord-bot/issues"
            target="_blank"
            className="text-blue-500 hover:underline"
          >
            Open an issue on GitHub
          </a>{" "}
          or share your thoughts in our support thread.
        </p>
      </div>
      <Footer />
      <KoFiWidget />
    </div>
  );
}
