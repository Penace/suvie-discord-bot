import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import {
  FaHome,
  FaBook,
  FaHeart,
  FaRoad,
  FaStar,
  FaQuestionCircle,
  FaUserAlt,
  FaShieldAlt,
} from "react-icons/fa";
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
    <nav className="w-full max-w-6xl mx-auto px-4 py-3 mb-6 bg-white/60 dark:bg-zinc-900/50 backdrop-blur-md rounded-2xl shadow-md flex items-center justify-between flex-wrap relative z-30">
      {/* Logo */}
      <div className="text-lg font-bold text-zinc-900 dark:text-white">
        <a href="/" className="flex items-center gap-2">
          suvie
        </a>
      </div>

      {/* Desktop Navigation */}
      <div className="hidden md:flex flex-wrap gap-2 items-center">
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
        <Link to="/features" className={navItemClass("/features")}>
          <FaStar /> Features
        </Link>
        <Link to="/faq" className={navItemClass("/faq")}>
          <FaQuestionCircle /> FAQ
        </Link>
        <Link to="/about" className={navItemClass("/about")}>
          <FaUserAlt /> About
        </Link>
        <Link to="/privacy" className={navItemClass("/privacy")}>
          <FaShieldAlt /> Privacy
        </Link>
      </div>

      {/* Right-side: Theme toggle + mobile menu */}
      <div className="flex items-center gap-2">
        <div className="rounded-full bg-zinc-200 dark:bg-pink-500 text-black dark:text-white">
          <ThemeToggle />
        </div>
        <button
          className="md:hidden p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition"
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle menu"
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
        <div className="absolute top-full left-0 right-0 mt-2 flex flex-col gap-2 bg-white dark:bg-zinc-900 shadow-xl rounded-2xl p-4 md:hidden z-20">
          {[
            ["/", <FaHome />, "Home"],
            ["/docs", <FaBook />, "Docs"],
            ["/support", <FaHeart />, "Support"],
            ["/roadmap", <FaRoad />, "Roadmap"],
            ["/features", <FaStar />, "Features"],
            ["/faq", <FaQuestionCircle />, "FAQ"],
            ["/about", <FaUserAlt />, "About"],
            ["/privacy", <FaShieldAlt />, "Privacy"],
          ].map(([path, icon, label]) => (
            <Link
              key={path}
              to={path}
              className={navItemClass(path)}
              onClick={() => setIsOpen(false)}
            >
              {icon} {label}
            </Link>
          ))}
        </div>
      )}
    </nav>
  );
}
