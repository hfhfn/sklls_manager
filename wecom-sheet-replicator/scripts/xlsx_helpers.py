"""写 xlsx 的公共封装。

这里封的是三个实际踩过的坑，不封就会得到"文件打不开"或"内容对不上"：

1. 从接口拿到的原文里可能带控制字符（\x00-\x1f），openpyxl 默认直接抛
   IllegalCharacterError。`allow_raw_text()` 先放开，写完再 `sanitize()` 统一替换成空格，
   这样原文不会在任何一步被悄悄丢掉。
2. 正文以 `=` 开头时 openpyxl 会当成公式写，打开后显示 #NAME?。
   `style_sheet()` 里统一把这类单元格的 data_type 改回 "s"。
3. 目标文件被 Excel/WPS/预览占用时 `wb.save()` 抛 PermissionError。
   `save_xlsx()` 自动改存同目录的 "xxx (2).xlsx"，而不是让整轮重建白跑。
"""
import os
import re

import openpyxl.cell.cell as _occ
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ILLEGAL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

GREEN = PatternFill("solid", fgColor="1E7A4C")
BLUE = PatternFill("solid", fgColor="4A90D9")
LIGHT = PatternFill("solid", fgColor="9DC3E6")
HEAD_FONT = Font(bold=True, color="FFFFFF", size=10)
BODY = Font(size=10)
LINK = Font(size=10, color="1155CC", underline="single")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(vertical="top", wrap_text=True)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)


def allow_raw_text():
    """放行控制字符，允许把接口原文原样写进单元格。写完记得 save_xlsx()。"""
    _occ.ILLEGAL_CHARACTERS_RE = re.compile(r"(?!x)x")


def sanitize(wb):
    """把控制字符换成空格。必须在保存前调用，否则 xlsx 里是乱码控制符。"""
    n = 0
    for ws in wb:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and ILLEGAL.search(c.value):
                    c.value = ILLEGAL.sub(" ", c.value)
                    n += 1
    return n


def style_sheet(ws, widths, header_rows=1, header_fill=GREEN, freeze=None):
    """表头填色冻结 + 正文自动换行 + 列宽 + 边框，顺手修掉 "=" 开头的伪公式。"""
    for r in range(1, header_rows + 1):
        for c in ws[r]:
            c.fill = header_fill
            c.font = HEAD_FONT
            c.alignment = CENTER
            c.border = BORDER
        ws.row_dimensions[r].height = 26
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, max_col=ws.max_column):
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("="):
                c.data_type = "s"
            if c.row > header_rows:
                c.font = BODY
                c.alignment = WRAP
            c.border = BORDER
    for i, w in widths.items():
        ws.column_dimensions[get_column_letter(i)].width = w
    if freeze:
        ws.freeze_panes = freeze


def merge_groups(ws, column, groups, value_in_first=True, fill=None, center=True):
    """按 (起始行, 值) 列表做纵向合并，一直合并到下一个分组的上一行。

    groups=[(2, "医疗"), (8, "教育")] 意为第 2-7 行合并且值为"医疗"，第 8 行到底为"教育"。

    注意 openpyxl 的 merge_cells 只保留左上角单元格的值，其余会被丢弃，
    所以值必须写在起始行（value_in_first=True 就是这个意思）。横向合并用 merge_row()。
    """
    out = []
    for i, (start, value) in enumerate(groups):
        end = groups[i + 1][0] - 1 if i + 1 < len(groups) else ws.max_row
        if end < start:
            end = start
        if value_in_first:
            ws.cell(row=start, column=column, value=value)
        if end > start:
            ws.merge_cells(start_row=start, start_column=column, end_row=end, end_column=column)
        if fill:
            for rr in range(start, end + 1):
                ws.cell(row=rr, column=column).fill = fill
        if center:
            ws.cell(row=start, column=column).alignment = CENTER
        out.append((start, end))
    return out


def merge_row(ws, row, col_start, col_end, value=None, fill=None, font=None):
    """横向合并一行并写值。

    值必须落在 col_start（左上角），写进中间列会被 openpyxl 在合并时丢掉——
    这是"表格里出现了文字、打开却找不到"的常见原因。
    """
    if value is not None:
        ws.cell(row=row, column=col_start, value=value)
    if col_end > col_start:
        ws.merge_cells(start_row=row, start_column=col_start, end_row=row, end_column=col_end)
    c = ws.cell(row=row, column=col_start)
    if fill:
        c.fill = fill
    if font:
        c.font = font
    c.alignment = CENTER
    return c


def put_link(ws, row, column, text, url):
    c = ws.cell(row=row, column=column, value=text)
    c.hyperlink = url
    c.font = LINK
    c.alignment = WRAP
    return c


def save_xlsx(wb, path):
    """保存；目标被占用时自动改名，不抛异常。返回实际写入的路径。"""
    sanitize(wb)
    path = os.path.expanduser(path)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    root, ext = os.path.splitext(path)
    for i in range(0, 20):
        target = path if i == 0 else f"{root} ({i}){ext}"
        try:
            wb.save(target)
            return target
        except PermissionError:
            continue
    raise PermissionError(f"{path} 及同名副本都被占用，先关掉 Excel/WPS 再试")
