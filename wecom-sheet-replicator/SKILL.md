---
name: wecom-sheet-replicator
description: 把企业微信在线表格（doc.weixin.qq.com / 企微文档 / wedoc / 微盘表格）完整复刻成本地 xlsx，即使在文档只读、右上角没有"导出"、Ctrl+C 都被禁用的情况下。原理是用用户本人的登录态逐行读取 dop-api/opendoc 的数据流并做字节级 protobuf 解析，不绕过任何权限、不猜密码、不触达无权限的内容。凡是用户给出 doc.weixin.qq.com 的 sheet 链接并要求下载 / 导出 / 另存 / 复刻 / 克隆 / 备份成 Excel，或者说"这个表没有导出权限""复制不了""右键下载灰色"，或者让你"照原样还原这张表"时，都用这个技能。
---

# 企业微信只读表格复刻

企业微信文档里的表格是 **canvas 绘制**的：页面上没有单元格 DOM，所以右键、打印、另存、复制、移动端 H5、无头浏览器 dump DOM 全都拿不到内容。唯一可靠的路径是它自己加载数据用的接口 `dop-api/opendoc`，用用户本人的登录态去读——这等价于"用户自己有阅读权限，只是换了个客户端看"。

## 先别做的事（这些一定失败，别浪费轮次）

| 尝试 | 结果 |
|---|---|
| 页面"导出/下载"菜单 | 管理员禁了导出，菜单项不存在或灰色 |
| 浏览器打印 / CDP `Page.printToPDF` | 打印出来只有工具栏和评论区，表格区空白（canvas 不进打印流） |
| 移动端 H5 / 改 UA | 仍是 canvas，只是尺寸变了 |
| 无头 Chrome `--dump-dom` | 渲染进程常被终止；即便成功也只有 `<canvas>` 壳子 |
| `Ctrl+A` / `Ctrl+C` | 被 `copy` 事件拦截，剪贴板无变化 |
| 直接 `curl` 文档 URL | 返回企微身份登录页 |
| 读本机 Chrome 的 Cookies 库 | 登录态在企微客户端 / 独立 profile 里，且库文件被运行中的浏览器锁住 |

如果用户已经试过其中几项，直接确认结论，然后说明还有一条读数据流的路线，不要重复踩。

## 两条硬规矩

1. **只用用户自己的登录态**，只读用户有权限看的文档。不要尝试绕过权限、不要猜 token。
2. **第三方包先审计再运行**。这次对话里用户给的一个"现成 MCP 工具"在 npm 上是 404，是编出来的；真实存在的那个（`wecomdocs-cli`）也要先 `npm view` 确认存在、解包、`grep` 所有外联域名、确认 cookie 只写本地，再运行。审计结果要如实告诉用户。

## 工作流

### 1. 准备依赖

```bash
bash <skill>/scripts/setup.sh            # 默认工作目录 ./.wecom-work
# 或指定：WECOM_WORKDIR=~/wcdoc bash <skill>/scripts/setup.sh
```

脚本做的事：`npm pack wecomdocs-cli` 解包（只用它的 `WecomClient` 和 `SessionManager`，不用它的表格解码器——那个解码器会丢坐标），装 `playwright`（跳过浏览器下载，复用系统 Chrome）、`openpyxl`、`pillow`。

### 2. 登录（拿 cookie）

```bash
node <skill>/scripts/login.mjs
```

用持久化 profile 打开 doc.weixin.qq.com，用户扫码一次。之后 cookie 存在 `~/.wecomdocs-cli/session.json`，profile 也留着，后续 30 天内不用再扫。检测成功的标志是 cookie 里有 `wedoc_sid`。

会话可能过期。`WecomClient` 构造时会抛"会话已过期"，重新跑一次登录即可。

### 3. 列出所有 sheet

```bash
node <skill>/scripts/wc.mjs tabs "<文档链接>"
# → [{"id":"000001","name":"面试实题"}, ...]
```

### 4. 看一眼结构再动手

```bash
node <skill>/scripts/wc.mjs shape "<文档链接>" <tabId> --rows 10
```

输出整表非空单元格总数 + 前 10 行的列数和内容片段。这一步是判断"该用哪种重建模式"的依据（模式见 `references/xlsx-rebuild.md`）。

### 5. 逐行抓取（核心）

```bash
node <skill>/scripts/wc.mjs fetch "<文档链接>" <tabId>          # 自动爬到底
node <skill>/scripts/wc.mjs rows  "<文档链接>" <tabId> 0 400     # 或手动指定区间，可断点续抓
```

**为什么必须一行一次请求**：接口返回的 protobuf 里只有"非空单元格"，**空单元格会被整段省略**，所以一次拉全表时列位置必然错位——这是所有"内容不缺但行列全乱"的根源。把 `startrow=endrow=N` 传进去，返回的就只有这一行的单元格，按"从左到右、缺省即空"就能还原列位。慢（一行一个请求，大表几分钟），但这是唯一准确的读法。

**行号是稀疏的**：合并单元格会让下一条记录跳到很远的行。实测一张表的前 5 条记录落在第 2、17、28、42、58 行——所以**不能用"连续 N 行空就停"猜结尾**（我一开始设 25 行，直接漏掉了后 4 条）。`fetch` 的做法是先整表拉一次数出非空单元格总数，再逐行累加，两个数字对上才算读完；对不上会明确警告"少读了 N 个单元格"。`--empty` 只作兜底（默认 60）。

