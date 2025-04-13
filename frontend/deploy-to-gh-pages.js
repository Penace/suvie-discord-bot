// deploy-gh-pages.js
import fs from "fs-extra";
import path from "path";
import { execSync } from "child_process";

const BUILD_CMD = "npm run build"; // should be run inside frontend/
const FRONTEND_DIR = path.resolve("frontend");
const DIST_DIR = path.join(FRONTEND_DIR, "dist");
const TEMP_DIR = path.resolve(".temp-gh-pages");
const GH_BRANCH = "gh-pages";
const CNAME = "suvie.me";

async function deploy() {
  try {
    console.log("📦 Building the site...");
    execSync(BUILD_CMD, { cwd: FRONTEND_DIR, stdio: "inherit" });

    console.log("🚚 Preparing temporary directory...");
    await fs.remove(TEMP_DIR);
    await fs.copy(DIST_DIR, TEMP_DIR);

    // Add .nojekyll and CNAME
    fs.writeFileSync(path.join(TEMP_DIR, ".nojekyll"), "");
    fs.writeFileSync(path.join(TEMP_DIR, "CNAME"), CNAME);

    console.log("🔀 Switching to gh-pages branch...");
    execSync(`git checkout ${GH_BRANCH}`);

    console.log("🧹 Cleaning gh-pages branch...");
    fs.readdirSync(process.cwd()).forEach((file) => {
      if (file !== ".git") fs.removeSync(path.resolve(file));
    });

    console.log("📁 Deploying new build to root...");
    await fs.copy(TEMP_DIR, ".");

    console.log("📤 Committing and pushing...");
    execSync(`git add .`);
    execSync(`git commit -m "🚀 Deploy to GitHub Pages"`);
    execSync(`git push origin ${GH_BRANCH}`);

    console.log("✅ Deployment complete! 🚀");

    // Restore main branch
    console.log("🔁 Switching back to main branch...");
    execSync(`git checkout main`);
    await fs.remove(TEMP_DIR);
    console.log("✨ Cleaned up and ready to go.");
  } catch (err) {
    console.error("❌ Deployment failed:", err);
  }
}

deploy();
