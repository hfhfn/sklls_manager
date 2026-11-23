# 可直接复用的代码片段

按用途分组。都是实际跑通过的，改掉域名/项目名即可用。

---

## 1. 登出接口（区分公开站 / Access 私有站）

`functions/api/auth/logout.js`

```js
import { clearSessionCookie } from "../_session.js"

const ACCESS_TEAM_DOMAIN = "https://<team>.cloudflareaccess.com"

function isPrivateHost(request) {
  return new URL(request.url).hostname.startsWith("private.")
}

// Access 会种的全部 cookie 名。少清一个就退不掉。
const ACCESS_COOKIES = ["CF_Authorization", "CF_Binding", "CF_Device", "CF_Session", "CF_AppSession"]

/**
 * 同时清 host-only / Domain=<host> / Domain=<apex> 三种形式。
 * Access 可能用任一形式种 cookie，猜错一个就清不掉。
 * 对不存在的 cookie 发清除指令是无害的。
 */
function clearAccessCookies(request) {
  const host = new URL(request.url).hostname
  const parts = host.split(".")
  const apex = parts.length > 2 ? "." + parts.slice(-3).join(".") : null

  const out = []
  for (const name of ACCESS_COOKIES) {
    out.push(`${name}=; Path=/; Max-Age=0; Secure; SameSite=Lax`)
    out.push(`${name}=; Path=/; Max-Age=0; Secure; SameSite=Lax; Domain=${host}`)
    if (apex) out.push(`${name}=; Path=/; Max-Age=0; Secure; SameSite=Lax; Domain=${apex}`)
  }
  return out
}

/**
 * 必须 team 域 + returnTo。
 * returnTo 必须是受 Access 保护的域名，否则 400。
 */
function accessLogoutUrl(request) {
  const origin = new URL(request.url).origin
  return `${ACCESS_TEAM_DOMAIN}/cdn-cgi/access/logout?returnTo=${encodeURIComponent(origin + "/")}`
}

export async function onRequestPost({ request }) {
  const privateSite = isPrivateHost(request)

  const headers = new Headers({
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store",
  })
  headers.append("set-cookie", clearSessionCookie())
  if (privateSite) {
    for (const c of clearAccessCookies(request)) headers.append("set-cookie", c)
  }

  return new Response(
    JSON.stringify({
      ok: true,
      accessLogoutUrl: privateSite ? accessLogoutUrl(request) : null,
      redirect: "/",
    }),
    { status: 200, headers },
  )
}

export async function onRequestGet({ request }) {
  const privateSite = isPrivateHost(request)
  const headers = new Headers({
    location: privateSite ? accessLogoutUrl(request) : "/",
    "cache-control": "no-store",
  })
  headers.append("set-cookie", clearSessionCookie())
  if (privateSite) {
    for (const c of clearAccessCookies(request)) headers.append("set-cookie", c)
  }
  return new Response(null, { status: 302, headers })
}
```

前端：

```js
window.__pbLogout = function () {
  fetch("/api/auth/logout", { method: "POST", credentials: "include" })
    .then(r => r.ok ? r.json() : null)
    .then(d => {
      if (d && d.accessLogoutUrl) location.href = d.accessLogoutUrl;
      else location.href = (d && d.redirect) || "/";
    })
    .catch(() => { location.href = "/"; });
};
```

---

## 2. 捕获阶段接管按钮（防双重绑定）

适用于按钮（非链接）。

```js
(function(){
  if (window.__nxCaptureInstalled) return;
  window.__nxCaptureInstalled = true;

  document.addEventListener('click', function(ev){
    var t = ev.target;
    if (!t || !t.closest) return;
    var btn = t.closest('.darkmode');
    if (!btn) return;
    // 抢在框架自己的 handler 之前，并阻止它继续执行，
    // 否则两边各切一次 = 没反应
    ev.preventDefault();
    ev.stopImmediatePropagation();
    var root = document.documentElement;
    var next = root.getAttribute('saved-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('saved-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  }, true);   // ← capture: true 是关键
})();
```

**不要**对 `<a>` 用这个 —— 会挡掉框架的 SPA 路由（见第 3 段）。

---

## 3. 链接点击：只补动作，绝不拦截

适用于「点目录名要展开 + 跳转」。

