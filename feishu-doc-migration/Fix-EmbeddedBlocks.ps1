param(
    [Parameter(Mandatory = $true)]
    [string]$WorkRoot,

    [Parameter(Mandatory = $true)]
    [string]$CheckpointFile,

    # 只处理标题匹配的文档（为空则处理全部）
    [string]$OnlyTitle = '',

    # 只演练不写入
    [switch]$DryRun,

    # 回填内嵌表格数据（源表 -> 新建空白表）
    [switch]$FillSheets,

    # 全部修复成功后，把 checkpoint 的 partial 状态归位为 success
    [switch]$MarkSuccess,

    # 单篇失败时继续下一篇
    [switch]$ContinueOnError
)

<#
.SYNOPSIS
修复 Migrate-FeishuDocs.ps1 迁移后丢失的内嵌对象。

.DESCRIPTION
飞书 API 跨空间复制内嵌对象会被服务端“降级”，且不报错：
  - <sheet token=...>      -> degrade_code 2113  Sheet content copy failed
  - <whiteboard token=...> -> degrade_code 2105  Whiteboard clone failed
  - <synced_reference>     -> 引用块跨文档绑定失效，目标里只剩空占位

本脚本按“块级插入/替换”修复，不重写整篇文档，因此不影响已有正文和图片：
  1. 表格：插入 <sheet type="blank"/>，再用 sheets API 把源表数据回填（保持可编辑）
  2. mermaid 画板：用内联 <whiteboard type="mermaid">源码</whiteboard> 重建
  3. token 画板：导出源画板 raw 节点 -> 新建 blank 画板 -> 导入节点
  4. synced_reference：可由调用方按需静态复制（本脚本不处理广告/导航类引用块）

依赖：工作目录中每篇文档的子目录（名称以源 token 前 8 位开头）内含 content.xml。
#>

$ErrorActionPreference = 'Continue'

function Log([string]$msg) {
    Write-Host ("[{0}] {1}" -f (Get-Date -Format 'HH:mm:ss'), $msg)
}

function Invoke-Lark {
    param([string[]]$ArgList, [string]$WorkingDir)
    $out = Join-Path $WorkingDir 'fix_out.json'
    $err = Join-Path $WorkingDir 'fix_err.txt'
    if (Test-Path -LiteralPath $out) { Remove-Item -LiteralPath $out -Force }
    $p = Start-Process -FilePath 'lark-cli' -ArgumentList $ArgList -WorkingDirectory $WorkingDir `
        -NoNewWindow -Wait -PassThru `
        -RedirectStandardOutput $out -RedirectStandardError $err
    $raw = ''
    if (Test-Path -LiteralPath $out) { $raw = Get-Content -LiteralPath $out -Raw }
    $errText = ''
    if (Test-Path -LiteralPath $err) { $errText = Get-Content -LiteralPath $err -Raw }
    $obj = $null
    if ($raw -and $raw.Trim()) { try { $obj = $raw | ConvertFrom-Json } catch { } }
    return [pscustomobject]@{ exit = $p.ExitCode; obj = $obj; raw = $raw; err = $errText }
}

function Get-DocContent {
    param([string]$DocToken, [string]$WorkingDir)
    $r = Invoke-Lark @('docs', '+fetch', '--doc', $DocToken, '--detail', 'with-ids', '--format', 'json', '--as', 'user') $WorkingDir
    if (-not $r.obj) { return $null }
    $d = $r.obj.data
    if ($d.document -and $d.document.content) { return $d.document.content }
    if ($d.content) { return $d.content }
    return $null
}

