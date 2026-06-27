#!/usr/bin/env node
// inject_web_meta: insert share meta tags into renpyweb output. This script does not generate art.

const fs = require("fs");
const path = require("path");

const project = path.resolve(__dirname, "..");
const indexPath = path.join(project, "build-web", "index.html");
const metaPath = path.join(project, "web-meta.html");
const markerStart = "<!-- chuimuo-share-meta:start -->";
const markerEnd = "<!-- chuimuo-share-meta:end -->";

function fail(message) {
  console.error(`inject_web_meta: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(indexPath)) fail(`missing build-web index: ${indexPath}`);
if (!fs.existsSync(metaPath)) fail(`missing web-meta.html: ${metaPath}`);

const index = fs.readFileSync(indexPath, "utf8");
const meta = `${markerStart}\n${fs.readFileSync(metaPath, "utf8").trim()}\n${markerEnd}`;

let next;
const existing = new RegExp(`${markerStart}[\\s\\S]*?${markerEnd}`);
if (existing.test(index)) {
  next = index.replace(existing, meta);
} else if (index.includes("</head>")) {
  next = index.replace("</head>", `${meta}\n</head>`);
} else {
  fail("cannot find </head> in build-web/index.html");
}

fs.writeFileSync(indexPath, next, "utf8");
console.log("inject_web_meta: web-meta.html injected into build-web/index.html");
