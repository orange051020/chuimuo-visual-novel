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
const title = "风暴中的大顺朝·垂暮序章";
const description = "架空历史悬疑水墨风视觉小说，一段关于理想、信息差与时代悲剧的故事";
const image = "game/images/background/bg_mainmenu.webp";

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
manifest.name = title;
manifest.short_name = "垂暮序章";
manifest.lang = "zh-CN";
fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2), "utf8");

const officialIndex = path.join(out, "renpy.html");
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
fs.writeFileSync(officialIndex, index, "utf8");

const story = buildStory();
fs.writeFileSync(path.join(out, "story.json"), JSON.stringify(story, null, 2), "utf8");
fs.writeFileSync(indexPath, buildLightweightIndex(story), "utf8");

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

function readUtf8(file) {
  return fs.readFileSync(file, "utf8").replace(/^\uFEFF/, "");
}

function buildAssetMap() {
  const text = readUtf8(path.join(project, "game", "story", "asset_manifest.rpy"));
  const map = {};
  for (const line of text.split(/\r?\n/)) {
    const m = line.match(/^image\s+(.+?)\s*=\s*"([^"]+)"/);
    if (!m) continue;
    map[m[1].trim()] = `game/${m[2]}`;
  }
  map.black = "";
  return map;
}

function unquoteRenpy(s) {
  return s.replace(/\\"/g, '"').replace(/\\\\/g, "\\");
}

function buildStory() {
  const assetMap = buildAssetMap();
  const text = readUtf8(path.join(project, "game", "story", "chapter_prologue.rpy"));
  const labels = {};
  let current = null;
  let menu = null;

  function step(type, data = {}) {
    if (!current) return;
    labels[current].push({ type, ...data });
  }

  for (const raw of text.split(/\r?\n/)) {
    const line = raw.trim();
    if (!line || line.startsWith("#")) continue;
    let m = line.match(/^label\s+([A-Za-z0-9_]+)\s*:/);
    if (m) {
      current = m[1];
      labels[current] = [];
      menu = null;
      continue;
    }
    if (!current) continue;

    if (menu) {
      m = line.match(/^"([^"]+)"\s*:/);
      if (m) {
        menu.options.push({ text: unquoteRenpy(m[1]), target: null });
        continue;
      }
      m = line.match(/^jump\s+([A-Za-z0-9_]+)/);
      if (m && menu.options.length) {
        menu.options[menu.options.length - 1].target = m[1];
        continue;
      }
    }

    if (line === "menu:") {
      menu = { type: "menu", options: [] };
      step("menu", { options: menu.options });
      continue;
    }
    m = line.match(/^scene\s+(.+)/);
    if (m) {
      const name = m[1].trim();
      step("scene", { name, src: assetMap[name] || "" });
      continue;
    }
    m = line.match(/^show\s+([A-Za-z0-9_]+)/);
    if (m) {
      const name = m[1];
      step("show", { name, src: assetMap[name] || "" });
      continue;
    }
    if (line.startsWith("hide ")) {
      step("hide");
      continue;
    }
    m = line.match(/^centered\s+"((?:[^"\\]|\\.)*)"/);
    if (m) {
      step("centered", { text: unquoteRenpy(m[1]) });
      continue;
    }
    m = line.match(/^pause\s+([0-9.]+)/);
    if (m) {
      step("pause", { seconds: Number(m[1]) || 0 });
      continue;
    }
    m = line.match(/^jump\s+([A-Za-z0-9_]+)/);
    if (m) {
      step("jump", { target: m[1] });
      continue;
    }
    if (line === "return") {
      step("end");
      continue;
    }
    m = line.match(/^"((?:[^"\\]|\\.)*)"\s+"((?:[^"\\]|\\.)*)"/);
    if (m) {
      step("say", { speaker: unquoteRenpy(m[1]), text: unquoteRenpy(m[2]) });
      continue;
    }
    m = line.match(/^"((?:[^"\\]|\\.)*)"/);
    if (m) {
      step("say", { speaker: "", text: unquoteRenpy(m[1]) });
    }
  }

  return { title, description, start: "chapter_prologue", labels };
}