```js
function toggleFolder(a){
  var li = a.closest('li');
  if (!li) return;
  var outer = li.querySelector(':scope > .folder-outer');
  if (!outer) return;

  var willOpen = !outer.classList.contains('open');
  outer.classList.toggle('open', willOpen);
  li.classList.toggle('open', willOpen);

  var fc = a.closest('.folder-container');
  if (fc) fc.setAttribute('aria-expanded', willOpen ? 'true' : 'false');

  // 必须同步到框架的 fileTree，否则导航后重渲染会按旧状态覆盖
  var folderPath = fc && fc.dataset ? fc.dataset.folderpath : null;
  if (folderPath) {
    try {
      var tree = JSON.parse(localStorage.getItem('fileTree') || '[]');
      var idx = -1;
      for (var i = 0; i < tree.length; i++) {
        if (tree[i] && tree[i].path === folderPath) { idx = i; break; }
      }
      var collapsed = !willOpen;
      if (idx >= 0) tree[idx].collapsed = collapsed;
      else tree.push({ path: folderPath, collapsed: collapsed });
      localStorage.setItem('fileTree', JSON.stringify(tree));
    } catch (e) {}
  }
}

document.addEventListener('click', function(ev){
  var t = ev.target;
  if (!t || !t.closest) return;
  var a = t.closest('.explorer-ul a.folder-button');
  if (!a) return;
  toggleFolder(a);   // 只展开，事件继续往下走 → SPA 路由正常工作
});  // 冒泡阶段，不 capture、不 stop、不 preventDefault
```

---

## 4. 登出后按后退不能回登录态（bfcache）

```js
(function(){
  var RELOAD_KEY = 'nx-auth-checked';

  function revalidate(){
    fetch('/api/whoami', { credentials: 'include', cache: 'no-store' })
      .then(r => r.ok ? r.json() : null)
      .then(d => {
        if (!d || d.authed) return;         // 还登录着，什么都不做
        var last = 0;
        try { last = Number(sessionStorage.getItem(RELOAD_KEY) || 0); } catch (e) {}
        var now = Date.now();
        if (now - last > 2000) {            // 2 秒去重，防反复 reload
          try { sessionStorage.setItem(RELOAD_KEY, String(now)); } catch (e) {}
          location.reload();
        }
      })
      .catch(() => {});
  }

  // persisted === true 表示从 bfcache 恢复（后退/前进），
  // 这种恢复不发任何网络请求，Cache-Control: no-store 拦不住
  window.addEventListener('pageshow', function(ev){
    if (ev.persisted) revalidate();
  });

  document.addEventListener('visibilitychange', function(){
    if (document.visibilityState === 'visible') {
      try {
        if (sessionStorage.getItem('nx-had-session') === '1') revalidate();
      } catch (e) {}
    }
  });
})();
```

---

## 5. 关系图谱：静止后停止重绘（含首帧放行）

构建后打补丁，不改 node_modules。

```js
// 匹配 Quartz 压缩后的渲染循环结尾
const OLD_TAIL = "requestAnimationFrame(se)}}"

const NEW_TAIL = `/* nx-patch: 静止后停止重绘 */
if(document.hidden){return}
se.__snap=se.__snap||{x:[],y:[],ready:false};
var __maxd=0,__i,__s,__dx,__dy,__arr=se.__snap;
for(__i=0;__i<j.length;__i++){
  __s=j[__i].simulationData;
  if(__s.x==null)continue;
  if(__arr.ready){
    __dx=__s.x-__arr.x[__i];__dy=__s.y-__arr.y[__i];
    var __d2=__dx*__dx+__dy*__dy;
    if(__d2>__maxd)__maxd=__d2;
  }
  __arr.x[__i]=__s.x;__arr.y[__i]=__s.y;
}
/* 首帧必须放行：此时没有上一帧可比，__maxd 恒为 0，
   直接按「静止」处理会一帧都不画，画布全空。 */
