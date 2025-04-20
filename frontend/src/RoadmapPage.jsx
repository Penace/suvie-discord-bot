import Footer from "./components/Footer.jsx";
import Nav from "./components/Nav.jsx";
import KoFiWidget from "./components/KoFiWidget.jsx";

export default function RoadmapPage() {
  return (
    <div className="min-h-screen flex flex-col items-center px-6 pb-16 pt-12 text-zinc-800 dark:text-white bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950">
      <Nav />
      <div className="w-full max-w-3xl text-center">
        <h1 className="text-4xl font-extrabold mb-3">🛣️ Roadmap</h1>
        <p className="text-zinc-600 dark:text-zinc-400 mb-8">
          A living roadmap of what’s next for Suvie — from improvements to new
          ideas.
        </p>

        <ul className="text-left text-zinc-700 dark:text-zinc-300 space-y-6 text-sm">
          <li>
            <strong>✅ v3: TV Support + Backup System</strong>
            <br />
            TV tracking, episode incrementing, structured backups, and improved
            UX.
          </li>

          <li>
            <strong>🚧 v4: Smart Matching + Advanced Slash Commands</strong>
            <br />
            Fuzzy title recognition, autocomplete, error handling, and embedded
            slash command builder.
          </li>

          <li>
            <strong>📊 v5: Public Stats & Server Dashboards</strong>
            <br />
            Anonymous movie trends, leaderboard views, and server-level stats.
          </li>

          <li>
            <strong>💡 Future Features</strong>
            <br />
            • Premium mode (optional perks)
            <br />• Web-based viewer at <code>suvie.me</code>
            <br />
            • Mobile-first companion app
            <br />• Multilingual support
          </li>
        </ul>
      </div>
      <Footer />
      <KoFiWidget />
    </div>
  );
}
