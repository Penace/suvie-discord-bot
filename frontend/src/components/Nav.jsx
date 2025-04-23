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
  FaHistory,
  FaDiscord,
} from "react-icons/fa";
import { MenuIcon, XIcon } from "lucide-react";
import ThemeToggle from "./ThemeToggle";

const allLinks = [
  {
    path: "/invite",
    label: "Invite",
    icon: <FaDiscord size={18} />,
    isInvite: true,
  },
  { path: "/docs", label: "Docs", icon: <FaBook size={18} /> },
  { path: "/support", label: "Support", icon: <FaHeart size={18} /> },
  { path: "/roadmap", label: "Roadmap", icon: <FaRoad size={18} /> },
  { path: "/features", label: "Features", icon: <FaStar size={18} /> },
  { path: "/faq", label: "FAQ", icon: <FaQuestionCircle size={18} /> },
  { path: "/about", label: "About", icon: <FaUserAlt size={18} /> },
  { path: "/privacy", label: "Privacy", icon: <FaShieldAlt size={18} /> },
  { path: "/changelog", label: "Changelog", icon: <FaHistory size={18} /> },
];

const getVisibleCount = (width) => {
  if (width > 1300) return allLinks.length;
  if (width > 1154) return 8;
  if (width > 1050) return 7;
  if (width > 937) return 6;
  if (width > 814) return 5;
  if (width > 723) return 4;
  if (width > 570) return 3;
  if (width > 405) return 3;
  if (width > 330) return 1;
  return 0;
};

export default function Nav() {
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);
  const [visibleCount, setVisibleCount] = useState(allLinks.length);
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const update = () => {
      setVisibleCount(getVisibleCount(window.innerWidth));
      setWidth(window.innerWidth);
    };
    update();
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, []);

  const visibleLinks = allLinks.slice(0, visibleCount);
  const collapsedLinks = allLinks.slice(visibleCount);

  const navItemClass = (path, isInvite = false) =>
    `relative flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 ${
      location.pathname === path
        ? "bg-zinc-800 text-white dark:bg-zinc-200 dark:text-black shadow-sm animate-pulse-slow"
        : isInvite
        ? "bg-[#5865F2] text-white hover:bg-[#4752c4]"
        : "text-zinc-600 dark:text-zinc-300 hover:text-black dark:hover:text-white"
    } before:absolute before:bottom-0 before:left-4 before:right-4 before:h-[2px] before:bg-pink-500 before:scale-x-0 hover:before:scale-x-100 before:transition-transform before:origin-left before:duration-300`;

  return (
    <nav className="w-full max-w-6xl mx-auto mb-6 relative z-40 animate-fade-in-up">
      <div className="flex rounded-2xl shadow-md overflow-hidden h-[56px]">
        {/* Logo Section */}
        <a
          href="/"
          className="relative z-50 bg-pink-500 text-white px-6 flex items-center rounded-l-2xl transition-transform hover:scale-105"
        >
          <span className="text-lg font-bold">suvie</span>
        </a>

        {/* Main Nav */}
        <div className="flex-grow px-4 py-3 flex items-center justify-between bg-gradient-to-r from-white/80 to-zinc-100/80 dark:from-zinc-800/70 dark:to-zinc-900/70 backdrop-blur-md">
          <div className="flex flex-wrap items-center gap-2">
            {visibleLinks.map(({ path, label, icon, isInvite }) => (
              <Link
                key={path}
                to={
                  path === "/invite"
                    ? "https://discord.com/oauth2/authorize?client_id=1360281760016892066&scope=bot+applications.commands"
                    : path
                }
                className={`${navItemClass(path, isInvite)} ${
                  width <= 550 && width > 405 ? "px-3 py-2 text-xs" : ""
                } ${width <= 405 ? "p-2 text-base" : ""}`}
              >
                {icon} {width > 550 ? label : width <= 405 ? null : ""}
              </Link>
            ))}
          </div>

          {/* Right Utilities */}
          <div className="absolute right-4 top-1/2 -translate-y-1/2 flex items-center gap-2">
            <div className="rounded-full bg-zinc-200 dark:bg-pink-600 text-black dark:text-white">
              <ThemeToggle position="inline" />
            </div>
            {collapsedLinks.length > 0 && (
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

      {/* Collapsed Dropdown */}
      {isOpen && collapsedLinks.length > 0 && (
        <div className="mt-2 flex flex-col gap-2 bg-white dark:bg-zinc-900 shadow-xl rounded-2xl p-4 z-50 animate-slide-down duration-500 ease-out">
          {collapsedLinks.map(({ path, label, icon, isInvite }) => (
            <Link
              key={path}
              to={
                path === "/invite"
                  ? "https://discord.com/oauth2/authorize?client_id=1360281760016892066&scope=bot+applications.commands"
                  : path
              }
              className={navItemClass(path, isInvite)}
              onClick={() => setIsOpen(false)}
            >
              {icon} {label}
            </Link>
          ))}

          {/* Extra CTA */}
          <a
            href="https://discord.com/oauth2/authorize?client_id=1360281760016892066&scope=bot+applications.commands"
            target="_blank"
            rel="noopener noreferrer"
            className="mt-4 text-center inline-block px-6 py-3 rounded-full bg-[#5865F2] hover:bg-[#4752c4] text-white font-semibold text-sm transition-all"
          >
            Invite suvie to your server
          </a>
        </div>
      )}
    </nav>
  );
}
