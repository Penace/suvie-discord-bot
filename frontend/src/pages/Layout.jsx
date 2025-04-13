import { Link, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="p-4 bg-black text-white border-b border-gray-800 flex justify-between items-center">
        <Link
          to="/"
          className="text-xl font-bold text-pink-400 hover:underline lowercase"
        >
          suvie
        </Link>
        <nav className="space-x-4 text-sm">
          <Link to="/">Home</Link>
          <Link to="/watchlist">Watchlist</Link>
          <Link to="/ai">AI</Link>
        </nav>
      </header>
      <main className="flex-1 p-6">
        <Outlet />
      </main>
    </div>
  );
}
