// deploy-to-gh-pages.js
import fs from "fs-extra";
import path from "path";

const DIST_DIR = path.resolve("dist");
const TARGET_DIR = path.resolve("../gh-pages");

async function deploy() {
  try {
    console.log("📦 Cleaning gh-pages directory...");
    await fs.emptyDir(TARGET_DIR);

    console.log("📂 Copying new build...");
    await fs.copy(DIST_DIR, TARGET_DIR, {
      filter: (src) => !src.includes(".DS_Store"),
    });

    console.log("✅ Done! Ready to commit gh-pages.");
  } catch (err) {
    console.error("❌ Deployment failed:", err);
  }
}

deploy();
