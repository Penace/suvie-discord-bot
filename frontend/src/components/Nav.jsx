import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { FaHome, FaBook, FaHeart, FaRoad } from "react-icons/fa";
import { MenuIcon, XIcon } from "lucide-react";
import ThemeToggle from "./ThemeToggle";

export default function Nav() {
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);

  const navItemClass = (path) =>
    `flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition ${
      location.pathname === path
        ? "bg-zinc-800 text-white dark:bg-zinc-200 dark:text-black"
        : "text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800"
    }`;

  return (
    <nav className="w-full max-w-5xl mx-auto px-4 py-3 mb-6 bg-white/60 dark:bg-zinc-900/50 backdrop-blur-md rounded-2xl shadow-md flex items-center justify-between">
      <div className="text-lg font-bold text-zinc-900 dark:text-white">
        suvie
      </div>

      <div className="hidden md:flex gap-2 items-center">
        <Link to="/" className={navItemClass("/")}>
          <FaHome /> Home
        </Link>
        <Link to="/docs" className={navItemClass("/docs")}>
          <FaBook /> Docs
        </Link>
        <Link to="/support" className={navItemClass("/support")}>
          <FaHeart /> Support
        </Link>
        <Link to="/roadmap" className={navItemClass("/roadmap")}>
          <FaRoad /> Roadmap
        </Link>
      </div>

      <div className="flex items-center gap-2">
        <ThemeToggle />
        <button
          className="md:hidden p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? (
            <XIcon className="w-5 h-5" />
          ) : (
            <MenuIcon className="w-5 h-5" />
          )}
        </button>
      </div>

      {/* Mobile Dropdown */}
      {isOpen && (
        <div className="absolute top-full left-4 right-4 mt-2 flex flex-col gap-2 bg-white dark:bg-zinc-900 shadow-xl rounded-2xl p-4 z-50 md:hidden">
          <Link
            to="/"
            className={navItemClass("/")}
            onClick={() => setIsOpen(false)}
          >
            <FaHome /> Home
          </Link>
          <Link
            to="/docs"
            className={navItemClass("/docs")}
            onClick={() => setIsOpen(false)}
          >
            <FaBook /> Docs
          </Link>
          <Link
            to="/support"
            className={navItemClass("/support")}
            onClick={() => setIsOpen(false)}
          >
            <FaHeart /> Support
          </Link>
          <Link
            to="/roadmap"
            className={navItemClass("/roadmap")}
            onClick={() => setIsOpen(false)}
          >
            <FaRoad /> Roadmap
          </Link>
        </div>
      )}
    </nav>
  );
}