if(!__arr.ready){__arr.ready=true;requestAnimationFrame(se);return}
/* 位移平方 < 0.09（约 0.3px）视为静止 → 300ms 后再看 */
if(__maxd<0.09){
  try{if(window.__nxPixiApp&&window.__nxPixiApp.ticker)window.__nxPixiApp.ticker.stop()}catch(e){}
  if(se.__timer)return;
  se.__timer=setTimeout(function(){se.__timer=null;se()},300);
  return;
}
/* 又开始动了：确保之前停掉的 ticker 恢复，否则画面冻住 */
try{var __app=window.__nxPixiApp;if(__app&&__app.ticker&&!__app.ticker.started)__app.ticker.start()}catch(e){}
requestAnimationFrame(se)}}`

// 同时停掉 PIXI 自动 ticker（它自己也占一个 rAF 循环）
const OLD_INIT = 'await Q.init({...}),_.appendChild(Q.canvas)'
const NEW_INIT = 'await Q.init({...}),Q.ticker&&(Q.ticker.autoStart=!1,Q.ticker.stop()),_.appendChild(Q.canvas),window.__nxPixiApp=Q'
```

**实测效果**：`se` 循环从 110 次/2s 降到 0，堆内存稳定 97MB。

---

## 6. 构建时算分页条数

```js
// 配置里显式写，不要运行时读 CSS
const KINDS = {
  book:  { cols: 5, perPage: 10 },   // 5 列 × 2 行
  movie: { cols: 4, perPage: 8  },   // 4 列 × 2 行
  video: { cols: 3, perPage: 9, sortable: true },  // 3 列 × 3 行
}

// 写进 HTML
`<div class="book-grid" data-for="${kind}" data-perpage="${cfg.perPage}">`

// 运行时只读属性
function perPageOf(grid){
  var n = Number(grid.getAttribute('data-perpage'));
  if (n > 0) return n;
  return { book: 5, movie: 4, video: 3 }[grid.dataset.for] * 3;
}
```

---

## 7. 完整分页器（首页/末页/跳页）

```html
<div class="library-pager">
  <button data-first disabled>« 首页</button>
  <button data-prev disabled>← 上一页</button>
  <span class="lib-pinfo">第 1 页</span>
  <button data-next>下一页 →</button>
  <button data-last>末页 »</button>
  <span class="lib-jump">
    跳至 <input class="lib-jump-input" type="number" min="1" value="1"> 页
  </span>
</div>
```

```js
function go(p){
  cur = Math.max(1, Math.min(p, pages));   // 越界夹到合法范围
  renderItems();
  info.textContent = '第 ' + cur + ' / ' + pages + ' 页';
  first.disabled = prev.disabled = (cur === 1);
  last.disabled = next.disabled = (cur === pages);
  // 只在值不同时改，避免打断用户输入
  if (String(jump.value) !== String(cur)) jump.value = cur;
  jump.max = pages;
}

jump.addEventListener('keydown', ev => {
  if (ev.key === 'Enter') { ev.preventDefault(); commit(); jump.blur(); }
});
jump.addEventListener('blur', commit);
jump.addEventListener('click', ev => ev.stopPropagation());

function commit(){
  var v = parseInt(jump.value, 10);
  if (!isNaN(v)) go(v);
  else jump.value = cur;   // 非法输入恢复
}
```

---

## 8. 按日期排序 + 重新分页

```js
// 卡片上带日期（YYYY-MM-DD，字符串比较即可正确排序）
`<div class="book-card" data-date="${infoMap["整理"] || infoMap["读完"] || ""}">`

function applySort(grid, dir){
  var cards = [].slice.call(grid.querySelectorAll('.book-card'));
  if (!cards.length) return;
  var sign = dir === 'desc' ? -1 : 1;
  cards.sort(function(a, b){
    var da = a.getAttribute('data-date') || '';
    var db = b.getAttribute('data-date') || '';
    if (!da && !db) return 0;
    if (!da) return 1;    // 无日期永远排最后，不管正序倒序
    if (!db) return -1;
    if (da === db) return 0;
    return da < db ? -sign : sign;
  });
  for (var i = 0; i < cards.length; i++) grid.appendChild(cards[i]);
}

// ⚠️ 排完必须重新分页，否则 slice 还是按旧顺序取
sortBtn.addEventListener('click', function(){
  var dir = sortBtn.dataset.dir === 'desc' ? 'asc' : 'desc';
  sortBtn.dataset.dir = dir;
  applySort(grid, dir);
  state.page = render(tabs, grid, pager, state.key, 1);
});
```

---

## 9. 构建后 JS 语法检查

