#!/usr/bin/env node
// Verifies that asset_list.md and art_prompts.jsonl describe the same 60 files.
// This script does not generate or transform images.

const fs = require("fs");
const path = require("path");

const project = path.resolve(__dirname, "..");
const assetListPath = path.join(project, "game", "images", "asset_list.md");
const promptsPath = path.join(project, "spec", "art_prompts.jsonl");

function readText(file) {
  if (!fs.existsSync(file)) throw new Error(`Missing file: ${file}`);
  return fs.readFileSync(file, "utf8");
}

const assetText = readText(assetListPath);
const listNames = [...new Set([...assetText.matchAll(/`([^`]+\.webp)`/g)].map((match) => match[1]))].sort();
const promptRows = readText(promptsPath)
  .trim()
  .split(/\r?\n/)
  .filter(Boolean)
  .map((line, index) => {
    try {
      return JSON.parse(line);
    } catch (error) {
      throw new Error(`Invalid JSONL at line ${index + 1}: ${error.message}`);
    }
  });
const promptNames = [...new Set(promptRows.map((row) => row.filename))].sort();

const missingFromPrompts = listNames.filter((name) => !promptNames.includes(name));
const missingFromList = promptNames.filter((name) => !listNames.includes(name));
const badRows = promptRows.filter((row) => {
  const widthOk = row.width === null || Number.isInteger(row.width);
  return !row.filename ||
    !row.category ||
    !widthOk ||
    !Number.isInteger(row.height) ||
    typeof row.transparent !== "boolean" ||
    !row.prompt_positive ||
    !row.prompt_negative ||
    typeof row.max_size_mb !== "number";
});

console.log(`asset_list.md files: ${listNames.length}`);
console.log(`art_prompts.jsonl rows: ${promptRows.length}`);
console.log(`art_prompts.jsonl unique filenames: ${promptNames.length}`);

if (missingFromPrompts.length) console.error(`Missing from art_prompts.jsonl:\n${missingFromPrompts.join("\n")}`);
if (missingFromList.length) console.error(`Missing from asset_list.md:\n${missingFromList.join("\n")}`);
if (badRows.length) console.error(`Malformed art prompt rows:\n${badRows.map((row) => row.filename || "<missing filename>").join("\n")}`);

if (
  listNames.length !== 60 ||
  promptRows.length !== 60 ||
  promptNames.length !== 60 ||
  missingFromPrompts.length ||
  missingFromList.length ||
  badRows.length
) {
  process.exit(1);
}

console.log("Asset manifest consistency check passed: 60 filenames match exactly.");