function Get-TopBlocks {
    param([string]$Xml)
    $x = $Xml -replace '^\s*<\?xml[^>]*\?>', ''
    $doc = New-Object System.Xml.XmlDocument
    $doc.PreserveWhitespace = $false
    $doc.LoadXml("<root>" + $x + "</root>")
    $list = @()
    foreach ($n in $doc.DocumentElement.ChildNodes) {
        if ($n.NodeType -ne [System.Xml.XmlNodeType]::Element) { continue }
        $text = ''
        foreach ($t in $n.SelectNodes('.//text()')) { $text += $t.Value }
        $tag = $n.LocalName
        $token = ''; $sheetId = ''; $wbType = ''
        if ($tag -eq 'sheet') { $token = $n.GetAttribute('token'); $sheetId = $n.GetAttribute('sheet-id') }
        if ($tag -eq 'whiteboard') { $wbType = $n.GetAttribute('type'); if (-not $wbType) { $token = $n.GetAttribute('token') } }
        $list += [pscustomobject]@{
            tag     = $tag
            text    = $text
            token   = $token
            sheetId = $sheetId
            wbType  = $wbType
            sig     = $tag + '|' + (($text -replace '\s+', ' ').Trim())
        }
    }
    return $list
}

function Get-TargetBlocks {
    param([string]$Content)
    $x = $Content -replace '^\s*<\?xml[^>]*\?>', ''
    $doc = New-Object System.Xml.XmlDocument
    $doc.PreserveWhitespace = $false
    $doc.LoadXml("<root>" + $x + "</root>")
    $list = @()
    foreach ($n in $doc.DocumentElement.ChildNodes) {
        if ($n.NodeType -ne [System.Xml.XmlNodeType]::Element) { continue }
        $text = ''
        foreach ($t in $n.SelectNodes('.//text()')) { $text += $t.Value }
        $token = ''; $sheetId = ''
        if ($n.LocalName -eq 'sheet') { $token = $n.GetAttribute('token'); $sheetId = $n.GetAttribute('sheet-id') }
        if ($n.LocalName -eq 'whiteboard') { $token = $n.GetAttribute('token') }
        $list += [pscustomobject]@{
            tag     = $n.LocalName
            text    = $text
            id      = $n.GetAttribute('id')
            token   = $token
            sheetId = $sheetId
            outer   = ($n.OuterXml -replace ' id="[^"]*"', '')
            sig     = $n.LocalName + '|' + (($text -replace '\s+', ' ').Trim())
        }
    }
    return $list
}

function Escape-Xml {
    param([string]$s)
    $s = $s -replace '&', '&amp;'
    $s = $s -replace '<', '&lt;'
    $s = $s -replace '>', '&gt;'
    return $s
}

if (-not (Test-Path -LiteralPath $CheckpointFile)) { throw "checkpoint 不存在: $CheckpointFile" }

$cp = @{}
foreach ($line in Get-Content -LiteralPath $CheckpointFile | Where-Object { $_.Trim() }) {
    try { $e = $line | ConvertFrom-Json } catch { continue }
    if ($e.source_node_token -and $e.target_obj_token) { $cp[$e.source_node_token] = $e }
}

$docs = @()
foreach ($f in (Get-ChildItem -LiteralPath $WorkRoot -Recurse -Filter 'content.xml')) {
    $t = Get-Content -LiteralPath $f.FullName -Raw
    if ($t -notmatch '<sheet|<whiteboard') { continue }
    $prefix = $f.Directory.Name.Split('_')[0]
    $m = $null
    foreach ($k in $cp.Keys) { if ($k.StartsWith($prefix)) { $m = $cp[$k]; break } }
    if (-not $m) { continue }
    if ($OnlyTitle -and $m.title -notlike "*$OnlyTitle*") { continue }
    $docs += [pscustomobject]@{ dir = $f.Directory.FullName; xml = $f.FullName; entry = $m }
}
Log ("待处理文档: {0} 篇" -f $docs.Count)

