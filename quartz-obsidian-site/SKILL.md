---
name: quartz-obsidian-site
description: Use when building or debugging a Quartz Obsidian site.
tags: [quartz, obsidian, cloudflare-pages, cloudflare-access, d1, spa, oauth]
---

# Quartz + Obsidian 站点：完整搭建流程与踩坑记录

从零搭一套「Obsidian 笔记 → Quartz 静态站 → Cloudflare Pages → 登录/书架/评论/订阅」的实战记录。
每一条「坑」都是真实调试出来的，照抄可以避免重走。

## 何时用这个 skill

- 搭建或维护 Quartz（v5.x）Obsidian 发布站
- 给静态站加登录（邮箱验证码 / Google / GitHub / 用户名密码）
- 加书架、观影库、视频专题这类「数据驱动」的列表页
- 用 Cloudflare Pages + D1 + Access 做部署和访问控制
- 排查「点了没反应」「SPA 导航后失效」「页面很卡/OOM」这类前端疑难

---

## 一、整体架构

```
D:\private\obsidian            源笔记仓库（Obsidian vault，唯一真源）
D:\private\obsidian-site       构建仓库
  content-all/                 全量内容（私有站用）      ← 生成物
  content-public/              公开子集（公开站用）        ← 生成物
  dist-all/                    私有站产物                 ← 生成物
  dist-public/                 公开站产物                 ← 生成物
  quartz/                      Quartz 框架 + plugins-local/
  scripts/                     构建/注入脚本（核心逻辑都在这）
  functions/                   Cloudflare Pages Functions（后端 API）
  db/migrations/               D1 迁移
```

**两个站共用一套代码**，靠 `make_public_subset.py` 分出公开内容：

| 站 | 域名 | Pages 项目 | 内容 |
|---|---|---|---|
| 公开 | notes.example.com | `hfhfn-notes` | content-public |
| 私有 | private.example.com | `hfhfn-notes-private` | content-all |

**铁律：每次改完必须两站都 build + deploy。** 只发一站会导致「私有站长期不同步」，用户会报「改了没生效」。

---

## 二、构建流水线

`package.json` 里的顺序不能乱：

```json
"build": "python scripts/build_library.py
       && python scripts/render_notebooklm.py content-all
       && node scripts/patch_explorer_init.mjs
       && npx quartz build -d content-all -o dist-all
       && node scripts/inject_library.mjs dist-all
       && node scripts/inject_charts.mjs dist-all
       && node scripts/rewrite_tags_index.mjs dist-all
       && node scripts/fix_tag_pages.mjs dist-all
       && node scripts/paginate_listing.mjs dist-all
       && python scripts/inject_fonts.py --dir dist-all
       && python scripts/inject_analytics.py --dir dist-all
       && node scripts/inject_mindmap.mjs dist-all
       && node scripts/harden_font_sizes.mjs dist-all
       && node scripts/bundle_runtime.mjs dist-all
       && node scripts/patch_graph_loop.mjs dist-all
       && node scripts/check_js_syntax.mjs dist-all"
```

关键点：
- **`bundle_runtime` 必须在所有 inject 之后** —— 它把各脚本的 RUNTIME 打包成外部文件
- **`patch_graph_loop` 在 bundle 之后** —— 它改的是 Quartz 编译产物
- **`check_js_syntax` 必须最后** —— 语法错误会让整段运行时静默失效，这是最坑的一类问题

---

## 三、Cloudflare Access 配置（私有站）

### 3.1 应用结构

Access 里应该只有 **2 个应用**：

```
Notes Bypass   self_hosted_domains:
                 /api
                 /my
                 /static
                 /vendor
                 /prescript-*
                 /postscript-*
                 /login
Notes Owner    整站（private.example.com）
```

**为什么必须列全这 6+ 条路径**：只放行 `/api` 会让静态 JS 全部 302，页面能开但所有交互失效。这是最难查的坑之一 —— HTML 正常、按钮全死。

### 3.2 用 API 管理（比面板可靠）

