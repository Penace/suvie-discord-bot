import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import LandingPage from "./LandingPage.jsx";
import DocsPage from "./DocsPage.jsx"; // ⬅️ New component for /docs
import KoFiWidget from "./components/KoFiWidget.jsx";
import ThemeToggle from "./components/ThemeToggle.jsx";
import "./index.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/docs" element={<DocsPage />} />
      </Routes>

      {/* Global Widgets (always rendered) */}
      <KoFiWidget />
      <ThemeToggle />
    </BrowserRouter>
  </StrictMode>
);