$summary = @()
foreach ($d in $docs) {
    $title = $d.entry.title
    try {
        $src = Get-TopBlocks (Get-Content -LiteralPath $d.xml -Raw)
        $missing = @($src | Where-Object {
                $_.tag -eq 'sheet' -or
                ($_.tag -eq 'whiteboard' -and ($_.wbType -eq 'mermaid' -or -not $_.wbType))
            })
        if ($missing.Count -eq 0) { continue }

        $tgtContent = Get-DocContent -DocToken $d.entry.target_obj_token -WorkingDir $d.dir
        if (-not $tgtContent) { Log ("跳过（无法读取目标正文）: {0}" -f $title); continue }
        $tgt = Get-TargetBlocks $tgtContent

        # 顺序对齐：找出源里存在、目标里缺失的内嵌块，并记录插入锚点
        # 目标侧 ul/ol/grid/callout 等容器没有 block id，此时用“替换下一个有 id 的块”
        $i = 0; $j = 0; $anchor = $null; $containerPending = $false; $plan = @(); $map = @{}
        while ($i -lt $src.Count) {
            $s = $src[$i]
            if ($j -lt $tgt.Count -and $s.sig -eq $tgt[$j].sig) {
                $map[$i] = $j
                if ($tgt[$j].id) { $anchor = $tgt[$j].id; $containerPending = $false }
                else { $containerPending = $true }
                $i++; $j++; continue
            }
            $isMissingObj = ($s.tag -eq 'sheet') -or ($s.tag -eq 'whiteboard' -and ($s.wbType -eq 'mermaid' -or -not $s.wbType))
            if ($isMissingObj) {
                $nextIdx = -1
                if ($containerPending) {
                    for ($k = $j; $k -lt $tgt.Count; $k++) {
                        if ($tgt[$k].id) { $nextIdx = $k; break }
                    }
                }
                if ($nextIdx -ge 0) {
                    $plan += [pscustomobject]@{ item = $s; mode = 'replace'; anchor = $null; nextIdx = $nextIdx }
                } else {
                    $plan += [pscustomobject]@{ item = $s; mode = 'after'; anchor = $anchor; nextIdx = -1 }
                }
                $i++
                continue
            }
            $found = -1
            for ($k = $j; $k -lt [Math]::Min($tgt.Count, $j + 25); $k++) {
                if ($tgt[$k].sig -eq $s.sig) { $found = $k; break }
            }
            if ($found -ge 0) {
                $map[$i] = $found
                if ($tgt[$found].id) { $anchor = $tgt[$found].id; $containerPending = $false }
                else { $containerPending = $true }
                $j = $found + 1; $i++
            } else { $i++ }
        }
        # 迁移脚本已把 token 表格/画板规范化为 blank 时，目标侧块已存在（有 token），
        # 此时不需要插入，只需要回填表格数据 / 导入画板节点
        $present = @()
        foreach ($si in @($map.Keys)) {
            $s = $src[$si]; $t = $tgt[$map[$si]]
            if ($s.tag -eq 'sheet' -and $t.tag -eq 'sheet' -and $t.token) {
                $present += [pscustomobject]@{ kind = 'sheetFill'; item = $s; token = $t.token; sheetId = $t.sheetId }
            }
            elseif ($s.tag -eq 'whiteboard' -and -not $s.wbType -and $t.tag -eq 'whiteboard' -and $t.token) {
                $present += [pscustomobject]@{ kind = 'wbImport'; item = $s; token = $t.token }
            }
        }
        if ($plan.Count -eq 0 -and $present.Count -eq 0) { continue }

        if ($DryRun) {
            Log ("[DRY] {0}: 需插入 {1} 块，需回填/导入 {2} 块" -f $title, $plan.Count, $present.Count)
            foreach ($p in $plan) {
                Log ("       - 插入 {0} mode={1} anchor={2} nextIdx={3}" -f $p.item.tag, $p.mode, ($p.anchor ?? ''), $p.nextIdx)
            }
            foreach ($p in $present) {
                Log ("       - {0} 目标已有块 token={1}" -f $p.kind, $p.token)
            }
            continue
        }

        $todo = @($present)
        $okAll = $true
        $curAnchor = $anchor
        $insCount = 0

        foreach ($p in $plan) {
            $item = $p.item
            $fileName = 'fx_insert.xml'

            # ---- 生成待插入内容 ----
            if ($item.tag -eq 'sheet') {
                $xmlParts = '<sheet type="blank"/>'
            }
            elseif ($item.wbType -eq 'mermaid') {
                $xmlParts = '<whiteboard type="mermaid">' + (Escape-Xml $item.text) + '</whiteboard>'
            }
            else {
                # token 画板：先建空白，再导入 raw 节点
                $xmlParts = '<whiteboard type="blank"/>'
            }

            if ($p.mode -eq 'replace') {
                $xmlParts += $tgt[$p.nextIdx].outer
                $cmdArgs = @('docs', '+update', '--doc', $d.entry.target_obj_token, '--command', 'block_replace',
                    '--block-id', $tgt[$p.nextIdx].id, '--content', '@./fx_insert.xml', '--as', 'user', '--format', 'json')
            } else {
                if (-not $curAnchor) { Log ("  跳过（无可用锚点）: {0}" -f $title); $okAll = $false; continue }
                $cmdArgs = @('docs', '+update', '--doc', $d.entry.target_obj_token, '--command', 'block_insert_after',
                    '--block-id', $curAnchor, '--content', '@./fx_insert.xml', '--as', 'user', '--format', 'json')
            }

            $file = Join-Path $d.dir $fileName
            $xmlParts | Out-File -LiteralPath $file -Encoding UTF8 -NoNewline
            $r = Invoke-Lark $cmdArgs $d.dir

            $newBlocks = @()
            if ($r.obj -and $r.obj.data -and $r.obj.data.document -and $r.obj.data.document.new_blocks) {
                $newBlocks = @($r.obj.data.document.new_blocks | Where-Object { $_.block_type -eq 'sheet' -or $_.block_type -eq 'whiteboard' })
            }
            if ($newBlocks.Count -eq 0) {
                $okAll = $false
                Log ("  插入失败 {0}: {1}" -f $title, (($r.err ?? $r.raw ?? 'no-output') -replace '\s+', ' ').Substring(0, [Math]::Min(160, (($r.err ?? $r.raw ?? 'no-output') -replace '\s+', ' ').Length)))
                continue
            }

            $nb = $newBlocks[0]
            $curAnchor = $nb.block_id
            $insCount++
            if ($item.tag -eq 'sheet') {
                $todo += [pscustomobject]@{ kind = 'sheetFill'; item = $item; token = $nb.block_token; sheetId = '' }
            }
            elseif ($item.wbType -ne 'mermaid') {
                $todo += [pscustomobject]@{ kind = 'wbImport'; item = $item; token = $nb.block_token }
            }
            Start-Sleep -Milliseconds 300
        }

        # ---- 回填表格数据 ----
        $filled = 0; $fillFail = 0
        if ($FillSheets) {
            foreach ($t in @($todo | Where-Object { $_.kind -eq 'sheetFill' })) {
                if ($t.sheetId) { $newSp = $t.token; $newSid = $t.sheetId }
                else {
                    $idx = $t.token.LastIndexOf('_')
                    if ($idx -lt 0) { $fillFail++; continue }
                    $newSp = $t.token.Substring(0, $idx)
                    $newSid = $t.token.Substring($idx + 1)
                }

                $gr = Invoke-Lark @('sheets', '+csv-get', '--spreadsheet-token', $t.item.token,
                    '--sheet-id', $t.item.sheetId, '--format', 'json', '--as', 'user') $d.dir
                if (-not $gr.obj -or -not $gr.obj.data -or -not $gr.obj.data.annotated_csv) { $fillFail++; continue }

                $csv = $gr.obj.data.annotated_csv -replace '(?m)^\[row=\d+\] ', ''
                if (-not $csv.Trim()) { continue }
                $csvFile = Join-Path $d.dir 'fx_sheet.csv'
                $csv | Out-File -LiteralPath $csvFile -Encoding UTF8 -NoNewline

                $pr = Invoke-Lark @('sheets', '+csv-put', '--spreadsheet-token', $newSp, '--sheet-id', $newSid,
                    '--start-cell', 'A1', '--csv', '@./fx_sheet.csv', '--as', 'user', '--format', 'json') $d.dir
                if ($pr.obj -and $pr.obj.ok -eq $true) { $filled++ }
                else {
                    $fillFail++
                    Log ("  回填失败 {0}: {1}" -f $title, (($pr.err ?? $pr.raw ?? 'no-output') -replace '\s+', ' ').Substring(0, [Math]::Min(160, (($pr.err ?? $pr.raw ?? 'no-output') -replace '\s+', ' ').Length)))
                }
                Start-Sleep -Milliseconds 300
            }
        }

        # ---- 导入 token 画板节点（目标侧新建空白，或迁移时已规范化成空白）----
        $imported = 0; $importFail = 0
        foreach ($t in @($todo | Where-Object { $_.kind -eq 'wbImport' })) {
            $srcFile = Join-Path $d.dir 'fx_wb_src.json'
            $ex = Invoke-Lark @('whiteboard', '+export', '--whiteboard-token', $t.item.token, '--output-type', 'raw', '--format', 'json', '--as', 'user') $d.dir
            if (-not ($ex.obj -and $ex.obj.data)) {
                $importFail++
                Log ("  画板导出失败 {0}: {1}" -f $title, (($ex.err ?? $ex.raw ?? '') -replace '\s+', ' '))
                continue
            }
            ($ex.obj.data | ConvertTo-Json -Depth 30) | Set-Content -LiteralPath $srcFile -Encoding UTF8
            $up = Invoke-Lark @('whiteboard', '+update', '--whiteboard-token', $t.token, '--input_format', 'raw',
                '--source', '@./fx_wb_src.json', '--overwrite', '--as', 'user', '--format', 'json') $d.dir
            if ($up.obj -and $up.obj.ok -eq $true) { $imported++ }
            else {
                $importFail++
                Log ("  画板导入失败 {0}: {1}" -f $title, (($up.err ?? $up.raw ?? '') -replace '\s+', ' '))
            }
            Start-Sleep -Milliseconds 300
        }

        $allSheets = @($todo | Where-Object { $_.kind -eq 'sheetFill' }).Count
        $allWbs = @($todo | Where-Object { $_.kind -eq 'wbImport' }).Count
        if ($importFail -gt 0) { $okAll = $false }

        $summary += [pscustomobject]@{
            title = $title; planned = $plan.Count + $present.Count
            sheets = $allSheets
            whiteboards = $allWbs
            filled = $filled; fillFail = $fillFail; ok = $okAll
        }
        Log ("完成 {0}: 插入 {1} 块，处理表格 {2}（回填 {3} 失败 {4}），画板 {5}（导入 {6} 失败 {7}）" -f `
                $title, $insCount, $allSheets, $filled, $fillFail, $allWbs, $imported, $importFail)
    }
    catch {
        Log ("异常 {0}: {1}" -f $title, $_.Exception.Message)
        $summary += [pscustomobject]@{ title = $title; planned = 0; sheets = 0; whiteboards = 0; filled = 0; fillFail = 0; ok = $false }
        if (-not $ContinueOnError) { throw }
    }
}

Log "================ 汇总 ================"
foreach ($s in $summary) {
    Log ("{0} | 计划 {1} | 表格 {2} | 画板 {3} | 回填 {4} | 失败 {5} | ok={6}" -f `
            $s.title, $s.planned, $s.sheets, $s.whiteboards, $s.filled, $s.fillFail, $s.ok)
}
Log ("合计：文档 {0} 篇，表格 {1}，画板 {2}，回填 {3}" -f `
        $summary.Count, `
        (($summary | Measure-Object sheets -Sum).Sum), `
        (($summary | Measure-Object whiteboards -Sum).Sum), `
        (($summary | Measure-Object filled -Sum).Sum))

if ($MarkSuccess -and -not $DryRun) {
    $okTitles = @($summary | Where-Object { $_.ok -and $_.fillFail -eq 0 } | ForEach-Object { $_.title })
    $updated = 0
    foreach ($k in $cp.Keys) {
        $e = $cp[$k]
        if ($e.status -ne 'partial') { continue }
        if ($OnlyTitle -and $e.title -notlike "*$OnlyTitle*") { continue }
        if ($okTitles -notcontains $e.title) { continue }
        $e.status = 'success'
        ($e | ConvertTo-Json -Depth 6 -Compress) | Add-Content -LiteralPath $CheckpointFile -Encoding UTF8
        $updated++
    }
    Log ("checkpoint 状态归位 success: {0} 条" -f $updated)
}
