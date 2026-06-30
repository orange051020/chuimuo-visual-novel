#!/usr/bin/env node
// Generates external art assets through Doubao/Volcengine Ark image API.
// This script calls an external image-generation service. It does not draw
// placeholders or synthesize images locally.

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const project = path.resolve(__dirname, "..");
const root = path.resolve(project, "..");
const promptsFile = path.join(project, "spec", "art_prompts.jsonl");
const dropDir = path.join(root, "external-art-drop");
const logDir = path.join(root, "logs");
const failedLog = path.join(logDir, "art_generation_failed.log");
const endpoint = process.env.DOUBAO_IMAGE_ENDPOINT || "https://ark.cn-beijing.volces.com/api/v3/images/generations";
const model = process.env.DOUBAO_MODEL || "doubao-seedream-4-0-250828";
const key = process.env.DOUBAO_API_KEY;
const force = process.argv.includes("--force");
const smoke = process.argv.includes("--smoke");
const startArg = Number((process.argv.find((arg) => arg.startsWith("--start=")) || "").split("=")[1] || 0);
const limitArg = Number((process.argv.find((arg) => arg.startsWith("--limit=")) || "").split("=")[1] || 0);

const globalPositive = "超高清，精细水墨笔触，传统中国水墨画，古宣纸纹理，褪色老旧卷轴质感，低饱和度，柔和水墨晕染边缘，分层薄雾氛围，极简留白，纯2D平面插画，无3D渲染，复古 muted 色调，边缘平滑清晰，对标《无悔华夏》美术风格";
const globalNegative = "写实照片，真人五官，清晰面部细节，高饱和亮色，卡通动漫，纯色几何方块，文字水印，模糊像素化，锯齿边缘，畸形变形，现代元素，塑料质感，矢量图形，硬边锐边，低画质颗粒感";

if (!key) {
  console.error("DOUBAO_API_KEY is missing.");
  process.exit(1);
}

fs.mkdirSync(dropDir, { recursive: true });
fs.mkdirSync(logDir, { recursive: true });

function readRows() {
  return fs.readFileSync(promptsFile, "utf8")
    .trim()
    .split(/\r?\n/)
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

function isCharacterAsset(asset) {
  return asset.filename.startsWith("char_") || asset.filename.startsWith("group_");
}

function isFullOrGroup(asset) {
  return asset.filename.includes("_full") || asset.filename.startsWith("group_");
}

function isCloseup(asset) {
  return asset.filename.includes("_closeup_");
}

function targetSpec(asset) {
  if (!isCharacterAsset(asset) || isCloseup(asset)) return { width: 1920, height: 1080, alpha: false, maxKb: 2048 };
  return { width: null, height: isFullOrGroup(asset) ? 1000 : 900, alpha: true, maxKb: 500 };
}

function promptFor(asset, retryIndex = 0) {
  const transparent = isCharacterAsset(asset) && !isCloseup(asset);
  const reinforce = retryIndex > 0 ? "，强化水墨国画、古卷轴、宣纸纹理、低饱和剪影风格" : "";
  const transparentText = transparent
    ? "，纯剪影，无五官，无面部细节，透明背景，主体外完全透明，边缘自然水墨晕染"
    : "";
  return `${globalPositive}${reinforce}。${asset.prompt_positive}${transparentText}`;
}

function negativeFor(asset) {
  return `${globalNegative}，${asset.prompt_negative}`;
}

function requestBodies(asset, retryIndex) {
  const spec = targetSpec(asset);
  const transparent = isCharacterAsset(asset) && !isCloseup(asset);
  const prompt = promptFor(asset, retryIndex);
  const negative = negativeFor(asset);
  const landscapeSize = spec.width && spec.height ? `${spec.width}x${spec.height}` : (spec.height === 1000 ? "1024x1536" : "1024x1024");
  return [
    {
      model,
      prompt,
      negative_prompt: negative,
      width: spec.width || (spec.height === 1000 ? 1000 : 900),
      height: spec.height,
      image_format: "webp",
      quality: "high",
      transparent_background: transparent,
      response_format: "url",
      watermark: false
    },
    {
      model,
      prompt,
      negative_prompt: negative,
      size: landscapeSize,
      response_format: "url",
      watermark: false,
      ...(transparent ? { transparent_background: true } : {})
    },
    {
      model,
      prompt,
      size: landscapeSize,
      response_format: "url",
      watermark: false
    }
  ];
}

async function callApi(body) {
  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${key}`
    },
    body: JSON.stringify(body)
  });
  const text = await response.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch {
    throw new Error(`HTTP ${response.status}: ${text.slice(0, 500)}`);
  }
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${JSON.stringify(json).slice(0, 1000)}`);
  }
  return json;
}

