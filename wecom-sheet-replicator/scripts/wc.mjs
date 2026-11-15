#!/usr/bin/env node
// 企业微信在线表格读取 CLI
//
//   node wc.mjs tabs  "<docUrl>"
//   node wc.mjs shape "<docUrl>" <tabId> [--rows 10]
//   node wc.mjs row   "<docUrl>" <tabId> <rowNo>
//   node wc.mjs rows  "<docUrl>" <tabId> <from> <to> [--out rows_<tab>.json] [--concurrency 4]
//   node wc.mjs fetch "<docUrl>" <tabId> [--out rows_<tab>.json] [--empty 60] [--max 5000] [--concurrency 4]
//
// 环境变量 WECOM_WORKDIR 指向 setup.sh 的工作目录（默认 ./.wecom-work）
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { inflateSync } from "node:zlib";
import { parse, pick, textOf, findLinkRecords } from "./proto.mjs";

const WORKDIR = path.resolve(process.env.WECOM_WORKDIR ?? path.join(process.cwd(), ".wecom-work"));
const load = (rel) => import(pathToFileURL(path.join(WORKDIR, rel)).href);

function need(cond, msg) {
  if (!cond) {
    console.error("错误：" + msg);
    process.exit(1);
  }
}

// ---------- 参数 ----------
const argv = process.argv.slice(2);
const flags = {};
const pos = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i].startsWith("--")) {
    const [k, v] = argv[i].slice(2).split("=");
    flags[k] = v ?? (argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : true);
  } else pos.push(argv[i]);
}
const [cmd, urlArg, tabArg, a3, a4] = pos;
need(cmd, "用法见文件头注释");

// ---------- URL ----------
function parseDocUrl(u) {
  let url;
  try {
    url = new URL(u);
  } catch {
    console.error("错误：链接格式不对，需要完整的 https://doc.weixin.qq.com/... 链接");
    process.exit(1);
  }
  const m = url.pathname.match(/\/(sheet|doc|slide|form)\/([A-Za-z0-9_-]+)/);
  const padId = m ? m[2] : url.searchParams.get("id");
  need(padId, "链接里找不到文档 id（形如 /sheet/e3_XXXX）");
  return { padId, scode: url.searchParams.get("scode") ?? "", tab: url.searchParams.get("tab") ?? "" };
}

// ---------- 客户端 ----------
let clientPromise;
function getClient() {
  if (!clientPromise) {
    clientPromise = (async () => {
      const mod = await load("package/dist/api/client.js").catch(() => null);
      if (!mod) {
        console.error(`错误：找不到 ${WORKDIR}/package，先跑一遍 scripts/setup.sh`);
        process.exit(1);
      }
      try {
        return new mod.WecomClient();
      } catch (e) {
        console.error(`错误：${e.message}\n→ 跑 node scripts/login.mjs 重新登录`);
        process.exit(1);
      }
    })();
  }
  return clientPromise;
}

// 一次 opendoc 请求，返回完整响应（rev / title / related_sheet 都在里面）
async function fetchDoc(client, doc, start, end, tab) {
  const params = new URLSearchParams({
    id: doc.padId,
    scode: doc.scode,
    outformat: "1",
    normal: "1",
    wb: "1",
    nowb: "0",
    noEscape: "1",
    startrow: String(start),
    endrow: String(end),
    // xsrf 必须是 cookie 里 TOK 的值：传 1 时 opendoc 也能通，但 get/tabs 会返回空 body
    xsrf: client.xsrf || "1",
    t: String(Date.now()),
    tab: tab ?? doc.tab,
  });
  return client.getRaw(`https://doc.weixin.qq.com/dop-api/opendoc?${params}`);
}

const sheetOf = (data) =>
  data?.clientVars?.collab_client_vars?.initialAttributedText?.text?.[0]?.related_sheet ?? null;

function navF19(b64) {
  let buf;
  try {
    buf = inflateSync(Buffer.from(b64, "base64"));
  } catch {
    buf = Buffer.from(b64, "base64");
  }
  const root = pick(parse(buf), 1)[0];
  if (!root || !root.msg) return null;
  const t18 = pick(root.msg, 5).find((n) => n.msg && n.msg.find((x) => x.f === 1 && x.v === 18));
  if (!t18 || !t18.msg) return null;
  const f19 = pick(t18.msg, 19)[0];
  return f19 && f19.msg ? f19.msg : null;
}

