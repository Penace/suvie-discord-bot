import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import LandingPage from "./LandingPage.jsx";
import KoFiWidget from "./components/KoFiWidget.jsx";
import ThemeToggle from "./components/ThemeToggle.jsx";
import "./index.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <LandingPage />
    <KoFiWidget />
    <ThemeToggle />
  </StrictMode>
);
