import Nav from "./Nav";
import Footer from "./Footer";
import KoFiWidget from "./KoFiWidget";
import ThemeToggle from "./ThemeToggle";

export default function Layout({ children }) {
  return (
    <div className="min-h-screen flex flex-col items-center px-4 pb-8 pt-4 text-zinc-800 dark:text-white bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950 transition-colors duration-300">
      <Nav />
      <main className="w-full max-w-5xl flex-grow py-6">{children}</main>
      <Footer />
      <ThemeToggle />
      <KoFiWidget />
    </div>
  );
}
