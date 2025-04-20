import Layout from "./components/Layout.jsx"; // reusable wrapper

export default function SupportPage() {
  return (
    <div className="min-h-screen flex flex-col items-center px-6 pb-16 pt-12 text-zinc-800 dark:text-white bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950">
      <Layout>
        <div className="w-full max-w-3xl text-center">
          <h1 className="text-4xl font-extrabold mb-3">💖 Support suvie</h1>
          <p className="text-zinc-600 dark:text-zinc-400 mb-8">
            Help support the development and maintenance of Suvie. Every
            contribution keeps it cozy.
          </p>

          <div className="flex justify-center gap-4 mb-8">
            <a
              href="https://ko-fi.com/penace"
              className="px-5 py-3 rounded-full bg-pink-500 text-white font-semibold hover:bg-pink-600 transition"
              target="_blank"
            >
              Ko-fi
            </a>
            <a
              href="https://www.buymeacoffee.com/penace"
              className="px-5 py-3 rounded-full bg-yellow-400 text-white font-semibold hover:bg-yellow-500 transition"
              target="_blank"
            >
              Buy Me a Coffee
            </a>
          </div>

          <p className="text-sm text-zinc-600 dark:text-zinc-400">
            You can also sponsor Suvie monthly, spread the word, or suggest
            features.
          </p>
        </div>
      </Layout>
    </div>
  );
}
