# 接口与 protobuf 字段地图

改动 `wc.mjs` 之前读这一页。这里记的是实测结论（2026-11，`wecomdocs-cli@0.6.0` 时期），格式可能随版本变，但解析思路不变。

## 一次请求长什么样

```
GET https://doc.weixin.qq.com/dop-api/opendoc
    ?id=<padId>              文档 id，URL 路径里 /sheet/e3_XXXX 的 e3_XXXX
    &scode=<scode>           分享码，URL query 里的 scode
    &tab=<tabId>             子表 id，如 000001 / mubwbm
    &outformat=1&normal=1&wb=1&nowb=0&noEscape=1
    &startrow=<N>&endrow=<N> 行区间。关键：传同一行，只返回这一行
    &xsrf=1&t=<毫秒时间戳>

Headers: Cookie: wedoc_sid=...; Referer: https://doc.weixin.qq.com/
```

子表列表走另一条：`GET /dop-api/get/tabs?padId=&rev=&xsrf=1`，`rev` 从 opendoc 响应里取；结果在 `header[].d[].{id,name,hidden}`。

### 请求参数里的两个坑

- **`xsrf` 要传 cookie 里 `TOK` 的值**，不是字面量 `1`。传 `1` 时 opendoc 照样返回数据（所以很容易以为没问题），但 `get/tabs` 会返回 **HTTP 200 + 空 body**，`JSON.parse` 直接炸 `Unexpected end of JSON input`。客户端里对应 `client.xsrf` 这个 getter。
- **`rev` 从响应里读**：`clientVars.collab_client_vars.rev`（形如 1177）。别去 protobuf 里猜——我照着某个 f1 字段猜了个 0，get/tabs 同样是空 body。

### 行号是稀疏的

合并单元格会把后续记录推到很远的行号。实测一张只有 5 条记录的表，内容落在第 **2、17、28、42、58** 行，中间全是空行（合并块撑开的）。后果：

- 不能用"连续 N 行空就停"猜结尾，N 设小了会整段漏掉；
- `maxRow` 拿不到：`getMaxRowFromProtobuf` 逻辑是 `f19.f3.f4`，但实测这个版本 `f19.f3` 只有 `f1`、`f5` 两个字段，函数只会 fallback 到 200（而表有 1200 行）。

可靠做法是**先整表拉一次数出非空单元格总数**，再逐行累加，两个数字对上才算读完。整表拉取的坐标不可信，但总数是准的（实测 19=19、1650≈1727，差异来自合并单元格的归属判断，用于判断"有没有读全"够用）。

## 数据在哪

```
data.clientVars.collab_client_vars
    .initialAttributedText.text[0].related_sheet   ← base64( deflate( protobuf ) )
```

解包：

```
buf  = inflateSync(base64decode(related_sheet))     // 有些情况本来就没压缩
root = parse(buf).filter(f == 1)[0]
f18  = root.msg.filter(f == 5).find(n => n.msg 里有 {f:1, v:18})
f19  = f18.msg.filter(f == 19)[0].msg
```

`f19` 里的关键子字段：

| 字段 | 含义 |
|---|---|
| `f5[0].f1[]` | 单元格列表。元素是纯文本节点，或 `{f1: 文本}` 的消息 |
| `f5[0].f2[]` | 元数据（样式、富文本、超链接） |
| `f4[]` | 表的尺寸/配置类信息 |
| `f6[]` | 样式条目 `{f1: 行号, f2: 列号, f3: 样式}` —— **有坐标，但没有文本** |

## 接口没有给的（必须自己处理）

- **空单元格**：整条省略。所以全表一次拉取时列位置必然错乱 —— 这就是逐行拉取的唯一理由。
- **数字单元格**：序号列（`1,2,3…`）不在文本数组里，怎么都读不到。只能按业务规则重建，再截图抽样核对。
- **合并范围**：`f6` 只有样式没有合并区，无法还原 `mergeCells` 的起止。做法：某行有值、后续行该列缺省，就推断为纵向合并。
- **列宽 / 行高 / 公式 / 图片**：都没有。

## 三个会让内容凭空消失的解码坑

### 1）文本被误判成嵌套消息（最致命）

一段普通文本的字节序列，常常**恰好是合法的 protobuf**。例如以 `1. ` 开头的句子：首字节 `0x31`… 之类会被读成 tag，于是"启发式解码器"判定它是子消息，递归进去，文本就丢了。表现是：整句 `1. 你有…` 消失，前后内容却都在。

对策：**任何 length-delimited 字段都保存原始字节 `raw`，先用 `raw.toString("utf-8")` 取文本**，只有在确认要往下挖时才递归。判断"是消息还是文本"时不要用正则猜，用调用方的语义（f1 下面就是文本）。

### 2）含 emoji 的单元格是 base64

同一批单元格里，纯中文是 UTF-8 原文，带 emoji 的会变成 base64 字符串。对策：`textOf()` 先按 UTF-8 解，出现 `\ufffd` 就按 base64 再解一次；另外对"纯 base64 字符集 + 长度 ≥16"的串也试一次 base64，解出来含中文才采纳。

### 3）超链接的显示文字不在 cells 里

`GIT 地址`、`话术模板` 这类列全是超链接，`f1` 单元格数组里**根本没有它们**。结构在 `f5.f2[]` 下面：

```
某节点 {
  f11: "https://..."        // 链接载荷
  f1:  "GitHub 仓库"        // 显示文字（有时为空）
}
或（f1 为空时）：
某节点 {
  f7: { f11: "https://...", ... },   // 链接
  f3: "GitHub 仓库"                   // 显示文字在兄弟节点
}
```

直接从 `f11` 拿到的字符串前面可能粘着长度前缀字节，值是"剩余文本的字节长度"，`findLinkRecords` 里的 `clean()` 就是按这个特征削掉它。

忘了这一步的典型症状：**整列看起来是空的**，而文字版的其它列都正常。
