#!/usr/bin/env node
// import_external_assets: copies externally generated WebP files into game/images.
// This script does not generate or transform images.

const fs = require("fs");
const path = require("path");

const project = path.resolve(__dirname, "..");
const root = path.resolve(project, "..");
const dropDir = path.join(root, "external-art-drop");
const assetList = path.join(project, "game", "images", "asset_list.md");
const backgroundDir = path.join(project, "game", "images", "background");
const characterDir = path.join(project, "game", "images", "character");
const dryRun = process.argv.includes("--dry-run");

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

function hasWebpHeader(file) {
  const buf = fs.readFileSync(file);
  return buf.slice(0, 4).toString("ascii") === "RIFF" && buf.slice(8, 12).toString("ascii") === "WEBP";
}

if (!fs.existsSync(dropDir)) fs.mkdirSync(dropDir, { recursive: true });
fs.mkdirSync(backgroundDir, { recursive: true });
fs.mkdirSync(characterDir, { recursive: true });

const required = parseAssets();
const allowed = new Set(required);
const present = fs.readdirSync(dropDir).filter((name) => name.endsWith(".webp"));
const unknown = present.filter((name) => !allowed.has(name));
const missing = required.filter((name) => !present.includes(name));
const badFormat = present.filter((name) => !hasWebpHeader(path.join(dropDir, name)));

if (unknown.length || missing.length || badFormat.length) {
  if (unknown.length) console.error(`Unknown files in external-art-drop:\n${unknown.join("\n")}`);
  if (missing.length) console.error(`Missing files in external-art-drop:\n${missing.join("\n")}`);
  if (badFormat.length) console.error(`Not valid WebP files:\n${badFormat.join("\n")}`);
  process.exit(1);
}

for (const name of required) {
  const source = path.join(dropDir, name);
  const target = path.join(isCharacterAsset(name) ? characterDir : backgroundDir, name);
  if (dryRun) {
    console.log(`[dry-run] ${source} -> ${target}`);
  } else {
    fs.copyFileSync(source, target);
    console.log(`Imported ${name}`);
  }
}

console.log(dryRun ? "Dry run passed." : "External assets imported.");
