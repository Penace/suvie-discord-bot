import { execSync } from "child_process";
import fs from "fs-extra";
import path from "path";

const ROOT = path.resolve(".");
const DIST = path.resolve("frontend/dist");
const TEMP = path.resolve(".deploy-temp");
const FILES_TO_PRESERVE = ["CNAME", ".gitignore"]; // Add more if needed

async function run() {
  try {
    console.log("📦 Building frontend...");
    execSync("npm run build", {
      cwd: path.resolve("frontend"),
      stdio: "inherit",
    });

    console.log("📁 Backing up essential files...");
    await fs.ensureDir(TEMP);
    for (const file of FILES_TO_PRESERVE) {
      if (await fs.pathExists(path.join(ROOT, file))) {
        await fs.copy(path.join(ROOT, file), path.join(TEMP, file));
      }
    }
    console.log("🔍 Checking for uncommitted changes...");
    const status = execSync("git status --porcelain").toString().trim();

    if (status) {
      console.log(
        "🛑 Uncommitted changes detected. Committing before deploy..."
      );

      execSync("git add .", { stdio: "inherit" });
      execSync('git commit -m "🚧 Pre-deploy auto commit"', {
        stdio: "inherit",
      });
    }

    console.log("🔀 Switching to gh-pages...");
    execSync("git checkout gh-pages", { stdio: "inherit" });

    console.log("🧹 Cleaning gh-pages root...");
    const files = await fs.readdir(ROOT);
    for (const file of files) {
      if (![".git", ".deploy-temp"].includes(file)) {
        await fs.remove(path.join(ROOT, file));
      }
    }

    console.log("📂 Copying new build to root...");
    await fs.copy(DIST, ROOT);

    console.log("📑 Restoring preserved files...");
    for (const file of FILES_TO_PRESERVE) {
      if (await fs.pathExists(path.join(TEMP, file))) {
        await fs.copy(path.join(TEMP, file), path.join(ROOT, file));
      }
    }

    console.log("📄 Ensuring .nojekyll is present...");
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
