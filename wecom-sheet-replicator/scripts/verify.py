"""校验：xlsx 是否把所有源单元格都写进去了。

    python verify.py rows_<tab>.json ~/Desktop/结果.xlsx [sheet名] [--show 10]

判定方式是把两边都归一化（去控制字符、去首尾空白）后按字符串比对。
覆盖率不是 100% 时，通常意味着：
  - 抓取时某些行没抓到（重跑 wc.mjs rows 补）
  - 分组逻辑把某段吞掉了（常见：横幅行把紧跟其后的正文一起吃进下一页）
  - 单元格里有 emoji 或 base64 内容，文本还原失败
"""
import json
import re
import sys

from openpyxl import load_workbook

ILL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def norm(s):
    return ILL.sub(" ", str(s)).strip()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    show = 10
    for a in sys.argv[1:]:
        if a.startswith("--show"):
            show = int(a.split("=", 1)[1]) if "=" in a else int(sys.argv[sys.argv.index(a) + 1])
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)

    rows_path, xlsx_path = args[0], args[1]
    sheet = args[2] if len(args) > 2 else None

    raw = json.load(open(rows_path, encoding="utf-8"))
    data = {int(k): v for k, v in raw.items()}

    src = []
    for k in sorted(data):
        for c in data[k].get("cells") or []:
            s = (c or "").strip()
            if s:
                src.append((k, s))

    wb = load_workbook(xlsx_path)
    ws = wb[sheet] if sheet else wb[wb.sheetnames[0]]
    have = set()
    for r in ws.iter_rows(values_only=True):
        for v in r:
            if isinstance(v, str):
                have.add(norm(v))

    miss = [(k, s) for k, s in src if norm(s) not in have]
    total = len(src)
    cov = (total - len(miss)) / total * 100 if total else 100.0

    print(f"sheet       : {ws.title}  ({ws.max_row} 行 x {ws.max_column} 列)")
    print(f"源单元格    : {total}")
    print(f"未写入      : {len(miss)}")
    print(f"覆盖率      : {cov:.2f}%")
    if miss:
        print(f"\n前 {show} 个未写入的单元格：")
        for k, s in miss[:show]:
            print(f"  第{k}行 len={len(s)}: {s[:70]!r}")
        sys.exit(2)


if __name__ == "__main__":
    main()