```python
TOKEN = "..."   # 需要 Access: Apps and Policies 编辑权限
ACC = "<account_id>"

# 列应用
GET  /accounts/{ACC}/access/apps
# 改 self_hosted_domains（注意：域名被别的应用占用会报 12132 conflict，
# 必须先删旧应用再加）
PUT  /accounts/{ACC}/access/apps/{app_id}
     body: {name, domain, type:"self_hosted", self_hosted_domains:[...],
            session_duration:"24h", app_launcher_visible:false}
```

### 3.3 登出端点：参数和域名都不能错

**实测对照表（2026-11 验证）**：

| URL | 结果 |
|---|---|
| `https://<team>.cloudflareaccess.com/cdn-cgi/access/logout?returnTo=<url>` | ✅ **302 + 4 条 Set-Cookie**（正确） |
| 同域 `<site>/cdn-cgi/access/logout` | ❌ 200 Error 页面，不清 cookie |
| 同域 + `?returnTo=` | ❌ 400 Bad Request |
| team 域 + `?redirect_url=` | ❌ 200 Error 页面，不清 cookie |
| `returnTo` 指向不受 Access 保护的域名 | ❌ 400 Bad Request |

**三个必踩的坑**：
1. 参数是 `returnTo`，**不是** `redirect_url`
2. 必须用 **team 域**，同域端点只返回错误页
3. `returnTo` 必须是**受 Access 保护的域名**，否则 400

### 3.4 Access 会种 4 个 cookie，少清一个就退不掉

```
CF_Authorization   JWT，真正决定是否放行
CF_Binding         设备绑定
CF_Device          设备标识
CF_Session         会话
```

清 cookie 时要**同时清三种 Domain 形式**（host-only / `Domain=<host>` / `Domain=<apex>`），因为 Access 可能用任一形式种 cookie，猜错一个就清不掉。对不存在的 cookie 发清除指令是无害的。

### 3.5 「登出后又自动登录」不是 bug

如果 Access 应用配了：
```
session_duration: 730h          （30 天）
auto_redirect_to_identity: true
```
那么清完 cookie 再访问站点，**Access 会用自己的边缘会话直接重新签发 JWT**，不问你验证码。这是 Access 的 SSO 设计。

验证方法（curl，不依赖浏览器）：
```bash
# 1. 未登录访问 → 302 到 Access 登录页
curl -s -o /dev/null -w "%{http_code} %{redirect_url}" https://private.example.com/
# 2. 访问登出端点 → 302 + 4 cookie
curl -s -D - -o /dev/null "https://<team>.cloudflareaccess.com/cdn-cgi/access/logout?returnTo=..."
# 3. 再访问 → 仍是 302 到登录页 = 后端没问题，是 SSO 行为
```

要真正强制重新输码，只能改 Access 配置（缩短 session_duration / 关 auto_redirect_to_identity）。

---

## 四、账号体系（自建会话，与 Access 并存）

### 4.1 身份来源优先级

```js
getUser(request, env):
  1. notes_session      自建 HMAC 会话（公开站读者）
  2. CF_Authorization   Access JWT（私有站）—— 必须完整验签！
```

### 4.2 ⚠️ 必须真正验签，不能只解码

JWT 的 payload 是**明文 base64**。只解码不验签 = 任何人伪造 payload 就能冒充管理员。

```js
// 正确做法
const JWKS_URL = "https://<team>.cloudflareaccess.com/cdn-cgi/access/certs"
// 用 WebCrypto 做 RS256 验签，校验 aud / exp，公钥缓存 1 小时
// 兜底：没配 ACCESS_AUD 就完全不信任 CF_Authorization
```

**实测攻击**：手工构造 `{"email": "<管理员邮箱>"}` + 假签名，修复前返回 `isAdmin: true`，修复后被拒。

### 4.3 业务数据必须按 user_id 归属，不能按 email

**这是最严重的设计坑。** 用户用 Gmail 和 GitHub 登录，如果业务表以 email 为主键，两边数据完全分家（实测 gmail 17 条、sina 12 条互不可见）。

