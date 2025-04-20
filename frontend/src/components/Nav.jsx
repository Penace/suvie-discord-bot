import { useState, useEffect } from "react";
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
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth < 700);
    window.addEventListener("resize", handleResize);
    handleResize();
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const navItemClass = (path) =>
    `flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition whitespace-nowrap ${
      location.pathname === path
        ? "bg-zinc-800 text-white dark:bg-zinc-200 dark:text-black"
        : "text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800"
    }`;

  return (
    <nav className="w-full max-w-6xl mx-auto px-4 py-3 mb-6 bg-white/60 dark:bg-zinc-900/50 backdrop-blur-md rounded-2xl shadow-md flex flex-wrap items-center justify-between relative z-40">
      {/* Left Side Logo */}
      <div className="text-lg font-bold text-zinc-900 dark:text-white">
        <a href="/" className="flex items-center gap-2">
          suvie
        </a>
      </div>

      {/* Center Nav (Desktop) */}
      {!isMobile && (
        <div className="flex flex-wrap items-center gap-2">
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
      )}

      {/* Right Side: Toggle & Dropdown */}
      <div className="ml-auto flex items-center gap-2">
        <div className="h-full flex items-center">
          <div className="rounded-full transition bg-zinc-200 dark:bg-pink-500 text-black dark:text-white">
            <ThemeToggle />
          </div>
        </div>
        {isMobile && (
          <button
            className="p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? (
              <XIcon className="w-5 h-5" />
            ) : (
              <MenuIcon className="w-5 h-5" />
            )}
          </button>
        )}
      </div>

      {/* Mobile Dropdown */}
      {isOpen && isMobile && (
        <div className="absolute top-full left-4 right-4 mt-2 flex flex-col gap-2 bg-white dark:bg-zinc-900 shadow-xl rounded-2xl p-4 z-50">
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
          <Link
            to="/features"
            className={navItemClass("/features")}
            onClick={() => setIsOpen(false)}
          >
            <FaStar /> Features
          </Link>
          <Link
            to="/faq"
            className={navItemClass("/faq")}
            onClick={() => setIsOpen(false)}
          >
            <FaQuestionCircle /> FAQ
          </Link>
          <Link
            to="/about"
            className={navItemClass("/about")}
            onClick={() => setIsOpen(false)}
          >
            <FaUserAlt /> About
          </Link>
          <Link
            to="/privacy"
            className={navItemClass("/privacy")}
            onClick={() => setIsOpen(false)}
          >
            <FaShieldAlt /> Privacy
          </Link>
        </div>
      )}
    </nav>
  );
}
