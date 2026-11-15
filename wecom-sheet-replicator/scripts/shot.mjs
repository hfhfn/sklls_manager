#!/usr/bin/env node
// 用已有会话截图，用于核对合并单元格 / 序号 / 视觉结构。
//   node shot.mjs "<docUrl>" <tabId> out.png [--w 1600] [--h 1400] [--cell A149] [--wait 11000]
//
// --cell 会尝试在左上角"名称框"里输入坐标跳转（能跳就直接定位到目标区域）。
import path from "node:path";
import fs from "node:fs";
import { pathToFileURL } from "node:url";
import { createRequire } from "node:module";

const WORKDIR = path.resolve(process.env.WECOM_WORKDIR ?? path.join(process.cwd(), ".wecom-work"));

const argv = process.argv.slice(2);
const flags = {};
const pos = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i].startsWith("--")) {
    const [k, v] = argv[i].slice(2).split("=");
    flags[k] = v ?? (argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : true);
  } else pos.push(argv[i]);
}
const [url, tab, out = "shot.png"] = pos;
if (!url || !tab) {
  console.error('用法: shot.mjs "<docUrl>" <tabId> out.png [--w 1600] [--h 1400] [--cell A149]');
  process.exit(1);
}
const W = Number(flags.w ?? 1600);
const H = Number(flags.h ?? 1400);

const req = createRequire(path.join(WORKDIR, "noop.js"));
const { chromium } = req("playwright");
const { SessionManager } = await import(pathToFileURL(path.join(WORKDIR, "package/dist/auth/session.js")).href);

const session = new SessionManager();
const raw = session.loadCookies();
if (!raw) {
  console.error("没有会话，先跑 node scripts/login.mjs");
  process.exit(1);
}
const cookies = raw.map((c) => ({ ...c, expires: c.expires > 0 ? c.expires : -1 }));

const target = new URL(url);
target.searchParams.set("tab", tab);

const browser = await chromium.launch({ headless: true, channel: "chrome" });
const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1.5 });
await ctx.addCookies(cookies);
const page = await ctx.newPage();
await page.goto(target.toString(), { waitUntil: "domcontentloaded" });
await page.waitForTimeout(Number(flags.wait ?? 11000));

if (flags.cell) {
  let jumped = false;
  for (const inp of await page.$$("input")) {
    const box = await inp.boundingBox();
    if (!box || box.y > 140 || box.x > 220 || box.width > 200) continue;
    await inp.click();
    await page.keyboard.press("Control+a");
    await page.keyboard.type(String(flags.cell));
    await page.keyboard.press("Enter");
    await page.waitForTimeout(3200);
    jumped = true;
    break;
  }
  if (!jumped) console.error("没找到名称框，截的是默认位置");
}

fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
await page.screenshot({ path: out });
console.log("saved", out, `${W}x${H}`);
await browser.close();
