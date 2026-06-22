import { copyFileSync, cpSync, existsSync, mkdirSync, rmSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const dist = join(root, "dist");

if (existsSync(dist)) {
  rmSync(dist, { recursive: true, force: true });
}

mkdirSync(dist, { recursive: true });
copyFileSync(join(root, "index.html"), join(dist, "index.html"));
copyFileSync(join(root, "pay_qr.html"), join(dist, "pay_qr.html"));
copyFileSync(join(root, "content_generator.html"), join(dist, "content_generator.html"));
cpSync(join(root, "assets"), join(dist, "assets"), { recursive: true });

console.log("frontend build ok");
