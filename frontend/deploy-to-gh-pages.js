// frontend/deploy-to-root.js
import fs from "fs-extra";
import path from "path";
import { fileURLToPath } from "url";
import { exec } from "child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const DIST_DIR = path.resolve(__dirname, "dist");
const ROOT_DIR = path.resolve(__dirname, ".."); // suvie-bot root

console.log("📦 Building site...");

exec("npm run build", { cwd: __dirname }, async (err, stdout, stderr) => {
  if (err) {
    console.error("❌ Build failed:", stderr);
    process.exit(1);
  }

  console.log("✅ Build complete.\n🧹 Cleaning old root deployment files...");

  try {
    const whitelist = ["CNAME", "movies.json", ".nojekyll"];
    const rootFiles = await fs.readdir(ROOT_DIR);

    // Clean all old deployment files except whitelisted
    for (const file of rootFiles) {
      const filePath = path.join(ROOT_DIR, file);
      if (
        fs.lstatSync(filePath).isFile() &&
        !whitelist.includes(file) &&
        !file.endsWith(".py") && // don't delete backend
        !file.endsWith(".env") && !file.endsWith(".md")
      ) {
        await fs.remove(filePath);
      }
    }

    console.log("📂 Copying new files to root...");
    await fs.copy(DIST_DIR, ROOT_DIR, {
      filter: (src) => !src.includes(".DS_Store"),
    });

    console.log("✅ Deployment complete! Root is updated with new build.");
    process.exit(0);
  } catch (e) {
    console.error("❌ Deployment failed:", e);
    process.exit(1);
  }
});
