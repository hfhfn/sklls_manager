param(
    [Parameter(Mandatory = $true)][string]$CheckpointFile,
    [Parameter(Mandatory = $true)][string]$TargetParentToken,
    [Parameter(Mandatory = $true)][string]$SpaceId,
    [switch]$Fix,
    [int]$MaxDepth = 12
)

<#
.SYNOPSIS
迁移后层级校验：把目标树一次性拉全，再与 checkpoint 的 1:1 父子映射比对。

.DESCRIPTION
- 不逐个节点调用 node-get，避免 O(n) 次 API 请求
- checkpoint 按 source_node_token 去重、后写入的覆盖先写入的
- -Fix 只执行 wiki +move 把节点挪到正确父节点，不删除、不重建
- 必须用 pwsh（PowerShell 7）运行：Windows PowerShell 5.1 读 UTF-8 checkpoint 会乱码导致 JSON 解析失败

.EXAMPLE
pwsh -NoProfile -File .\Verify-MigrationTree.ps1 `
  -CheckpointFile "..\migrate\migration_checkpoint.jsonl" `
  -TargetParentToken "LtigwlhiCirA24ksMAGc3KvwnCh" `
  -SpaceId "7687104096158878649"
#>

$ErrorActionPreference = 'Continue'

$entries = @{}
foreach ($line in Get-Content -LiteralPath $CheckpointFile) {
    if (-not $line.Trim()) { continue }
    try { $e = $line | ConvertFrom-Json } catch { continue }
    if (-not $e.source_node_token -or -not $e.target_node_token) { continue }
    $entries[$e.source_node_token] = $e   # 同一节点多条记录时以最后一条为准
}
Write-Host "checkpoint unique = $($entries.Count)"

$parents = @{}
function Collect {
    param([string]$Parent, [int]$Depth)
    if ($Depth -gt $MaxDepth) { return }
    # --page-all 必须显式传，否则只取第一页 50 条，大知识库会漏节点
    $raw = lark-cli wiki +node-list --space-id $SpaceId --parent-node-token $Parent `
        --page-all --page-limit 0 --page-size 50 --as user --format json 2>$null | ConvertFrom-Json
    if (-not $raw.data -or -not $raw.data.nodes) { return }
    foreach ($n in $raw.data.nodes) {
        $script:parents[$n.node_token] = $Parent
        if ($n.has_child) { Collect -Parent $n.node_token -Depth ($Depth + 1) }
    }
}
Collect -Parent $TargetParentToken -Depth 0
Write-Host "target nodes = $($parents.Count)"

$bad = @()
foreach ($e in $entries.Values) {
    $expected = $TargetParentToken
    if ($e.parent_source_node_token) {
        if (-not $entries.ContainsKey($e.parent_source_node_token)) {
            $bad += [pscustomobject]@{ title = $e.title; node = $e.target_node_token; expected = $null; actual = $parents[$e.target_node_token]; issue = 'parent not migrated' }
            continue
        }
        $expected = $entries[$e.parent_source_node_token].target_node_token
    }
    $actual = $parents[$e.target_node_token]
    if (-not $actual) {
        $bad += [pscustomobject]@{ title = $e.title; node = $e.target_node_token; expected = $expected; actual = 'MISSING'; issue = 'node not found in tree' }
        continue
    }
    if ($actual -ne $expected) {
        $bad += [pscustomobject]@{ title = $e.title; node = $e.target_node_token; depth = $e.depth; status = $e.status; actual = $actual; expected = $expected; issue = 'parent mismatch' }
    }
}

Write-Host "mismatch = $($bad.Count)"
$bad | ForEach-Object { $_ | Format-List | Out-String | Write-Host }

$statusBad = @($entries.Values | Where-Object { $_.status -ne 'success' })
Write-Host "status != success = $($statusBad.Count)"
$statusBad | ForEach-Object { Write-Host ("  {0} | {1} | imgFail={2}" -f $_.status, $_.title, $_.image_bind_failed) }

if ($Fix -and $bad.Count -gt 0) {
    foreach ($b in $bad) {
        if (-not $b.expected -or $b.actual -eq 'MISSING') {
            Write-Host "跳过（无法确定目标父节点）: $($b.title)"
            continue
        }
        $r = lark-cli wiki +move --node-token $b.node --target-parent-token $b.expected `
            --source-space-id $SpaceId --as user --format json 2>&1
        Write-Host "move $($b.title) -> $($b.expected) : $r"
    }
    Write-Host "修复完成，未删除任何节点"
}
