#!/usr/bin/env node
// write_acceptance_report: creates a final_acceptance_report.md snapshot after verification.

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const project = path.resolve(__dirname, "..");
const root = path.resolve(project, "..");
const output = path.join(project, "final_acceptance_report.md");
const template = path.join(project, "spec", "final_acceptance_template.md");

function run(command, args) {
  const result = spawnSync(command, args, { cwd: root, encoding: "utf8" });
  return {
    command: [command, ...args].join(" "),
    status: result.status,
    stdout: result.stdout.trim(),
    stderr: result.stderr.trim()
  };
}

const checks = [
  run(process.execPath, ["work/tests/validate_project.js"]),
  run(process.execPath, ["work/tests/validate_assets_ready.js"])
];

const body = fs.readFileSync(template, "utf8");
const lines = [
  body.trim(),
  "",
  "## 自动化检查输出",
  "",
  ...checks.flatMap((check) => [
    `### ${check.command}`,
    "",
    `Exit code: ${check.status}`,
    "",
    "```text",
    check.stdout || check.stderr || "(no output)",
    "```",
    ""
  ])
];

fs.writeFileSync(output, lines.join("\n"), "utf8");
console.log(`write_acceptance_report: wrote ${output}`);