正确的表结构：
```sql
users(id PK, email, name)           -- id 是稳定 uid
identities(provider, provider_uid, user_id)
account_links(email, user_id)
-- 业务表全部挂 user_id，email 只用于展示和发信
collections(user_id, item_key, status)
bookmarks(user_id, slug)
likes(user_id, slug)
comments(user_id, ...)
history(user_id, slug, visits, last_seen)
comment_reactions(user_id, comment_id, emoji)
```

**迁移时容易漏表**：我们第一次只改了 4 张表，漏了 `history` 和 `comment_reactions`，用户报「书架合并了但足迹没合并」。

**哪些表刻意不该按 uid 归属**：
| 表 | 为什么 |
|---|---|
| `views` | 按 slug 聚合的全站统计，不属于个人 |
| `subscribers` | 邮件订阅按邮箱是正确语义（退订链接绑邮箱） |
| `video_visibility` | 管理员隐藏视频的**全站开关**，按 uid 隔离会让「A 隐藏了 B 看不到」 |

### 4.4 GitHub 无真实邮箱时不要建影子账号

GitHub 可能只返回 `<id>+<login>@users.noreply.github.com`。直接拿它建号会得到一个**永远收不到信、也没法和 Gmail 归并**的账号。

正确行为：标记 `needsBind`，引导用户绑定真实邮箱，绑定后把历史数据一起迁过来。

### 4.5 多登录方式合并只能靠用户主动绑定

| 场景 | 结果 |
|---|---|
| Google `a@gmail.com` + GitHub `a@gmail.com` | ✅ 自动同一账号 |
| Google `a@gmail.com` + GitHub `b@qq.com` | ❌ 两个账号，**系统无法自动判断** |

按 IP / 设备去猜既不安全也不可靠。只能提供「绑定其他邮箱」入口让用户主动合并。

### 4.6 GitHub API 必须带 User-Agent

不带会返回 `403 Request forbidden by administrative rules`，看起来像 token 失效，实际是缺头。

```js
const USER_AGENT = "my-site-auth (+https://notes.example.com)"
// /user、/user/emails 统一带上
```

### 4.7 PBKDF2 迭代次数上限

Cloudflare Workers 的 PBKDF2 **上限 100000**，超过报 `NotSupportedError: iteration counts above 100000 are not supported`。

---

## 五、Quartz SPA 的 7 个致命坑

Quartz 是 SPA：导航只替换 `<body>`，**内联 `<script>` 不会重新执行**。这是所有前端问题的总根源。

### 5.1 首次加载不触发 nav / render 事件

Quartz 很多组件的初始化写成：
```js
document.addEventListener("nav", init)
document.addEventListener("render", init)
```
**首次直接打开页面时这两个事件都不发** → 组件（日夜按钮、explorer 折叠）根本没绑定。

### 5.2 ❌ 绝对不要补发 render 事件（会 OOM）

看起来最自然的修法是「在调度器里补发 render 让组件重新初始化」。**这会炸**：

```
run() → dispatch render → graph 组件收到后重建整个 PIXI 应用
→ DOM 变化 → MutationObserver → run() → dispatch render → ...
无限循环，每轮 new 一个 WebGL 上下文，几十秒就 out of memory
```

✅ 正确修法：**只针对具体元素直接绑定**，不触发任何全局事件。

### 5.3 ⚠️ 双重绑定会让按钮「点了没反应」

这是最隐蔽的一类问题。Quartz 自己绑了 handler，我们又绑一个：
- 日夜切换：两个 handler 各切一次 → 净效果为零
- explorer 折叠：两个 handler 各 toggle 一次 → 看起来没反应

✅ 统一解法：**捕获阶段接管 + 阻止冒泡**
```js
document.addEventListener('click', function(ev){
  var btn = ev.target.closest('.target');
  if (!btn) return;
  ev.preventDefault();
  ev.stopImmediatePropagation();   // 挡住 Quartz 的
  doTheThing();
}, true);  // ← capture: true 是关键
```
委托在 `document` 上还有个好处：SPA 换掉整个 body 后不用重新绑。

### 5.4 ⚠️ 但捕获阶段 + stop 会破坏 SPA 路由

