#!/usr/bin/env node
// Fallback web package builder used when Ren'Py SDK web_build command is unavailable.
// It copies the installed Ren'Py web runtime and packages project game assets.

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const project = path.resolve(__dirname, "..");
const root = path.resolve(project, "..");
const out = path.join(project, "build-web");
const game = path.join(project, "game");
const sdkWeb = "C:\\Users\\12726\\Documents\\Codex\\tools\\renpy-sdk\\renpy-8.5.3-sdk\\web";

function copyDir(src, dst) {
  fs.mkdirSync(dst, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dst, entry.name);
    if (entry.isDirectory()) copyDir(s, d);
    else fs.copyFileSync(s, d);
  }
}

function run(command, args) {
  const result = spawnSync(command, args, { cwd: root, encoding: "utf8" });
  if (result.stdout) process.stdout.write(result.stdout);
  if (result.stderr) process.stderr.write(result.stderr);
  if (result.status !== 0) process.exit(result.status || 1);
}

if (!fs.existsSync(sdkWeb)) {
  console.error(`Missing Ren'Py web runtime: ${sdkWeb}`);
  process.exit(1);
}

fs.rmSync(out, { recursive: true, force: true });
copyDir(sdkWeb, out);

const archive = path.join(out, "game.zip");
if (fs.existsSync(archive)) fs.unlinkSync(archive);

const ps = [
  "$ErrorActionPreference='Stop'",
  `Compress-Archive -Path '${game.replace(/'/g, "''")}\\*' -DestinationPath '${archive.replace(/'/g, "''")}' -Force`
].join("; ");
run("powershell.exe", ["-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps]);

const manifestPath = path.join(out, "manifest.json");
let manifest = {};
if (fs.existsSync(manifestPath)) {
  manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
}
manifest["package"] = "game.zip";
manifest["name"] = "风暴中的大顺朝·垂暮序章";
fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2), "utf8");

const indexPath = path.join(out, "index.html");
let index = fs.readFileSync(indexPath, "utf8");
index = index.replace(/<title>.*?<\/title>/, "<title>风暴中的大顺朝·垂暮序章</title>");
fs.writeFileSync(indexPath, index, "utf8");

console.log(`Fallback web build written to ${out}`);
