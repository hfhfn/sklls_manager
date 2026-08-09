#!/usr/bin/env node
/**
 * 独立识图脚本 — 调用智谱 GLM 视觉模型，按量付费。
 *
 * 双模型自动回退：
 *   优先用 VISION_MODEL_PRIMARY (默认 GLM-4.6V-Flash)。
 *   若主模型返回 HTTP 429（限流“访问量过大”），自动切换到
 *   VISION_MODEL_FALLBACK (默认 GLM-4.1V-Thinking-Flash) 重试。
 *
 * 用法:
 *   node vision.js <图片路径> [问题]
 *   node vision.js --url <图片链接> [问题]
 *
 * 环境变量:
 *   VISION_MODEL_PRIMARY  主模型（默认 GLM-4.6V-Flash）
 *   VISION_MODEL_FALLBACK 限流回退模型（默认 GLM-4.1V-Thinking-Flash）
 *   VISION_MODEL          旧单模型变量，若设置了则固定用它（不回退）
 *   VISION_API_KEY        或 CUSTOM_GLM_API_KEY
 *   VISION_BASE_URL       默认 https://open.bigmodel.cn/api/paas/v4
 *   VISION_MAX_RETRIES    429 回退尝试次数（默认 1，即最多切 1 个备用模型）
 */

const fs = require("fs");
const path = require("path");
const https = require("https");
const http = require("http");

// 尝试加载 .env（先找当前目录，再找脚本所在目录）
try { require("dotenv").config(); } catch {}
try { require("dotenv").config({ path: path.resolve(__dirname, ".env") }); } catch {}

const BASE_URL = process.env.VISION_BASE_URL || "https://open.bigmodel.cn/api/paas/v4";
const API_KEY = process.env.VISION_API_KEY || process.env.CUSTOM_GLM_API_KEY || "sk-xxx";

// 模型配置：优先单模型（旧变量），否则双模型回退
const LEGACY_MODEL = process.env.VISION_MODEL || "";
const PRIMARY_MODEL = process.env.VISION_MODEL_PRIMARY || "GLM-4.6V-Flash";
const FALLBACK_MODEL = process.env.VISION_MODEL_FALLBACK || "GLM-4.1V-Thinking-Flash";
const MAX_FALLBACK_RETRIES = parseInt(process.env.VISION_MAX_RETRIES || "1", 10);

function parseArgs() {
  const argv = process.argv.slice(2);
  let imageSource = "", prompt = "", isUrl = false;

  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--url" && argv[i + 1]) {
      isUrl = true;
      imageSource = argv[++i];
    } else if (!imageSource && !argv[i].startsWith("--")) {
      imageSource = argv[i];
    } else if (imageSource && !argv[i].startsWith("--")) {
      prompt = prompt ? prompt + " " + argv[i] : argv[i];
    }
  }
  if (!prompt) prompt = "请详细描述这张图片的内容。";
  return { imageSource, prompt, isUrl };
}

function resolveImageUrl(source, isUrl) {
  if (isUrl) return source;
  const resolved = path.resolve(source);
  if (!fs.existsSync(resolved)) throw new Error(`文件不存在: ${resolved}`);
  const ext = path.extname(resolved).toLowerCase().replace(".", "");
  const mimeMap = { jpg: "jpeg", jpeg: "jpeg", png: "png", gif: "gif", webp: "webp", bmp: "bmp" };
  const data = fs.readFileSync(resolved);
  return `data:image/${mimeMap[ext] || "jpeg"};base64,${data.toString("base64")}`;
}

function request(model, payload) {
  const url = new URL(BASE_URL.replace(/\/?$/, "/") + "chat/completions");
  const body = JSON.stringify(payload);
  const transport = url.protocol === "https:" ? https : http;

  return new Promise((resolve, reject) => {
    const req = transport.request(url, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${API_KEY}`,
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(body),
      },
    }, (res) => {
      let data = "";
      res.on("data", (c) => data += c);
      res.on("end", () => {
        // 把 429 单独抛出来，方便上层做模型回退
        if (res.statusCode === 429) {
          return reject(Object.assign(new Error(`API 429 限流: ${data.slice(0, 300)}`), { statusCode: 429 }));
        }
        if (res.statusCode >= 400) return reject(Object.assign(
          new Error(`API ${res.statusCode}: ${data.slice(0, 300)}`), { statusCode: res.statusCode }
        ));
        try {
          resolve(JSON.parse(data)?.choices?.[0]?.message?.content || data);
        } catch { resolve(data); }
      });
    });
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

async function callVision(model, imageUrl, prompt) {
  return request(model, {
    model,
    messages: [{ role: "user", content: [
      { type: "image_url", image_url: { url: imageUrl } },
      { type: "text", text: prompt },
    ]}],
    stream: false,
    max_tokens: 1024,
  });
}

async function main() {
  if (!API_KEY) {
    console.error("请设置 CUSTOM_GLM_API_KEY 环境变量或在 .env 文件中配置。");
    process.exit(1);
  }
  const { imageSource, prompt, isUrl } = parseArgs();
  if (!imageSource) {
    console.error("用法: node vision.js <图片路径> [问题]");
    console.error("      node vision.js --url <图片链接> [问题]");
    process.exit(1);
  }

  try {
    const imageUrl = resolveImageUrl(imageSource, isUrl);

    // 固定单模型模式（旧行为）
    if (LEGACY_MODEL) {
      const result = await callVision(LEGACY_MODEL, imageUrl, prompt);
      console.log(result);
      return;
    }

    // 双模型回退模式
    let attempts = 0;
    let lastErr = null;
    const modelQueue = [PRIMARY_MODEL];
    for (let i = 0; i < Math.max(0, MAX_FALLBACK_RETRIES); i++) {
      modelQueue.push(FALLBACK_MODEL);
    }

    for (const model of modelQueue) {
      attempts++;
      try {
        const result = await callVision(model, imageUrl, prompt);
        if (attempts > 1) {
          console.error(`[vision] 主模型 ${PRIMARY_MODEL} 限流，已用 ${model} 成功。`);
        }
        console.log(result);
        return;
      } catch (err) {
        lastErr = err;
        if (err.statusCode === 429) {
          console.error(`[vision] ${model} 返回 429 限流，切换备用模型重试...`);
          continue;
        }
        throw err; // 非 429 错误不重试
      }
    }

    // 所有模型都 429
    console.error(`[vision] 所有模型均限流 (${modelQueue.join(", ")}): ${lastErr?.message || lastErr}`);
    process.exit(1);
  } catch (err) {
    console.error("识图失败:", err.message);
    process.exit(1);
  }
}

main();