对**链接**（`<a>`）用 `stopImmediatePropagation` 会把 Quartz 的 SPA 路由拦截器也挡住 → 退化成整页刷新 → 用户看到「点一下整个页面都闪一下」。

查 Quartz 源码 `@quartz-community/explorer`：
```js
let A = n.dataset.behavior || "collapse"
if (A !== "link") { C.stopPropagation(); ...toggle... }
```
配置 `folderClickBehavior: "link"` 时，**Quartz 对 folder-button 什么都不做**，只让浏览器正常跳转。

✅ 所以对链接：**只补做自己的动作，绝不 stop / preventDefault**。
```js
document.addEventListener('click', function(ev){
  var a = ev.target.closest('.explorer-ul a.folder-button');
  if (!a) return;
  toggleFolder(a);   // 只展开，事件继续往下走
});  // 冒泡阶段，不 capture、不 stop
```

### 5.5 状态要写进 localStorage 的 fileTree

Quartz 用 `localStorage.fileTree`（`[{path, collapsed}]`）恢复目录展开状态。点击后页面跳转、explorer 重渲染，它会按这份数据重建。

我们只改 DOM 不写 localStorage → 它按旧状态重建 → 「刚展开又被折叠」。

### 5.6 运行时要打包成外部文件，不能每页内联

689 个页面各内联 53KB JS = 41MB 重复内容。

✅ 打包成带 hash 的 `/static/nx-runtime.<hash>.js`，每页只放一行 `<script src defer>`。单页内联从 53,530 字节降到 356 字节。

### 5.7 语法错误会让整段运行时静默失效

一个多余的 `}` 就让 `window.__pbToggleAccount` 变成 `undefined`，整段功能死掉但页面看起来正常。

✅ 必须加构建后检查：
```js
// scripts/check_js_syntax.mjs — 对 dist 里所有 JS 跑 node --check，有错就让构建失败
```

---

## 六、运行时计算的坑

### 6.1 不要在运行时读 CSS 算分页条数

```js
// ❌ 布局没完成时 getComputedStyle().gridTemplateColumns 返回 "none" 或 1 列
var cols = getComputedStyle(grid).gridTemplateColumns.split(/\s+/).length;
perPage = cols * 3;   // 3 列变成 1×3 = 3
```

用户反馈「每页 3 个」就是这个。

✅ **构建时算好写进 `data-perpage`，运行时只读属性**：
```js
function perPageOf(grid){
  var n = Number(grid.getAttribute('data-perpage'));
  if (n > 0) return n;
  return {book:5, movie:4, video:3}[grid.dataset.for] * 3;
}
```

**判据**：榜单分页一直正常、书架分页一直错，差别就在前者构建时静态切好、后者运行时算。

### 6.2 每页条数应按列数整数倍

各库列数不同（藏书馆 5、观影库 4、视频专题 3），写死 12 条时 5 列的库最后一行只剩 2 张，像漏了数据。

按「列数 × N 行」算，每页都是完整行。

### 6.3 事件发了没人听

`inject_charts` 标记后插入卡片时会派发 `shelf-changed`，但 `inject_library` **从来没监听它** → 后插的卡片不参与分页 → 「标记了 25 本但看不到分页器」。

### 6.4 排序后必须重新分页

按日期重排 DOM 后不重新 `render()`，分页的 slice 还是按旧顺序取 → 「第 1 页显示的是旧的第 1 批」。

### 6.5 无日期的条目排序时永远放最后

不管正序倒序，缺 `data-date` 的都排末尾 —— 它们没有时间信息，混在中间会让人误以为是某个时间点的内容。

---

## 七、性能：关系图谱会拖垮整页

`@quartz-community/graph` 的渲染循环是**无条件递归**的：
```js
function se(){ if(!De){ ...重绘所有节点和连线...; requestAnimationFrame(se) } }
```
不看物理模拟是否收敛，也不看页面是否可见，**每帧都重绘**。实测空闲时仍跑 48 FPS，主线程被占满 → 整个页面卡、日夜切换也卡。

### 补丁方案（构建后打，不改 node_modules）