产出 `rows_<tabId>.json`：`{ "行号": { "cells": ["A列文本","B列文本",...], "links": [{"text","url"}] } }`。
`cells` 已按列序排列（尾部空列被裁掉）；`links` 是该行的超链接，显示文字和 URL 都已还原。

大表建议后台跑，一次 300–500 行，边跑边做第 6 步。

### 6. 摸清每张表的真实结构

抓完先看数据形状，再决定怎么排版。用 `wc.mjs rows ... | head` 或直接读 JSON：

- **每行列数**：稳定 2 列 = 简单两列；忽 1 忽 2 = 有纵向合并（合并区只在首行返回一次文本）；忽 2 忽 3 = 有横向分组块（类别列 + 内容列）。
- **有没有横幅行**：整行只有一个短文本、且下一段内容重新从 1 开始，通常是"1期""XX 汇总""此后面试题实时更新，倒序排列"这类分隔横幅。
- **有没有超链接**：`links` 非空的行，说明那一列原来是指向外部文档的链接（GIT 地址、话术模板）。这类单元格的**显示文字不在 cells 里**，必须用 `links[].text` 补，否则整列看起来是空的。

接口给不了的两样东西，只能靠截图核对：**合并范围**、**数字单元格（序号）**。序号在文本数组里根本不返回，需要按业务规则重建（例如"每个横幅后重新从 1 计数"），并用截图抽样验证 `1=…、5=…、13=…` 是否对得上。

需要看原表长什么样时，用带 cookie 的 playwright 截图：

```bash
node <skill>/scripts/shot.mjs "<文档链接>" <tabId> out.png 1600 1400
```

只对**有疑问的表**截图核对（通常 1–3 张），逐格全量转写只在表格很小、或用户明确要求像素级一致时才做——大表转写既慢又不如接口准。

### 7. 写成 xlsx

不要手搓样式细节，用 `scripts/xlsx_helpers.py`（封装了合并组、超链接字体、宽度、冻结窗格、以及三个会让 openpyxl 报错/出错值的坑）。

```python
import sys; sys.path.insert(0, "<skill>/scripts")
from xlsx_helpers import *

allow_raw_text()        # 允许写入含控制字符的原文，最后统一清洗
wb = Workbook(); wb.remove(wb.active)
ws = wb.create_sheet("面试实题")
...
style_sheet(ws, {1: 6, 2: 26, 3: 96}, header_rows=2)
merge_groups(ws, column=2, groups=[(4, "医疗"), (6, "教育")], fill="9DC3E6")
put_link(ws, row=4, column=4, text="GitHub", url="https://...")
save_xlsx(wb, "~/Desktop/结果.xlsx")   # 内部做非法字符清洗 + "=" 开头文本不当公式
```

改写规则，按原表视觉结构来：

- 纵向合并的列（序号、公司、类别、阶段）→ 首行写值，其余行 `merge_cells`，并让合并区垂直居中。用 `merge_groups()`，它会自动算出每组的结束行。
- 横向合并的横幅行 → 用 `merge_row()`。`merge_cells` 只保留左上角的值，把横幅文字写在第 2 列再合并，文字会直接消失（`verify.py` 能抓到这种错）。
- 一题一行 / 一条一行，永远不要把多行挤成一行，也不要把一行的多段拼成一个单元格。
- 超链接 → `put_link()`，它同时设置 `hyperlink` 和蓝色下划线字体，否则看起来像普通文本。
- 列宽按内容给（长文本列 90–105），长文本 `wrap_text=True`、`vertical="top"`。

### 8. 验证，再交付

```bash
python <skill>/scripts/verify.py rows_<tabId>.json ~/Desktop/结果.xlsx 面试实题
```

它把所有源单元格文本与 xlsx 里的值做归一化比对（去控制字符、去首尾空白），输出"缺失数量 / 覆盖率 / 未出现的单元格"。**覆盖率必须 100%**；不为 100% 就说明有行没抓到、或者分组逻辑把某段吞了（常见：横幅行把紧跟的题目吃掉了）。

再抽查 3 个点：第一行、中间某条、最后一行，用 `shot.mjs` 截图和 xlsx 对照。

## 交付时要诚实说明的三件事

把文件交给用户时，明确区分"接口精确还原"和"推断"：

1. **文字 100% 是原文**，逐单元格校验过。
2. **序号是重建的**（接口不返回数字单元格），规则依赖业务假设，已用截图抽样验证。
3. **合并范围是推断的**：接口无坐标，按"首行有值、后续行缺省"还原，绝大多数正确，但复杂嵌套合并（一个块与另一个块错位）可能偏差一行。

不要声称"和原表一模一样"。用户拿它当内容备份没问题，当审计留档就得说清差异。

## 收尾安全

`~/.wecomdocs-cli/session.json` 里是用户的企微文档 cookie（等同登录凭证）。任务结束后主动问是否删除；用户说删就 `rm` 掉，同时可删 `<workdir>/browser-profile`。

## 参考

- `references/protobuf-map.md` — 接口与 protobuf 字段地图、三个会让内容凭空消失的解码坑。改动 `wc.mjs` 前必读。
- `references/xlsx-rebuild.md` — 复杂表结构的重建模式（分组块、双序号列、横向公司+题目对、合并与链接），附真实案例。