function extractImagePayload(json) {
  const data = Array.isArray(json.data) ? json.data[0] : null;
  const directUrl = data?.url || data?.image_url || data?.image_urls?.[0] || json.url || json.image_url || json.image_urls?.[0];
  const b64 = data?.b64_json || data?.image_base64 || json.b64_json || json.image_base64;
  if (b64) return { type: "base64", value: b64 };
  if (directUrl) return { type: "url", value: directUrl };
  throw new Error(`No image URL/base64 in response: ${JSON.stringify(json).slice(0, 1000)}`);
}

async function downloadImage(payload, rawPath) {
  if (payload.type === "base64") {
    fs.writeFileSync(rawPath, Buffer.from(payload.value, "base64"));
    return;
  }
  const response = await fetch(payload.value);
  if (!response.ok) throw new Error(`Image download failed HTTP ${response.status}: ${payload.value}`);
  fs.writeFileSync(rawPath, Buffer.from(await response.arrayBuffer()));
}

function normalizeWithPython(rawPath, finalPath, asset) {
  const spec = targetSpec(asset);
  const script = `
from PIL import Image
import os
src = r'''${rawPath.replace(/\\/g, "\\\\")}'''
dst = r'''${finalPath.replace(/\\/g, "\\\\")}'''
target_w = ${spec.width === null ? "None" : spec.width}
target_h = ${spec.height}
alpha = ${spec.alpha ? "True" : "False"}
max_kb = ${spec.maxKb}
im = Image.open(src)
if alpha:
    im = im.convert("RGBA")
    # If the provider returned an opaque image despite transparency request,
    # remove near-white/near-green flat backgrounds conservatively.
    if im.getextrema()[3][0] == 255:
        px = im.load()
        w, h = im.size
        samples = [px[0,0], px[w-1,0], px[0,h-1], px[w-1,h-1]]
        bg = tuple(sum(s[i] for s in samples)//len(samples) for i in range(3))
        for y in range(h):
            for x in range(w):
                r,g,b,a = px[x,y]
                if abs(r-bg[0]) < 28 and abs(g-bg[1]) < 28 and abs(b-bg[2]) < 28:
                    px[x,y] = (r,g,b,0)
    ratio = target_h / im.size[1]
    new_w = max(1, round(im.size[0] * ratio))
    im = im.resize((new_w, target_h), Image.Resampling.LANCZOS)
else:
    im = im.convert("RGB")
    im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
quality = 90
while quality >= 45:
    im.save(dst, "WEBP", quality=quality, method=6)
    if os.path.getsize(dst) <= max_kb * 1024:
        break
    quality -= 5
`;
  const py = process.env.CODEX_PYTHON || "C:\\Users\\12726\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe";
  const result = spawnSync(py, ["-c", script], { encoding: "utf8" });
  if (result.status !== 0) {
    throw new Error(`Pillow normalize failed: ${result.stderr || result.stdout}`);
  }
}

async function generateOne(asset) {
  const finalPath = path.join(dropDir, asset.filename);
  if (!force && fs.existsSync(finalPath)) {
    console.log(`skip existing ${asset.filename}`);
    return true;
  }
  const rawPath = path.join(dropDir, `${asset.filename}.raw`);
  let lastError = null;
  for (let attempt = 0; attempt < 3; attempt++) {
    const bodies = requestBodies(asset, attempt);
    for (const body of bodies) {
      try {
        console.log(`generate ${asset.filename} attempt=${attempt + 1}`);
        const json = await callApi(body);
        await downloadImage(extractImagePayload(json), rawPath);
        normalizeWithPython(rawPath, finalPath, asset);
        if (fs.existsSync(rawPath)) fs.unlinkSync(rawPath);
        console.log(`ok ${asset.filename}`);
        return true;
      } catch (error) {
        lastError = error;
        console.warn(`failed ${asset.filename}: ${error.message}`);
      }
    }
  }
  fs.appendFileSync(failedLog, `${asset.filename}\t${lastError?.message || "unknown error"}\n`, "utf8");
  return false;
}

async function main() {
  if (fs.existsSync(failedLog)) fs.unlinkSync(failedLog);
  const rows = readRows().sort((a, b) => Number(isCharacterAsset(a)) - Number(isCharacterAsset(b)));
  const slice = smoke ? rows.slice(0, 1) : rows.slice(startArg, limitArg ? startArg + limitArg : undefined);
  let failures = 0;
  for (const asset of slice) {
    const ok = await generateOne(asset);
    if (!ok) failures++;
    if (failures > Math.max(1, Math.floor(slice.length * 0.1))) {
      throw new Error(`Failure rate exceeded 10%: ${failures}/${slice.length}`);
    }
  }
  console.log(`Doubao generation finished. total=${slice.length} failures=${failures}`);
  if (failures) process.exit(1);
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
