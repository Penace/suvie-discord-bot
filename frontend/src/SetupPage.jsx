import Nav from "./components/Nav.jsx";
import Footer from "./components/Footer.jsx";
import KoFiWidget from "./components/KoFiWidget";

export default function SetupPage() {
  return (
    <div className="min-h-screen flex flex-col items-center px-6 pb-16 pt-12 text-zinc-800 dark:text-white bg-gradient-to-b from-zinc-50 to-zinc-200 dark:from-zinc-900 dark:to-zinc-950">
      <Nav />
      <Footer />
      <KoFiWidget />
    </div>
  );
}
