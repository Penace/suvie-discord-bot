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
    <div
      className="fixed bottom-5 right-5 z-50"
      aria-label="Toggle dark mode"
      onClick={toggleTheme}
    >
      <div
        className={`w-12 h-6 flex items-center bg-zinc-300 dark:bg-zinc-700 rounded-full p-1 cursor-pointer transition`}
      >
        <div
          className={`bg-white dark:bg-black w-4 h-4 rounded-full shadow transform transition-transform duration-300 ${
            isDark ? "translate-x-6" : "translate-x-0"
          }`}
        />
      </div>
    </div>
  );
}