// 一行的内容：cells 按出现顺序（= 从左到右，空单元格不返回），links 为超链接
function rowOf(b64) {
  if (!b64) return { cells: [], links: [] };
  const f19 = navF19(b64);
  if (!f19) return { cells: [], links: [] };
  const f5 = pick(f19, 5)[0];
  if (!f5 || !f5.msg) return { cells: [], links: [] };
  const cells = pick(f5.msg, 1).map((c) => {
    if (!c.msg) return textOf(c);
    const t = c.msg.find((x) => x.f === 1);
    return t ? textOf(t) : "";
  });
  const links = [];
  pick(f5.msg, 2).forEach((m) => m.msg && findLinkRecords(m.msg, links));
  const byUrl = new Map();
  for (const l of links) {
    const prev = byUrl.get(l.url);
    if (!prev || (prev.text.startsWith("http") && !l.text.startsWith("http"))) byUrl.set(l.url, l);
  }
  return { cells, links: [...byUrl.values()] };
}

const hasText = (rec) => (rec.cells ?? []).some((c) => c && c.trim());

async function fetchRow(client, doc, row, tab, retries = 4) {
  for (let a = 0; a < retries; a++) {
    try {
      return rowOf(sheetOf(await fetchDoc(client, doc, row, row, tab)));
    } catch (e) {
      if (a === retries - 1) {
        console.error(`  行 ${row} 失败: ${e.message}`);
        return { cells: [], links: [], err: true };
      }
      await new Promise((r) => setTimeout(r, 700 * (a + 1)));
    }
  }
  return { cells: [], links: [] };
}

async function pool(items, worker, concurrency) {
  let i = 0;
  await Promise.all(
    Array.from({ length: Math.max(1, Math.min(concurrency, items.length)) }, async () => {
      while (i < items.length) {
        const k = i++;
        await worker(items[k]);
        await new Promise((r) => setTimeout(r, 40 + Math.random() * 60));
      }
    })
  );
}

// 整表一次性拉取：只用来数"一共有多少非空单元格"，坐标不可信（空单元格被省略）
async function countAllCells(client, doc, tab) {
  try {
    const rec = rowOf(sheetOf(await fetchDoc(client, doc, 0, -1, tab)));
    return rec.cells.filter((c) => c && c.trim()).length;
  } catch {
    return 0;
  }
}

// ---------- 命令 ----------
async function cmdTabs() {
  const doc = parseDocUrl(urlArg);
  const client = await getClient();
  const info = await fetchDoc(client, doc, 0, 1);
  need(info, "接口没返回数据。可能是登录态失效，或该链接不是表格文档");
  const rev = info?.clientVars?.collab_client_vars?.rev ?? 0;
  const title = info?.clientVars?.title ?? "未命名";
  const data = await client.get("dop-api/get/tabs", { padId: doc.padId, rev: String(rev), xsrf: client.xsrf || "1" });
  const tabs = [];
  for (const h of data?.header ?? []) for (const item of h?.d ?? []) if (item.id && !item.hidden) tabs.push({ id: item.id, name: item.name ?? item.id });
  if (!tabs.length) console.error("没拿到标签列表，改用 URL 里的 tab 参数：" + (doc.tab || "无"));
  console.error(`# ${title}  rev=${rev}`);
  console.log(JSON.stringify(tabs, null, 2));
}

async function cmdShape() {
  const doc = parseDocUrl(urlArg);
  const tab = tabArg ?? doc.tab;
  need(tab, "缺少 tabId（先跑 tabs 命令拿 id）");
  const client = await getClient();
  const n = Number(flags.rows ?? 10);
  const totalCells = await countAllCells(client, doc, tab);
  const preview = [];
  let linkRows = 0;
  for (let r = 0; r < n; r++) {
    const rec = await fetchRow(client, doc, r, tab);
    if (rec.links.length) linkRows++;
    preview.push({ row: r, n: rec.cells.length, cells: rec.cells.map((c) => c.slice(0, 60)), links: rec.links.length });
  }
  console.log(JSON.stringify({ tab, totalNonEmptyCells: totalCells, previewRows: preview, rowsWithLinksInPreview: linkRows }, null, 2));
}

async function cmdRow() {
  const doc = parseDocUrl(urlArg);
  const tab = tabArg ?? doc.tab;
  const row = Number(a3);
  need(tab && Number.isFinite(row), "用法: wc.mjs row <url> <tabId> <rowNo>");
  const client = await getClient();
  console.log(JSON.stringify({ row, ...(await fetchRow(client, doc, row, tab)) }, null, 2));
}

