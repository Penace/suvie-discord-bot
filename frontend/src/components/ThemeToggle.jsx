import { useEffect, useState } from "react";

export default function ThemeToggle() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("theme");
    const systemDark = window.matchMedia(
      "(prefers-color-scheme: dark)"
    ).matches;
    const activeDark = saved === "dark" || (!saved && systemDark);
    document.documentElement.classList.toggle("dark", activeDark);
    setIsDark(activeDark);
  }, []);

  const toggleTheme = () => {
    const newIsDark = !isDark;
    document.documentElement.classList.toggle("dark", newIsDark);
    localStorage.setItem("theme", newIsDark ? "dark" : "light");
    setIsDark(newIsDark);
  };

  return (
    <button
      onClick={toggleTheme}
      className="w-12 h-6 flex items-center rounded-full bg-zinc-300 dark:bg-pink-600 p-1 transition-colors duration-300"
      aria-label="Toggle dark mode"
    >
      <div
        className={`w-4 h-4 rounded-full bg-white dark:bg-black shadow transform transition-transform duration-300 ${
          isDark ? "translate-x-6" : ""
        }`}
      />
    </button>
  );
}
