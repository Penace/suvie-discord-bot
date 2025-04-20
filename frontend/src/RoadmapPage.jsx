import Footer from "./components/Footer.jsx";
import KoFiWidget from "./components/KoFiWidget.jsx";
import ThemeToggle from "./components/ThemeToggle.jsx";
import Nav from "./components/Nav.jsx";

export default function RoadmapPage() {
  return (
    <div className="min-h-screen flex flex-col items-center px-6 pb-16 pt-12 text-zinc-800 dark:text-white bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950">
      <div className="w-full max-w-3xl text-center">
        <h1 className="text-4xl font-extrabold mb-3">🛣️ Roadmap</h1>
        <Nav />
        <p className="text-zinc-600 dark:text-zinc-400 mb-8">
          A glimpse into what’s next for Suvie.
        </p>

        <ul className="text-left text-zinc-700 dark:text-zinc-300 space-y-4 text-sm">
          <li>✅ Version 3 – TV Show support, multi-entry, polished embeds</li>
          <li>
            🚧 Version 4 – Fuzzy matching, slash command builder, external data
            sync
          </li>
          <li>
            🔮 Future – GUI frontend (suvie.me), public stats, and premium tier
          </li>
        </ul>
      </div>
      <Footer />
      <KoFiWidget />
      <ThemeToggle />
    </div>
  );
}
