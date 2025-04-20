import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { HashRouter, Routes, Route } from "react-router-dom";

import LandingPage from "./LandingPage.jsx";
import DocsPage from "./DocsPage.jsx";
import SupportPage from "./SupportPage.jsx";
import RoadmapPage from "./RoadmapPage.jsx";

import Layout from "./components/Layout.jsx"; // reusable wrapper
import "./index.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <HashRouter>
      <Routes>
        {/* Home has no layout */}
        <Route path="/" element={<LandingPage />} />

        {/* All other pages go inside layout */}
        <Route
          path="/docs"
          element={
            <Layout>
              <DocsPage />
            </Layout>
          }
        />
        <Route
          path="/support"
          element={
            <Layout>
              <SupportPage />
            </Layout>
          }
        />
        <Route
          path="/roadmap"
          element={
            <Layout>
              <RoadmapPage />
            </Layout>
          }
        />
      </Routes>
    </HashRouter>
  </StrictMode>
);
