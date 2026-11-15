# 结构重建模式

逐行数据拿到手之后，剩下的工作是"这堆 cells 在原表里是怎么摆的"。下面六种是企微文档里最常见的排法，判断依据是**每行列数的变化规律**。

## 先看列数

```python
import json
data = {int(k): v for k, v in json.load(open("rows_000001.json", encoding="utf-8")).items()}
for k in sorted(data):
    cells = [c for c in data[k]["cells"] if c.strip()]
    print(k, len(cells), [c[:24] for c in cells])
```

| 现象 | 推断 |
|---|---|
| 每行稳定 2 个单元格 | 两列清单，一列名、一列内容 |
| 忽 1 忽 2 | 有纵向合并：合并区只在首行返回一次 |
| 忽 2 忽 3 | 有分组列：多出来的那个是"类别/阶段/公司" |
| 某行只有 1 个短文本、且后面从 1 重新计数 | 横幅行（`1期`、`XX汇总`、`倒序排列`） |
| `links` 非空但 `cells` 里没对应文字 | 那一列是超链接，文字要从 `links[].text` 取 |

## 模式与写法

### A. 两列清单

一行一条，直接 `ws.append([name, content])`。唯一的坑是单元格里可能有换行，`wrap_text=True` + `vertical="top"`。

### B. 序号/对象 + 多条明细（一条对多行）

源数据的特征：某个对象独占一行（只有它一个 cell 或带说明），后续只带一个 cell 的行是它的明细。

```python
groups = []
for k in sorted(data):
    cells = [c.strip() for c in data[k]["cells"] if c and c.strip()]
    if not cells:
        continue
    if len(cells) >= 2:
        groups.append({"head": cells[0], "items": cells[1:]})
    elif not groups or is_head(cells[0]):
        groups.append({"head": cells[0], "items": []})
    else:
        groups[-1]["items"].append(cells[0])
```

写表时每个 group 占 `max(1, len(items))` 行，首列/次列 `merge_cells` 到整块，`vertical="center"`。

注意源行号可能跳得很远（第 2 行之后直接是第 17 行），这不影响分组——分组只按出现顺序，不看行号是否连续。判断"这是新的一条还是上一条的明细"要看**列数**和**词形**，不能看行距。

`is_head()` 只能靠词形判断，没有权威依据。实测有效的规则（按顺序短路）：

```python
if "倒序排列" in s: return True                  # 横幅
if re.match(r"^\d+期$", s): return True           # 期数横幅
if re.match(r"^\d{2,4}[\./]\d{1,2}", s): return True   # 日期开头的批次
if re.search(r"[？?。；;]", s): return False      # 带问号/分号的是题目
if re.search(r"(公司|集团|科技|信息|技术|软件|网络|智能|外包|股份|中心|事业部|研究院|工作室|…)$", s): return True
if re.match(r"^(北京|上海|深圳|杭州|…)", s) and len(s) <= 22: return True
return False
```

局限要跟用户说清：**短而无后缀的对象名会被错分到明细列**（"东风日产""易诚互动"）。做不到 100%，别假装做到了。

### C. 分组列 + 多列明细（一个类别跨多行）

源数据：每个新类别的首行多一个 cell，其余行没有。

```python
groups = []          # [(起始行, 类别名)]
for r in rows:
    cells = [c.strip() for c in r["cells"]]
    if len(cells) >= 3:
        groups.append((ws.max_row + 1, cells[0]))
        name, desc = cells[1], cells[2]
    else:
        name, desc = cells[0], cells[1]
    ws.append([seq, "", name, url, desc])

merge_groups(ws, column=2, groups=groups, fill=LIGHT)
```

`merge_groups` 会自动"从本组起始行合并到下一组起始行的上一行"，最后一组一直合并到 `max_row`。

### D. 双序号列

原表把"项目"和"岗位职责"两个清单并排放在一张表里，各有自己的序号列：

```
| 序号 | 项目名称 | 项目内容 | 序号 | 岗位职责 |
```

同一个 `seq` 写进第 1 列和第 4 列，两列序号同步。别自作聪明合并成一列——用户的筛选依赖它。

### E. 分组 + 合并单元格里挂一个链接

原表在一整段合并区里放了一个"话术模板"链接。接口会把这个链接记在该段**每一行**上（重复），所以要先抽干、再只写一次：

```python
for start, end in ranges:
    link = None
    for rr in range(start, end + 1):
        c = ws.cell(row=rr, column=5)
        if c.hyperlink:
            link = (c.value, c.hyperlink.target)
            c.value = None; c.hyperlink = None
    if link:
        put_link(ws, start, 5, link[0], link[1])
    ws.merge_cells(start_row=start, start_column=5, end_row=end, end_column=5)
```

### F. 横幅行 + 序号重启

整行跨列合并、加底色；**并把序号计数器清零**。这一步最容易漏：清零了但没写横幅后面的正文，或者写了正文但序号没清零，都会造成"内容少一段"或"序号从 100 继续"。

```python
if re.match(r"^\d+期$", head) or "倒序排列" in head:
    ws.append([head, None, None])
    r = ws.max_row
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
    ws.cell(row=r, column=1).fill = BLUE
    seq = 0
    for q in items:                     # 横幅行也可能挂着正文，别丢
        ws.append([None, None, q])
    continue
```

## 完整骨架

```python
import json, sys
sys.path.insert(0, "<skill>/scripts")
from xlsx_helpers import *
from openpyxl import Workbook

allow_raw_text()
data = {int(k): v for k, v in json.load(open("rows_000001.json", encoding="utf-8")).items()}

wb = Workbook(); wb.remove(wb.active)
ws = wb.create_sheet("面试实题")
ws.append(["序号", "公司", "面试题"])
# … 按上面的模式填 …
style_sheet(ws, {1: 6, 2: 26, 3: 96}, header_rows=1, freeze="A2")
print("saved ->", save_xlsx(wb, "~/Desktop/结果.xlsx"))
```

## 两个 openpyxl 陷阱

1. **合并只保留左上角的值**。`merge_cells("A2:D2")` 之后，B2/C2/D2 里原本写的东西会被丢弃。横幅文字必须写在 A 列（`merge_row()` 就是干这个的），纵向合并同理写在起始行。症状是"明明写了，打开却没有"，`verify.py` 能直接抓出来。
2. **以 `=` 开头的正文会被当公式**。`style_sheet()` 里统一把这类单元格 `data_type = "s"`，否则打开显示 `#NAME?`。

另外：`wb.save()` 在目标文件被 Excel/WPS 占用时抛 `PermissionError`。用 `save_xlsx()`，它会自动改存 `xxx (2).xlsx`，不用整轮重跑。

## 核实清单

交付前跑一遍：

1. `python verify.py rows_<tab>.json 结果.xlsx <sheet名>` → 覆盖率必须 100%
2. 截图对三个点：第 1 行、中间某条、最后一行（`shot.mjs --cell A150`）
3. 序号抽样：截图上读 3 个数字，和 xlsx 里同位置比
4. 合并区数量合理（不是 0，也不是每行都合）

**不要声称"和原表一模一样"**：文字是精确的，序号和合并是推断的。这个区别对用户很重要。