function buildLightweightIndex() {
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>${title}</title>
  <meta name="description" content="${description}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="${title}">
  <meta property="og:description" content="${description}">
  <meta property="og:image" content="${image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${title}">
  <meta name="twitter:description" content="${description}">
  <meta name="twitter:image" content="${image}">
  <style>
    @font-face{font-family:ChuiMuo;src:url("game/fonts/NotoSansSC-Regular.subset.otf") format("opentype");font-display:swap}
    @font-face{font-family:ChuiMuo;font-weight:700;src:url("game/fonts/NotoSansSC-Bold.subset.otf") format("opentype");font-display:swap}
    *{box-sizing:border-box} html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#090806;color:#f3ead8;font-family:ChuiMuo,"Microsoft YaHei",sans-serif}
    #app{position:relative;width:100vw;height:100vh;background:#090806;isolation:isolate}
    .bg{position:absolute;inset:0;background:#090806 center/cover no-repeat;transition:opacity .45s ease;z-index:0}
    .bg::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.12),rgba(0,0,0,.35) 58%,rgba(0,0,0,.62));pointer-events:none}
    .char{position:absolute;right:4vw;bottom:0;max-height:min(82vh,760px);max-width:48vw;object-fit:contain;filter:drop-shadow(0 18px 28px rgba(0,0,0,.35));transition:opacity .35s ease,transform .35s ease;z-index:1}
    .top{position:absolute;left:16px;top:12px;z-index:5;display:flex;gap:10px;align-items:center}
    button{font-family:inherit;border:1px solid rgba(242,222,180,.42);background:rgba(21,17,12,.72);color:#f5ead2;border-radius:6px;padding:10px 14px;cursor:pointer}
    button:hover{background:rgba(70,46,30,.82)}
    .menuBtn{width:40px;height:40px;padding:0;font-size:24px;line-height:1}
    .panel{position:absolute;right:16px;top:62px;z-index:6;display:none;gap:8px;flex-direction:column}.panel.open{display:flex}
    .box{position:absolute;left:50%;bottom:4.5vh;transform:translateX(-50%);width:min(1180px,calc(100vw - 48px));min-height:168px;z-index:3;background:rgba(238,229,209,.88);color:#211912;border:1px solid rgba(80,54,30,.25);box-shadow:0 18px 42px rgba(0,0,0,.35);padding:26px 34px;border-radius:8px}
    .speaker{color:#8b3a3a;font-weight:700;font-size:24px;margin-bottom:10px;min-height:28px}
    .text{font-size:28px;line-height:1.72;letter-spacing:0}
    .centered{position:absolute;inset:0;display:grid;place-items:center;z-index:4;font-size:30px;text-align:center;background:#050505;color:#f4ead8;padding:24px}
    .choices{display:flex;flex-direction:column;gap:12px;margin-top:12px}.choices button{font-size:24px;padding:14px 18px;background:rgba(245,232,204,.95);color:#211912}
    .hint{position:absolute;right:28px;bottom:18px;color:rgba(33,25,18,.58);font-size:16px}.hidden{display:none!important}
    @media (max-width:760px){.char{right:-12vw;max-width:70vw;max-height:68vh}.box{width:calc(100vw - 24px);bottom:2vh;padding:18px 20px;min-height:150px}.text{font-size:22px}.speaker{font-size:20px}.centered{font-size:24px}}
  </style>
</head>
<body>
  <div id="app">
    <div id="bg" class="bg"></div>
    <img id="char" class="char hidden" alt="">
    <div class="top"><button id="menuBtn" class="menuBtn" aria-label="菜单">≡</button></div>
    <div id="panel" class="panel"><button id="saveBtn">保存</button><button id="loadBtn">读取</button><button id="restartBtn">重新开始</button><button onclick="location.href='renpy.html'">Ren'Py版</button></div>
    <div id="centered" class="centered hidden"></div>
    <div id="box" class="box"><div id="speaker" class="speaker"></div><div id="text" class="text"></div><div id="choices" class="choices hidden"></div><div class="hint">点击继续</div></div>
  </div>
  <script>
  (() => {
    const state = { label: "", index: 0, bg: "", char: "", waiting: false, story: null };
    const els = {
      bg: document.getElementById("bg"), char: document.getElementById("char"), box: document.getElementById("box"),
      speaker: document.getElementById("speaker"), text: document.getElementById("text"), choices: document.getElementById("choices"),
      centered: document.getElementById("centered"), panel: document.getElementById("panel")
    };
    const saveKey = "chuimuo-light-save";
    const preload = src => src ? new Promise(r => { const i = new Image(); i.onload = i.onerror = r; i.src = src; }) : Promise.resolve();
    const setBg = src => { state.bg = src; els.bg.style.backgroundImage = src ? 'url("' + src + '")' : "none"; };
    const setChar = src => { state.char = src; if (src) { els.char.src = src; els.char.classList.remove("hidden"); } else els.char.classList.add("hidden"); };
    const save = () => localStorage.setItem(saveKey, JSON.stringify({ label: state.label, index: state.index, bg: state.bg, char: state.char }));
    const restore = () => { const s = JSON.parse(localStorage.getItem(saveKey) || "null"); if (!s) return false; state.label=s.label; state.index=s.index; setBg(s.bg); setChar(s.char); run(); return true; };
    function goto(label){ state.label = label; state.index = 0; run(); }
    function next(){ if (state.waiting) return; state.index += 1; run(); }
    function showText(speaker, text){ els.centered.classList.add("hidden"); els.box.classList.remove("hidden"); els.choices.classList.add("hidden"); els.speaker.textContent = speaker || ""; els.text.textContent = text; }
    function run(){
      state.waiting = false;
      const steps = state.story.labels[state.label] || [];
      for (;;) {
        const step = steps[state.index];
        if (!step) { showText("", ""); return; }
        if (step.type === "scene") { setBg(step.src); setChar(""); state.index += 1; continue; }
        if (step.type === "show") { setChar(step.src); state.index += 1; continue; }
        if (step.type === "hide") { setChar(""); state.index += 1; continue; }
        if (step.type === "jump") { goto(step.target); return; }
        if (step.type === "pause") { state.index += 1; setTimeout(run, Math.min(1600, (step.seconds || 0) * 1000)); return; }
        if (step.type === "centered") { els.box.classList.add("hidden"); els.centered.textContent = step.text; els.centered.classList.remove("hidden"); return; }
        if (step.type === "say") { showText(step.speaker, step.text); return; }
        if (step.type === "menu") { showText("", ""); els.choices.innerHTML = ""; els.choices.classList.remove("hidden"); for (const opt of step.options) { const b=document.createElement("button"); b.textContent=opt.text; b.onclick=e=>{e.stopPropagation(); goto(opt.target);}; els.choices.appendChild(b); } return; }
        if (step.type === "end") { showText("", "剧终"); return; }
        state.index += 1;
      }
    }
    document.getElementById("menuBtn").onclick = e => { e.stopPropagation(); els.panel.classList.toggle("open"); };
    document.getElementById("saveBtn").onclick = e => { e.stopPropagation(); save(); };
    document.getElementById("loadBtn").onclick = e => { e.stopPropagation(); restore(); };
    document.getElementById("restartBtn").onclick = e => { e.stopPropagation(); localStorage.removeItem(saveKey); setBg(""); setChar(""); goto(state.story.start); };
    document.body.addEventListener("click", () => next());
    document.body.addEventListener("keydown", e => { if (e.key === " " || e.key === "Enter") next(); });
    fetch("story.json?v=20260630-light").then(r => r.json()).then(async story => {
      state.story = story; state.label = story.start;
      const first = story.labels[story.start].find(s => s.type === "scene" && s.src);
      if (first) await preload(first.src);
      run();
    }).catch(err => showText("加载失败", String(err)));
  })();
  </script>
</body>
</html>`;
}
