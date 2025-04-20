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
    const handleResize = () => setIsMobile(window.innerWidth < 1080);
    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const navItemClass = (path) =>
    `relative flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 
    ${
      location.pathname === path
        ? "bg-zinc-800 text-white dark:bg-zinc-200 dark:text-black shadow-[0_0_0_2px_rgba(255,255,255,0.1)] animate-pulse-slow"
        : "text-zinc-600 dark:text-zinc-300 hover:text-black dark:hover:text-white"
    }
    before:absolute before:bottom-0 before:left-4 before:right-4 before:h-[2px] before:bg-pink-500 before:scale-x-0 hover:before:scale-x-100 before:transition-transform before:origin-left before:duration-300`;

  return (
    <nav className="w-full max-w-6xl mx-auto mb-6 relative z-40 animate-fade-in-up">
      <div className="flex rounded-2xl shadow-md overflow-hidden">
        {/* Logo Block with Gradient + Subtle Animation */}
        <div className="relative z-50 bg-gradient-to-br from-pink-500 to-pink-400 text-white px-6 py-2 rounded-l-2xl shadow-[4px_0_10px_-2px_rgba(0,0,0,0.15)] transition-all duration-500">
          <a href="/" className="text-lg font-bold text-white">
            suvie
          </a>
        </div>

        {/* Main Nav Bar */}
        <div className="flex-grow px-4 py-3 flex flex-wrap items-center justify-between bg-gradient-to-r from-white/80 to-zinc-100/80 dark:from-zinc-800/70 dark:to-zinc-900/70 backdrop-blur-md">
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

          {/* Right Utilities */}
          <div className="flex items-center gap-2 ml-auto">
            <div className="rounded-full transition bg-zinc-200 dark:bg-pink-600 text-black dark:text-white">
              <ThemeToggle />
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
        </div>
      </div>

      {/* Mobile Dropdown */}
      {isOpen && isMobile && (
        <div className="mt-2 flex flex-col gap-2 bg-white dark:bg-zinc-900 shadow-xl rounded-2xl p-4 z-50 animate-fade-in-up duration-500 ease-out">
          {" "}
          {[
            { path: "/", label: "Home", icon: <FaHome /> },
            { path: "/docs", label: "Docs", icon: <FaBook /> },
            { path: "/support", label: "Support", icon: <FaHeart /> },
            { path: "/roadmap", label: "Roadmap", icon: <FaRoad /> },
            { path: "/features", label: "Features", icon: <FaStar /> },
            { path: "/faq", label: "FAQ", icon: <FaQuestionCircle /> },
            { path: "/about", label: "About", icon: <FaUserAlt /> },
            { path: "/privacy", label: "Privacy", icon: <FaShieldAlt /> },
          ].map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={navItemClass(item.path)}
              onClick={() => setIsOpen(false)}
            >
              {item.icon} {item.label}
            </Link>
          ))}
        </div>
      )}
    </nav>
  );
}
