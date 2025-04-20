import { Link, useLocation } from "react-router-dom";
import ThemeToggle from "./ThemeToggle";

export default function Nav() {
  const location = useLocation();

  const navItemClass = (path) =>
    `px-4 py-2 rounded-full text-sm font-medium transition ${
      location.pathname === path
        ? "bg-zinc-800 text-white dark:bg-zinc-200 dark:text-black"
        : "text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800"
    }`;

  return (
    <nav className="w-full max-w-5xl mx-auto flex flex-wrap justify-between items-center gap-2 mb-6 px-4 py-3 bg-white/60 dark:bg-zinc-900/50 rounded-2xl shadow-md backdrop-blur-sm transition">
      <div className="text-lg font-bold text-zinc-900 dark:text-white">
        suvie
      </div>

      <div className="flex flex-wrap gap-2 items-center">
        <Link to="/" className={navItemClass("/")}>
          Home
        </Link>
        <Link to="/docs" className={navItemClass("/docs")}>
          Docs
        </Link>
        <Link to="/support" className={navItemClass("/support")}>
          Support
        </Link>
        <Link to="/roadmap" className={navItemClass("/roadmap")}>
          Roadmap
        </Link>
      </div>

      <ThemeToggle />
    </nav>
  );
}