```js
// 每帧记录所有节点坐标，与上一帧比最大位移
// 位移平方 < 0.09（约 0.3px）视为静止 → 300ms 后再看
// 顺带 Q.ticker.autoStart = false 停掉 PIXI 自动 ticker
```

### ⚠️ 首帧必须无条件放行

首帧 `ready = false` 时循环里不比较，`__maxd` 恒为 0 → 判定「静止」→ 直接 return → **一帧都没画，画布全空**。

```js
if (!__arr.ready) { __arr.ready = true; requestAnimationFrame(se); return; }  // 首帧放行
if (__maxd < 0.09) { ...静止处理... }
```

### ⚠️ 恢复时要重启 ticker

静止时 `ticker.stop()` 之后，节点又开始动时 ticker 不会自己醒来 → 画面冻住。

---

## 八、页面级功能实现要点

### 8.1 分页器要一次做全

只给「上一页/下一页」不够用。完整形态：
```
« 首页    ← 上一页   第 1 / 5 页   下一页 →   末页 »   跳至 [n] 页
```
- 输入越界不报错，内部夹到合法范围（输 999 落到末页）
- 输入非法（空/非数字）恢复成当前页
- `input.max` 同步总页数
- 只在值不同时才回写 `input.value`，避免打断用户输入
- input 的 `click` 阻止冒泡，防止被别的委托监听当成翻页

**站内通常有三套独立分页器**（书架 / 榜单 / 笔记列表），改一套不够，要全部覆盖。

### 8.2 登录后跳转要合理

`safeRedirect` 的默认回退不要写死某个功能页（比如 `/my/bookmarks`），否则「在足迹页登录，结果跳到收藏页」。用户倾向**显示首页**。

### 8.3 登出后按后退不能回到已登录页面

`Cache-Control: no-store` **拦不住** —— 后退走的是 **bfcache**，整个页面（含 JS 堆、DOM）冻结在内存里，恢复时不发任何请求。

✅ 监听 `pageshow`：
```js
window.addEventListener('pageshow', function(ev){
  if (ev.persisted) {   // 从 bfcache 恢复
    fetch('/api/whoami', {credentials:'include', cache:'no-store'})
      .then(r => r.json())
      .then(d => { if (!d.authed) location.reload(); });
  }
});
```

为什么 reload 而不是原地改 DOM：服务端渲染的页面里带的是登录态数据（收藏列表、足迹、账号名），原地改要改十几处且容易漏。

### 8.4 导出文件必须带后缀

用 `data URL` + `a.download` 保证文件名带 `.svg` / `.html`。

### 8.5 订阅推送基线要覆盖普通页面

Quartz 同时输出 `<slug>/index.html` 和 `<slug>.html`。只 `rglob("index.html")` 会漏掉大半（实测只收集到 58/368 篇）。

---

## 九、数据库迁移清单

按这个顺序，一张表都不能漏：

```
001_login_codes            邮箱验证码
002_comments               评论
003_collections            书架/标记
004_video_visibility       视频可见性（全站开关，不挂 uid）
005_account_identities     users.id + identities
006_credentials            用户名密码
007_user_id_ownership      collections/comments/bookmarks/likes 加 user_id
008_history_user_id        history 加 user_id        ← 007 漏了这张
009_reactions_visibility   comment_reactions 加 user_id
```

**迁移前必须备份**：`wrangler d1 execute --command "SELECT * FROM t" --json > backup.json`

**D1 迁移是事务性的**：第一次执行在 `users.id` UNIQUE 约束上失败，完整回滚，数据完好。

**去重策略**：同一 `item_key` 在两个邮箱都出现时保留较新记录（实测删了 4 条重复电影标记）。

---

## 十、测试与验证

### 10.1 测试夹具要跟着迁移走

改完 API 后如果测试挂了，先查测试文件里**内联的 CREATE TABLE** 是不是缺字段。我们改了 5 张表的查询，测试夹具还停留在旧 schema。

### 10.2 已知的固定失败

`npm run test` 固定 2 个失败（`links a cloned plugin's peers` / `links a git plugin's peers`），根因是全局 `~/.npmrc` 的 `allow-scripts` 与项目级 install 冲突：
```
npm error --allow-scripts is not allowed in project-scoped installs
```
与业务代码无关，基线就存在。

