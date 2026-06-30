#!/usr/bin/env node
// Creates a fast-loading Ren'Py Web build using the official Ren'Py web builder.
// Source art under game/images is left unchanged.

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const project = path.resolve(__dirname, "..");
const root = path.resolve(project, "..");
const out = path.join(project, "build-web");
const sourceGame = path.join(project, "game");
const work = path.join(root, "work", "web-build-optimized");
const optimizedProject = path.join(work, "chuimuo-visual-novel");
const optimizedGame = path.join(optimizedProject, "game");
const officialOut = path.join(work, "official-web");
const sdk = "C:\\Users\\12726\\Documents\\Codex\\tools\\renpy-sdk\\renpy-8.5.3-sdk";
const renpy = path.join(sdk, "renpy.exe");
const launcher = path.join(sdk, "launcher");
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
    maxBuffer: 1024 * 1024 * 100,
  });
  if (result.stdout) process.stdout.write(result.stdout);
  if (result.stderr) process.stderr.write(result.stderr);
  if (result.status !== 0) process.exit(result.status || 1);
}

if (!fs.existsSync(renpy)) {
  console.error(`Missing Ren'Py SDK: ${renpy}`);
  process.exit(1);
}

fs.rmSync(out, { recursive: true, force: true });
fs.rmSync(work, { recursive: true, force: true });
fs.mkdirSync(optimizedProject, { recursive: true });

for (const name of fs.readdirSync(project, { withFileTypes: true })) {
  if ([".git", "build-web"].includes(name.name)) continue;
  const s = path.join(project, name.name);
  const d = path.join(optimizedProject, name.name);
  if (name.isDirectory()) copyDir(s, d);
  else fs.copyFileSync(s, d);
}

const cleanupScript = `
from pathlib import Path
import shutil

game = Path(r'''${optimizedGame.replace(/\\/g, "\\\\")}''')
for pattern in ('*.rpyc', '*.rpymc', '*.rpyb'):
    for path in game.rglob(pattern):
        path.unlink()
for dirname in ('saves',):
    shutil.rmtree(game / dirname, ignore_errors=True)
for path in game.rglob('*.bak'):
    path.unlink()
`;
run(python, ["-c", cleanupScript]);

const optimizeScript = `
from pathlib import Path
from PIL import Image

game = Path(r'''${optimizedGame.replace(/\\/g, "\\\\")}''')
total_before = 0
total_after = 0

def save_webp(im, path, quality):
    im.save(path, 'WEBP', quality=quality, method=6)

for path in sorted((game / 'images' / 'background').glob('*.webp')):
    total_before += path.stat().st_size
    im = Image.open(path).convert('RGB')
    if im.size != (1280, 720):
        im = im.resize((1280, 720), Image.Resampling.LANCZOS)
    save_webp(im, path, 56)
    total_after += path.stat().st_size

for path in sorted((game / 'images' / 'character').glob('*.webp')):
    total_before += path.stat().st_size
    im = Image.open(path).convert('RGBA')
    target_h = 640 if im.height > 720 else im.height
    if target_h != im.height:
        target_w = max(1, round(im.width * target_h / im.height))
        im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    save_webp(im, path, 58)
    total_after += path.stat().st_size

print(f'optimized images: {total_before} -> {total_after} bytes')
`;
run(python, ["-c", optimizeScript]);

run(renpy, [optimizedProject, "compile"], { cwd: optimizedProject });
run(renpy, [launcher, "web_build", optimizedProject, "--destination", officialOut], { cwd: root });

copyDir(officialOut, out);

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
im.save(p, 'JPEG', quality=62, optimize=True, progressive=True)
`;
  run(python, ["-c", presplashScript]);
}

const manifestPath = path.join(out, "manifest.json");
let manifest = {};
if (fs.existsSync(manifestPath)) {
  manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
}
manifest.name = "风暴中的大顺朝·垂暮序章";
manifest.short_name = "垂暮序章";
manifest.lang = "zh-CN";
fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2), "utf8");

const title = "风暴中的大顺朝·垂暮序章";
const description = "架空历史悬疑水墨风视觉小说，一段关于理想、信息差与时代悲剧的故事";
const image = "game/images/background/bg_mainmenu.webp";
const indexPath = path.join(out, "index.html");
let index = fs.readFileSync(indexPath, "utf8");
index = index.replace(/<title>.*?<\/title>/, `<title>${title}</title>`);
const meta = `
  <meta name="description" content="${description}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="${title}">
  <meta property="og:description" content="${description}">
  <meta property="og:image" content="${image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${title}">
  <meta name="twitter:description" content="${description}">
  <meta name="twitter:image" content="${image}">
`;
if (!index.includes('property="og:title"')) {
  index = index.replace("</head>", `${meta}\n</head>`);
}
index = index.replace(/window\.gameZipURL = 'game\.zip[^']*';/, "window.gameZipURL = 'game.zip?v=20260630-official-fast-font';");
fs.writeFileSync(indexPath, index, "utf8");

const serviceWorkerPath = path.join(out, "service-worker.js");
if (fs.existsSync(serviceWorkerPath)) {
  let serviceWorker = fs.readFileSync(serviceWorkerPath, "utf8");
  serviceWorker = serviceWorker.replace(
    /var cacheName = 'renpy-web-game[^']*';/,
    "var cacheName = 'chuimuo-web-game-20260630-official-fast-font';"
  );
  fs.writeFileSync(serviceWorkerPath, serviceWorker, "utf8");
}

console.log(`Optimized official web build written to ${out}`);
