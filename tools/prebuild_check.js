#!/usr/bin/env node
// prebuild_check: run before Ren'Py/renpyweb build. This script does not generate art.

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const project = path.resolve(__dirname, "..");
const root = path.resolve(project, "..");
const buildWeb = path.join(project, "build-web");
const assetValidator = path.join(root, "work", "tests", "validate_assets_ready.js");

function runNode(script) {
  const result = spawnSync(process.execPath, [script], {
    cwd: root,
    encoding: "utf8"
  });
  if (result.stdout) process.stdout.write(result.stdout);
  if (result.stderr) process.stderr.write(result.stderr);
  if (result.status !== 0) process.exit(result.status || 1);
}

function hasCommand(command) {
  const probe = process.platform === "win32" ? "where" : "which";
  const result = spawnSync(probe, [command], { encoding: "utf8" });
  return result.status === 0;
}

console.log("prebuild_check: verifying external assets.");
runNode(assetValidator);

if (!fs.existsSync(buildWeb)) fs.mkdirSync(buildWeb, { recursive: true });

if (!hasCommand("renpy")) {
  console.warn("Ren'Py executable not found on PATH. Use the Ren'Py launcher or add renpy to PATH before automated builds.");
}

console.log(`prebuild_check: build-web directory ready at ${buildWeb}`);
