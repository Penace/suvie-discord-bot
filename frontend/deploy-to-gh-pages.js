// deploy-to-gh-pages.js
import fs from "fs-extra";
import path from "path";
import { execSync } from "child_process";

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

    console.log("🔁 Committing changes to gh-pages...");
    execSync(`git add .`, { cwd: TARGET_DIR, stdio: "inherit" });
    execSync(
      `git commit -m "Deploy landing page" || echo "No changes to commit."`,
      {
        cwd: TARGET_DIR,
        stdio: "inherit",
      }
    );

    console.log("🚀 Pushing to remote...");
    execSync(`git push origin gh-pages --force`, {
      cwd: TARGET_DIR,
      stdio: "inherit",
    });

    console.log("✅ Deployed to GitHub Pages!");
  } catch (err) {
    console.error("❌ Deployment failed:", err.message || err);
  }
}

deploy();
