import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { HashRouter, Routes, Route } from "react-router-dom";

import LandingPage from "./LandingPage.jsx";
import DocsPage from "./DocsPage.jsx";
import SupportPage from "./SupportPage.jsx";
import RoadmapPage from "./RoadmapPage.jsx";
import FeaturesPage from "./FeaturesPage.jsx";
import FAQPage from "./FAQPage.jsx";
import AboutPage from "./AboutPage.jsx";
import PrivacyPage from "./PrivacyPage.jsx";
import ChangelogPage from "./ChangelogPage.jsx";

import "./index.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <HashRouter>
      <Routes>
        {/* Home has no layout */}
        <Route path="/" element={<LandingPage />} />

        {/* Core site pages */}
        <Route path="/docs" element={<DocsPage />} />
        <Route path="/support" element={<SupportPage />} />
        <Route path="/roadmap" element={<RoadmapPage />} />
        <Route path="/features" element={<FeaturesPage />} />
        <Route path="/faq" element={<FAQPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/privacy" element={<PrivacyPage />} />
        <Route path="/changelog" element={<ChangelogPage />} />
      </Routes>
    </HashRouter>
  </StrictMode>
);
