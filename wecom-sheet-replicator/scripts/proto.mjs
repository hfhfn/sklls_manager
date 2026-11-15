// 字节级 protobuf 解析。
// 关键点：任何 length-delimited 字段都保留 raw 字节，文本一律用 raw 直接 UTF-8 解码。
// 第三方解码器会用"像不像子消息"的启发式判断，把以 "1. " 开头的长句当成嵌套消息，导致整句丢失。
export function parse(buf) {
  const out = [];
  let off = 0;
  while (off < buf.length) {
    const [tag, o1] = varint(buf, off);
    if (o1 > buf.length) break;
    off = o1;
    const f = Number(tag >> 3n), w = Number(tag & 7n);
    if (f === 0) break;
    if (w === 0) {
      const [v, o2] = varint(buf, off);
      off = o2;
      out.push({ f, w, v: Number(v) });
    } else if (w === 2) {
      const [len, o2] = varint(buf, off);
      off = o2;
      const n = Number(len);
      if (off + n > buf.length) break;
      const raw = buf.subarray(off, off + n);
      off += n;
      const node = { f, w, raw };
      try {
        const kids = parse(raw);
        if (kids.length && Math.max(...kids.map((k) => k.f)) <= 2000) node.msg = kids;
      } catch {}
      out.push(node);
    } else if (w === 5) {
      off += 4;
    } else if (w === 1) {
      off += 8;
    } else break;
  }
  return out;
}

function varint(buf, off) {
  let r = 0n, s = 0n, p = off;
  while (p < buf.length) {
    const b = buf[p++];
    r |= BigInt(b & 0x7f) << s;
    if ((b & 0x80) === 0) break;
    s += 7n;
    if (s > 63n) break;
  }
  return [r, p];
}

export const pick = (nodes, f) => nodes.filter((n) => n.f === f);
export const one = (nodes, f) => nodes.find((n) => n.f === f);

// 取文本：优先 raw 直接 UTF-8；出现替换字符时按 base64 再试一次（含 emoji 的单元格是 base64）
export function textOf(node) {
  if (!node || !node.raw) return "";
  let s = node.raw.toString("utf-8");
  if (s.includes("\ufffd")) {
    const alt = Buffer.from(s, "base64").toString("utf-8");
    if (!alt.includes("\ufffd")) s = alt;
  } else if (/^[A-Za-z0-9+/]{16,}={0,2}$/.test(s)) {
    const alt = Buffer.from(s, "base64").toString("utf-8");
    if (alt && !alt.includes("\ufffd") && /[\u4e00-\u9fff]/.test(alt)) s = alt;
  }
  return s;
}

// 递归收集节点内所有 http 字符串
export function httpIn(node, out = []) {
  if (!node) return out;
  if (node.raw) {
    const s = node.raw.toString("utf-8");
    const i = s.indexOf("http");
    if (i >= 0) {
      const m = s.slice(i).match(/^https?:\/\/[^\s"']+/);
      if (m) out.push(m[0]);
    }
  }
  if (node.msg) for (const c of node.msg) httpIn(c, out);
  return out;
}

// 超链接：父节点下某个子消息含 f11（链接载荷），该子消息的 f1 是显示文字；
// 若 f1 为空，显示文字在同级 f7 的兄弟节点 f3 上。
export function findLinkRecords(nodes, out = []) {
  for (const n of nodes) {
    if (!n.msg) continue;
    for (const c of n.msg) {
      if (!c.msg) continue;
      const lf = c.msg.find((x) => x.f === 11);
      if (!lf) continue;
      const urls = httpIn(lf);
      if (!urls.length) continue;
      const clean = (t) => {
        let x = t.replace(/^[\u0000-\u001f]+/, "");
        // 去掉被误当作内容的长度前缀字节（其值恰等于剩余文本的字节长度）
        if (x.length > 1 && x.charCodeAt(0) < 128 && x.charCodeAt(0) === Buffer.byteLength(x.slice(1), "utf-8")) x = x.slice(1);
        return x.replace(/[\u0000-\u001f]+$/, "").trim();
      };
      let text = "";
      const own = c.msg.find((x) => x.f === 1);
      if (own) {
        const t = clean(textOf(own));
        if (t && !t.includes("http")) text = t;
      }
      if (!text && c.f === 7) {
        const sib = n.msg.find((x) => x.f === 3);
        if (sib) {
          const t = clean(textOf(sib));
          if (t && !t.includes("http")) text = t;
        }
      }
      out.push({ text: text || urls[0], url: urls[0] });
    }
    for (const c of n.msg) if (c.msg) findLinkRecords([c], out);
  }
  return out;
}
