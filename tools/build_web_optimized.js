#!/usr/bin/env node
// Builds the Ren'Py web package with web-sized image assets for faster first load.
// Source art under game/images is left unchanged.

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const project = path.resolve(__dirname, "..");
const root = path.resolve(project, "..");
const out = path.join(project, "build-web");
const sourceGame = path.join(project, "game");
const work = path.join(root, "work", "web-build-optimized");
const optimizedGame = path.join(work, "game");
const sdkWeb = "C:\\Users\\12726\\Documents\\Codex\\tools\\renpy-sdk\\renpy-8.5.3-sdk\\web";
const python = "C:\\Users\\12726\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe";

function copyDir(src, dst) {
  fs.mkdirSync(dst, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dst, entry.name);
    if (entry.isDirectory()) copyDir(s, d);
    else fs.copyFileSync(s, d);
  }
}

function run(command, args, options = {}) {
  const result = spawnSync(command, args, {
    cwd: options.cwd || root,
    encoding: "utf8",
    maxBuffer: 1024 * 1024 * 20,
  });
  if (result.stdout) process.stdout.write(result.stdout);
  if (result.stderr) process.stderr.write(result.stderr);
  if (result.status !== 0) process.exit(result.status || 1);
}

if (!fs.existsSync(sdkWeb)) {
  console.error(`Missing Ren'Py web runtime: ${sdkWeb}`);
  process.exit(1);
}

fs.rmSync(out, { recursive: true, force: true });
fs.rmSync(work, { recursive: true, force: true });
copyDir(sdkWeb, out);
copyDir(sourceGame, optimizedGame);

const optimizeScript = `
from pathlib import Path
from PIL import Image

game = Path(r'''${optimizedGame.replace(/\\/g, "\\\\")}''')
total_before = 0
total_after = 0

def save_webp(im, path, quality):
    im.save(path, 'WEBP', quality=quality, method=4)

for path in sorted((game / 'images' / 'background').glob('*.webp')):
    total_before += path.stat().st_size
    im = Image.open(path).convert('RGB')
    if im.size != (1280, 720):
        im = im.resize((1280, 720), Image.Resampling.LANCZOS)
    save_webp(im, path, 58)
    total_after += path.stat().st_size

for path in sorted((game / 'images' / 'character').glob('*.webp')):
    total_before += path.stat().st_size
    im = Image.open(path).convert('RGBA')
    target_h = 640 if im.height > 720 else im.height
    if target_h != im.height:
        target_w = max(1, round(im.width * target_h / im.height))
        im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    save_webp(im, path, 60)
    total_after += path.stat().st_size

print(f'optimized images: {total_before} -> {total_after} bytes')
`;

run(python, ["-c", optimizeScript]);

const archive = path.join(out, "game.zip");
const zipScript = `
from pathlib import Path
import zipfile

game = Path(r'''${optimizedGame.replace(/\\/g, "\\\\")}''')
archive = Path(r'''${archive.replace(/\\/g, "\\\\")}''')
if archive.exists():
    archive.unlink()

with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for path in sorted(game.rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(game).as_posix()
        z.write(path, 'game/' + rel)
    # Emscripten's Python entrypoint opens /main.py. The SDK web runtime expects
    # this to be present in the virtual filesystem before Ren'Py starts.
    sdk = Path(r'''${sdkWeb.replace(/\\/g, "\\\\")}''').parent
    z.write(sdk / 'renpy.py', 'main.py')
`;
run(python, ["-c", zipScript]);

const symbolsPath = path.join(out, "index.html.symbols");
if (fs.existsSync(symbolsPath)) fs.unlinkSync(symbolsPath);

const presplashPath = path.join(out, "web-presplash.jpg");
if (fs.existsSync(presplashPath)) {
  const presplashScript = `
from pathlib import Path
from PIL import Image
p = Path(r'''${presplashPath.replace(/\\/g, "\\\\")}''')
im = Image.open(p).convert('RGB')
im.thumbnail((960, 540), Image.Resampling.LANCZOS)
im.save(p, 'JPEG', quality=68, optimize=True, progressive=True)
`;
  run(python, ["-c", presplashScript]);
}

const manifestPath = path.join(out, "manifest.json");
let manifest = {};
if (fs.existsSync(manifestPath)) {
  manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
}
manifest["package"] = "game.zip";
manifest["package"] = "game.zip";
manifest["name"] = "\u98ce\u66b4\u4e2d\u7684\u5927\u987a\u671d\u00b7\u5782\u66ae\u5e8f\u7ae0";
fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2), "utf8");

const indexPath = path.join(out, "index.html");
let index = fs.readFileSync(indexPath, "utf8");
index = index.replace(
  new RegExp("<title>.*?</title>"),
  "<title>\u98ce\u66b4\u4e2d\u7684\u5927\u987a\u671d\u00b7\u5782\u66ae\u5e8f\u7ae0</title>"
);
index = index.replace(
  "window.gameZipURL = 'game.zip';",
  "window.gameZipURL = 'game.zip?v=20260630-game-dir-fix';"
);
fs.writeFileSync(indexPath, index, "utf8");

const serviceWorkerPath = path.join(out, "service-worker.js");
if (fs.existsSync(serviceWorkerPath)) {
  let serviceWorker = fs.readFileSync(serviceWorkerPath, "utf8");
  serviceWorker = serviceWorker.replace(
    "var cacheName = 'renpy-web-game';",
    "var cacheName = 'chuimuo-web-game-20260630-game-dir-fix';"
  );
  fs.writeFileSync(serviceWorkerPath, serviceWorker, "utf8");
}

console.log(`Optimized web build written to ${out}`);
