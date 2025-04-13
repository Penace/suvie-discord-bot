import { execSync } from "child_process";
import fs from "fs-extra";
import path from "path";

const ROOT = path.resolve(".");
const DIST = path.resolve("frontend/dist");
const CNAME_SOURCE = path.resolve("docs/CNAME");
const TEMP = path.resolve(".deploy-temp");

async function run() {
  try {
    console.log("📦 Building frontend...");
    execSync("npm run build", {
      cwd: path.resolve("frontend"),
      stdio: "inherit",
    });

    console.log("📁 Saving CNAME to temp...");
    await fs.ensureDir(TEMP);
    await fs.copy(CNAME_SOURCE, path.join(TEMP, "CNAME"));

    console.log("🔀 Switching to gh-pages...");
    execSync("git checkout gh-pages", { stdio: "inherit" });

    console.log("🧹 Cleaning gh-pages...");
    const files = await fs.readdir(ROOT);
    for (const file of files) {
      if (![".git", ".gitignore"].includes(file)) {
        await fs.remove(path.join(ROOT, file));
      }
    }

    console.log("📂 Copying new build to root...");
    await fs.copy(DIST, ROOT);

    console.log("📑 Restoring CNAME...");
    await fs.copy(path.join(TEMP, "CNAME"), path.join(ROOT, "CNAME"));

    console.log("📄 Adding .nojekyll...");
    await fs.outputFile(path.join(ROOT, ".nojekyll"), "");

    console.log("📤 Committing & pushing...");
    execSync("git add .", { stdio: "inherit" });
    execSync('git commit -m "🚀 Deploy latest build to suvie.me"', {
      stdio: "inherit",
    });
    execSync("git push origin gh-pages", { stdio: "inherit" });

    console.log("🔁 Returning to main...");
    execSync("git checkout main", { stdio: "inherit" });

    console.log("✅ Deployment complete!");
  } catch (err) {
    console.error("❌ Deployment failed:", err);
  } finally {
    await fs.remove(TEMP);
  }
}

run();