```js
// scripts/check_js_syntax.mjs
// 一个多余的 } 会让整段运行时静默失效，页面看起来完全正常但功能全死。
import fs from "node:fs"
import path from "node:path"
import { execFileSync } from "node:child_process"

const dir = process.argv[2]
let bad = 0, total = 0

function walk(d) {
  for (const f of fs.readdirSync(d)) {
    const p = path.join(d, f)
    const st = fs.statSync(p)
    if (st.isDirectory()) walk(p)
    else if (f.endsWith(".js")) {
      total++
      try {
        execFileSync("node", ["--check", p], { stdio: "pipe" })
      } catch (e) {
        bad++
        console.error(`[check-js] ✗ ${path.relative(dir, p)}`)
        console.error(String(e.stderr || e.message).slice(0, 500))
      }
    }
  }
}

walk(dir)
if (bad) {
  console.error(`[check-js] ${bad}/${total} 个文件有语法错误`)
  process.exit(1)
}
console.log(`[check-js] ✓ ${total} 个 JS 文件语法正常`)
```

---

## 10. CF_Authorization 完整验签

```js
const JWKS_URL = "https://<team>.cloudflareaccess.com/cdn-cgi/access/certs"

let jwksCache = { keys: null, at: 0 }

async function getKeys() {
  if (jwksCache.keys && Date.now() - jwksCache.at < 3600_000) return jwksCache.keys
  const r = await fetch(JWKS_URL)
  const d = await r.json()
  jwksCache = { keys: d.keys, at: Date.now() }
  return d.keys
}

function b64urlToBuf(s) {
  s = s.replace(/-/g, "+").replace(/_/g, "/")
  while (s.length % 4) s += "="
  const bin = atob(s)
  const buf = new Uint8Array(bin.length)
  for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i)
  return buf
}

export async function verifyAccessJwt(token, expectedAud) {
  // 没配 aud 就完全不信任 —— 宁可不认，也不要认错
  if (!expectedAud) return null

  const parts = token.split(".")
  if (parts.length !== 3) return null

  let header, payload
  try {
    header = JSON.parse(new TextDecoder().decode(b64urlToBuf(parts[0])))
    payload = JSON.parse(new TextDecoder().decode(b64urlToBuf(parts[1])))
  } catch { return null }

  // 校验 aud
  const aud = Array.isArray(payload.aud) ? payload.aud : [payload.aud]
  if (!aud.includes(expectedAud)) return null

  // 校验 exp
  if (!payload.exp || payload.exp * 1000 < Date.now()) return null

  // RS256 验签
  const keys = await getKeys()
  const jwk = keys.find(k => k.kid === header.kid)
  if (!jwk) return null

  const key = await crypto.subtle.importKey(
    "jwk", jwk,
    { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
    false, ["verify"],
  )
  const ok = await crypto.subtle.verify(
    "RSASSA-PKCS1-v1_5", key,
    b64urlToBuf(parts[2]),
    new TextEncoder().encode(parts[0] + "." + parts[1]),
  )
  return ok ? payload : null
}
```

**只解码不验签的后果**：手工构造 `{"email": "<管理员邮箱>"}` + 假签名就能拿到 `isAdmin: true`。实测过。

---

## 11. 诊断 Access 登出链路的 curl 脚本

```bash
#!/usr/bin/env bash
# 判断「登出后又自动登录」是后端问题还是 Access SSO 行为
TEAM="https://<team>.cloudflareaccess.com"
SITE="https://private.example.com"
JAR=$(mktemp)

echo "=== 1. 未登录访问（应 302 到 Access 登录页）==="
curl -s -o /dev/null -w "  %{http_code} → %{redirect_url}\n" -b "$JAR" -c "$JAR" "$SITE/"

echo "=== 2. 登出端点（应 302 + 4 条 Set-Cookie）==="
curl -s -D - -o /dev/null --max-time 25 \
  "$TEAM/cdn-cgi/access/logout?returnTo=$(printf %s "$SITE/" | python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.stdin.read(),safe=""))')" \
  | grep -iE '^HTTP/|^location|^set-cookie'

echo "=== 3. 再访问（仍 302 到登录页 = 后端没问题）==="
curl -s -o /dev/null -w "  %{http_code} → %{redirect_url}\n" -b "$JAR" -c "$JAR" "$SITE/"

rm -f "$JAR"
```

如果第 3 步仍是 302 到登录页，但浏览器里会自动登录 —— 那就是 Access 的 SSO 行为（`auto_redirect_to_identity` + 长 `session_duration`），不是代码 bug。