### 10.3 验证必须走用户的实际路径

不能只测直接 URL。用户路径是「首页 → 点列表 → 点详情」，每一步都可能触发不同的初始化时机。

### 10.4 用 curl 做后端验证，不要外包给用户

```bash
# 状态码 + 跳转
curl -s -o /dev/null -w "%{http_code} %{redirect_url}" URL
# 完整响应头（看 Set-Cookie / Location）
curl -s -D - -o /dev/null URL
# 带 cookie 模拟会话
curl -b jar.txt -c jar.txt URL
```

---

## 十一、部署注意事项

### 11.1 Pages 环境变量必须是 secret_text

`wrangler pages deploy` 会**清空** `plain_text` 类型的变量。所有密钥用 `secret_text`。

### 11.2 环境变量改了要重新部署

Pages secret 需要重新部署才会注入 Functions 运行时。

### 11.3 私有站和公开站要分别配变量

同一个代码库，两个 Pages 项目，**环境变量不共享**。私有站缺 OAuth 变量就渲染不出 Google/GitHub 按钮（`providerConfigured` 返回 false）。

### 11.4 部署命令

```bash
npx wrangler pages deploy dist-public --project-name hfhfn-notes --commit-dirty=true
npx wrangler pages deploy dist-all --project-name hfhfn-notes-private --commit-dirty=true
```

注意：如果 shell 里残留了 `CLOUDFLARE_API_TOKEN` / `CF_API_TOKEN` 且权限不足，部署会报 `Authentication error [code: 10000]`。先 `unset`。

---

## 十二、排查方法论（比具体修法更重要）

这几条是从反复返工里总结出来的，能省大量时间。

### 12.1 「点了没反应」先查双重绑定，别猜时机

按钮失效有两个常见原因：
1. 绑定时机不对（组件还没渲染）
2. **双重绑定互相抵消**（框架也绑了）

先查 2：在 console 里看元素上有没有多个 listener，或者临时 `stopImmediatePropagation` 试一下。日夜按钮、探索折叠都是这个形状。

### 12.2 「以前正常现在坏了」先查自己上一轮改了什么

`git log --oneline -5` + `git diff HEAD~1`。关系图谱全空、文件夹点击闪烁、数据全乱，三次都是我自己引入的回归。

### 12.3 同类问题第 2 次出现时换方法，不要重试

第一次失败可能是偶然，第二次失败说明假设错了。加诊断探针拿确定证据（诊断端点、绑定计数、网络日志），不要反复改代码碰运气。

### 12.4 用「哪些同类功能是好的」反推差异

- 榜单分页正常 / 书架分页错 → 差别在构建时算 vs 运行时算
- 首页日夜按钮正常 / 其他页失效 → 差别在首次加载 vs SPA 导航
- 公开站正常 / 私有站失效 → 差别在 Access 层

对照组比单点排查快得多。

### 12.5 结构化配置不要用行号替换

我用行号改 `KINDS` 配置，误删了相邻的 `json:` 字段，导致两个库的数据整个没注入。用精确字符串匹配。

### 12.6 部署前先单步跑注入，确认三个库都有输出

```
[book]  已注入 3 本
[movie] 已注入 2 部
[video] 已注入 37 条
```
少一行就说明配置坏了，不要继续全量构建。

---

## 十三、必须交付前回归验证的功能

用户会以「又变回…了」指出回归，交付前逐项过一遍：

- [ ] 日夜切换（首页 + 非首页 + SPA 导航后）
- [ ] 探索折叠 / 目录展开折叠（含导航后状态保持）
- [ ] 三个库的数据完整（书籍/电影/视频条数）
- [ ] 分页器（首页/末页/跳页/翻页）
- [ ] 排序切换（正序/倒序）
- [ ] 侧边栏账号入口（登录态显示用户名）
- [ ] 登出 → 回首页/登录页，后退不回登录态
- [ ] 关系图谱有内容且不卡
- [ ] 评论、思维导图、信息图、灯箱
- [ ] 两站都部署了
