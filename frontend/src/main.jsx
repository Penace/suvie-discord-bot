import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { HashRouter, Routes, Route } from "react-router-dom";
import Footer from "./components/Footer.jsx";
import LandingPage from "./LandingPage.jsx";
import DocsPage from "./DocsPage.jsx";
import KoFiWidget from "./components/KoFiWidget.jsx";
import ThemeToggle from "./components/ThemeToggle.jsx";
import "./index.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <HashRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/docs" element={<DocsPage />} />
        <Route path="/support" element={<SupportPage />} />
        <Route path="/roadmap" element={<RoadmapPage />} />
      </Routes>

      <Footer />
      <KoFiWidget />
      <ThemeToggle />
    </HashRouter>
  </StrictMode>
);
