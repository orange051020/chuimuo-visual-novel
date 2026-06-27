#!/usr/bin/env node
// Writes a text report of missing externally generated assets. Does not generate images.

const fs = require("fs");
const path = require("path");

const project = path.resolve(__dirname, "..");
const root = path.resolve(project, "..");
const assetList = path.join(project, "game", "images", "asset_list.md");
const dropDir = path.join(root, "external-art-drop");
const output = path.join(project, "missing_assets_report.md");

function readText(file) {
  if (!fs.existsSync(file)) throw new Error(`Missing file: ${file}`);
  return fs.readFileSync(file, "utf8");
}

function parseAssets() {
  const text = readText(assetList);
  return [...new Set([...text.matchAll(/`([^`]+\.webp)`/g)].map((match) => match[1]))];
}

function isCharacterAsset(name) {
  return name.startsWith("char_") || name.startsWith("group_");
}

const required = parseAssets();
const present = fs.existsSync(dropDir) ? fs.readdirSync(dropDir).filter((name) => name.endsWith(".webp")) : [];
const presentSet = new Set(present);
const missing = required.filter((name) => !presentSet.has(name));

const lines = [
  "# Missing External Art Assets",
  "",
  "Codex must not generate images. The following files must be produced by the external text-to-image pipeline and placed in `external-art-drop/`.",
  "",
  `Total required: ${required.length}`,
  `Present in external-art-drop: ${present.length}`,
  `Missing: ${missing.length}`,
  "",
  "## Missing Background/UI Assets",
  "",
  ...missing.filter((name) => !isCharacterAsset(name)).map((name) => `- ${name}`),
  "",
  "## Missing Character/Group Assets",
  "",
  ...missing.filter(isCharacterAsset).map((name) => `- ${name}`),
  "",
  "## Next Commands",
  "",
  "```bash",
  "node chuimuo-visual-novel/tools/import_external_assets.js --dry-run",
  "node chuimuo-visual-novel/tools/import_external_assets.js",
  "node work/tests/validate_assets_ready.js",
  "node chuimuo-visual-novel/tools/prebuild_check.js",
  "```",
  ""
];

fs.writeFileSync(output, lines.join("\n"), "utf8");
console.log(`Missing asset report written: ${output}`);
if (missing.length) process.exit(1);
