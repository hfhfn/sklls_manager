#!/usr/bin/env node
// 登录：用持久化 profile 打开企业微信文档，扫码一次，把 cookie 存进 ~/.wecomdocs-cli/session.json
//
//   node login.mjs                       # 默认打开 doc.weixin.qq.com
//   node login.mjs "<docUrl>"            # 直接打开某个文档
//   node login.mjs --force               # 忽略已有会话，强制重登
//
// 为什么用持久化 profile：cookie 存在 profile 里，下次再跑不用重新扫码；
// 而且不碰用户正在使用的 Chrome（运行中的 profile 是锁住的，读不了）。
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { createRequire } from "node:module";

const WORKDIR = path.resolve(process.env.WECOM_WORKDIR ?? path.join(process.cwd(), ".wecom-work"));
const PROFILE = path.join(WORKDIR, "browser-profile");
const args = process.argv.slice(2);
const force = args.includes("--force");
const url = args.find((a) => a.startsWith("http")) ?? "https://doc.weixin.qq.com/";

const need = (cond, msg) => {
  if (!cond) {
    console.error("错误：" + msg);
    process.exit(1);
  }
};
need(fs.existsSync(path.join(WORKDIR, "package/dist/auth/session.js")), `先跑 scripts/setup.sh（工作目录 ${WORKDIR}）`);

const req = createRequire(path.join(WORKDIR, "noop.js"));
const { chromium } = req("playwright");
const { SessionManager } = await import(pathToFileURL(path.join(WORKDIR, "package/dist/auth/session.js")).href);

const session = new SessionManager();

if (!force && session.loadCookies() && !session.isExpired()) {
  console.log(`已有有效会话：${session.sessionPath}（要重登加 --force）`);
  process.exit(0);
}

fs.mkdirSync(PROFILE, { recursive: true });
console.log("打开浏览器，请用企业微信扫码登录（最长等 5 分钟）...");

let ctx;
try {
  ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: false,
    channel: "chrome",
    viewport: { width: 1280, height: 860 },
    args: ["--no-first-run", "--no-default-browser-check"],
  });
} catch (e) {
  console.error(
    `启动 Chrome 失败：${e.message}\n` +
      "系统需要安装 Chrome。没有的话装一个，或改成 chromium：\n" +
      `  node ${path.join(WORKDIR, "node_modules/playwright/cli.js")} install chromium`
  );
  process.exit(1);
}

const page = ctx.pages()[0] ?? (await ctx.newPage());
await page.goto(url, { waitUntil: "domcontentloaded" });

const deadline = Date.now() + 300_000;
let ok = false;
while (Date.now() < deadline) {
  const cookies = await ctx.cookies();
  if (cookies.some((c) => c.name === "wedoc_sid" && c.value)) {
    ok = true;
    break;
  }
  await page.waitForTimeout(2000);
}

if (!ok) {
  console.error("超时，没拿到 wedoc_sid。确认扫码完成、且这个账号有该文档的访问权限。");
  await ctx.close();
  process.exit(1);
}

const cookies = (await ctx.cookies()).map((c) => ({
  name: c.name,
  value: c.value,
  domain: c.domain,
  path: c.path,
  expires: c.expires,
  httpOnly: c.httpOnly,
  secure: c.secure,
  sameSite: c.sameSite,
}));
session.saveCookies(cookies);
console.log(`登录成功，已保存 ${cookies.length} 个 cookie -> ${session.sessionPath}`);
await ctx.close();
