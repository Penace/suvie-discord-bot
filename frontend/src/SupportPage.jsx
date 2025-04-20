import Footer from "./components/Footer.jsx";
import Nav from "./components/Nav.jsx";
import KoFiWidget from "./components/KoFiWidget.jsx";

export default function SupportPage() {
  return (
    <div className="min-h-screen flex flex-col items-center px-6 pb-16 pt-12 text-zinc-800 dark:text-white bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950">
      <Nav />
      <div className="w-full max-w-3xl text-center">
        <h1 className="text-4xl font-extrabold mb-3">
          💖 Support Suvie – Your AI Movie Bot
        </h1>
        <p className="text-zinc-600 dark:text-zinc-400 mb-8">
          Suvie is an open-source Discord bot built with love, curiosity, and
          caffeine. If you find value in it, consider helping keep development
          cozy and sustainable.
        </p>

        <div className="flex justify-center gap-4 mb-8">
          <a
            href="https://ko-fi.com/penace"
            className="px-5 py-3 rounded-full bg-pink-500 text-white font-semibold hover:bg-pink-600 transition"
            target="_blank"
            rel="noopener noreferrer"
          >
            Support on Ko-fi
          </a>
          <a
            href="https://www.buymeacoffee.com/penace"
            className="px-5 py-3 rounded-full bg-yellow-400 text-white font-semibold hover:bg-yellow-500 transition"
            target="_blank"
            rel="noopener noreferrer"
          >
            Buy Me a Coffee
          </a>
        </div>

        <p className="text-sm text-zinc-600 dark:text-zinc-400">
          You can also{" "}
          <a
            href="https://github.com/Penace/suvie-discord-bot"
            className="text-blue-500 hover:underline"
            target="_blank"
          >
            ⭐️ star the repo
          </a>
          , share it with friends, or suggest a feature. Every bit helps.
        </p>
      </div>
      <Footer />
      <KoFiWidget />
    </div>
  );
}