function loadMap(file) {
  return fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, "utf-8")) : {};
}

async function cmdRows() {
  const doc = parseDocUrl(urlArg);
  const tab = tabArg ?? doc.tab;
  const from = Number(a3), to = Number(a4);
  need(tab && Number.isFinite(from) && Number.isFinite(to), "用法: wc.mjs rows <url> <tabId> <from> <to>");
  const out = path.resolve(flags.out ?? `rows_${tab}.json`);
  const concurrency = Number(flags.concurrency ?? 4);
  const client = await getClient();
  const map = loadMap(out);

  const todo = [];
  for (let r = from; r <= to; r++) if (!(flags.resume && hasText(map[r] ?? {}))) todo.push(r);
  let done = 0;
  await pool(
    todo,
    async (r) => {
      map[r] = await fetchRow(client, doc, r, tab);
      if (++done % 25 === 0) {
        fs.writeFileSync(out, JSON.stringify(map));
        console.error(`  ${done}/${todo.length} 行 (r=${r})`);
      }
    },
    concurrency
  );
  fs.writeFileSync(out, JSON.stringify(map));
  const keys = Object.keys(map).map(Number).sort((a, b) => a - b);
  const filled = keys.filter((k) => hasText(map[k]));
  console.error(`完成 ${done} 行 → ${out}\n共 ${keys.length} 行, 有文字 ${filled.length} 行, 最后一行 ${filled.pop() ?? "-"}`);
}

// 自动爬到底：合并单元格会让"下一行"离得很远（实测中间有 15 行空），
// 所以不能靠"连续 N 行空"猜结尾，用连续空行数 + 单元格总数双重判据。
async function cmdFetch() {
  const doc = parseDocUrl(urlArg);
  const tab = tabArg ?? doc.tab;
  need(tab, "缺少 tabId（先跑 tabs 命令拿 id）");
  const client = await getClient();
  const out = path.resolve(flags.out ?? `rows_${tab}.json`);
  const concurrency = Number(flags.concurrency ?? 4);
  const emptyWindow = Number(flags.empty ?? 60);
  const maxRow = Number(flags.max ?? 5000);
  const chunk = Number(flags.chunk ?? 40);

  const map = loadMap(out);
  const total = await countAllCells(client, doc, tab);
  console.error(`整表非空单元格 ${total} 个，开始逐行抓取（空行容忍 ${emptyWindow}）...`);

  let row = 0, emptyRun = 0, acc = 0, last = -1, fetched = 0;
  while (row <= maxRow && emptyRun < emptyWindow) {
    const batch = [];
    for (let i = 0; i < chunk && row + i <= maxRow; i++) batch.push(row + i);
    await pool(
      batch,
      async (r) => {
        if (flags.resume && hasText(map[r] ?? {})) return;
        map[r] = await fetchRow(client, doc, r, tab);
        fetched++;
      },
      concurrency
    );
    for (const r of batch) {
      const rec = map[r] ?? { cells: [] };
      if (hasText(rec)) {
        const n = rec.cells.filter((c) => c && c.trim()).length;
        acc += n;
        last = r;
        emptyRun = 0;
      } else emptyRun++;
    }
    row += chunk;
    fs.writeFileSync(out, JSON.stringify(map));
    console.error(`  扫到第 ${Math.min(row - 1, maxRow)} 行，累计 ${acc}/${total} 个单元格，最后非空行 ${last}`);
  }

  // 裁掉尾部的空行
  for (const k of Object.keys(map)) if (Number(k) > last) delete map[k];
  fs.writeFileSync(out, JSON.stringify(map));
  const rows = Object.keys(map).length;
  console.error(`\n完成：${rows} 行（有文字 ${Object.values(map).filter(hasText).length} 行），最后一行 ${last}`);
  console.error(`累计单元格 ${acc} / 整表 ${total}`);
  if (total && acc < total * 0.98) {
    console.error(
      `⚠️ 少读了 ${total - acc} 个单元格。可能原因：合并块比 ${emptyWindow} 行更高（加大 --empty），` +
        `或中间有超长空白段（先用 shape 看看前几行，再手动 rows 补区间）`
    );
  }
  console.log(out);
}

const commands = { tabs: cmdTabs, shape: cmdShape, row: cmdRow, rows: cmdRows, fetch: cmdFetch };
need(commands[cmd], `未知命令 ${cmd}，可选: ${Object.keys(commands).join(" / ")}`);
await commands[cmd]();
