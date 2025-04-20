import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { HashRouter, Routes, Route } from "react-router-dom";
import LandingPage from "./LandingPage.jsx";
import DocsPage from "./DocsPage.jsx";
import SupportPage from "./SupportPage.jsx";
import RoadmapPage from "./RoadmapPage.jsx";

// import Footer from "./components/Footer.jsx";
// import KoFiWidget from "./components/KoFiWidget.jsx";
// import ThemeToggle from "./components/ThemeToggle.jsx";
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
    </HashRouter>
  </StrictMode>
);
