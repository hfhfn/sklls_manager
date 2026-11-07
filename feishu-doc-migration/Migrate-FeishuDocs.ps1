<#
.SYNOPSIS
飞书文档跨空间迁移脚本 v3 - 使用 lark-cli API 完整迁移文档（含子文档、图片、表格、内部引用修复）

.DESCRIPTION
- 递归迁移 Wiki 文档树（父文档 + 所有子文档）
- 保留所有格式：标题/列表/表格/代码块/引用（XML 直搬，不转 Markdown）
- 图片处理：从源文档下载 → 本地上传 → 替换 token 引用
  - 复制保护的文档自动回退到 media-preview
- 表格直接使用原始 XML，不做格式转换
- 内部引用修复：sub-page-list、@文档引用、文档链接全部指向新文档
- 目标支持：知识库根目录 或 指定父节点
- 带错误重试（指数退避）和实时进度输出
- 生成迁移日志和结果映射表

.PARAMETER SourceWikiUrls
源文档 Wiki URL 数组，可传入多个根文档

.PARAMETER TargetSpaceId
目标知识库空间 ID。与 TargetParentWikiUrl 二选一。
指定后文档将创建在目标知识库根目录下。

.PARAMETER TargetParentWikiUrl
目标知识库父节点 URL。与 TargetSpaceId 二选一。
指定后文档将作为该节点的子节点。

.PARAMETER WorkDir
临时工作目录，用于存放下载的图片和 XML 缓存（默认: .\lark_migration_temp）

.PARAMETER MaxRetries
API 调用最大重试次数（默认: 3）

.PARAMETER RetryBaseDelay
重试基础延迟秒数（指数退避: delay * 2^retry）（默认: 3）

.PARAMETER AsUser
以用户身份调用 lark-cli（默认: user）

.PARAMETER FixInternalRefs
是否修复内部文档引用（默认: $true）

.EXAMPLE
# 迁移到知识库根目录
.\Migrate-FeishuDocs.ps1 -SourceWikiUrls @("https://a.feishu.cn/wiki/xxx") -TargetSpaceId 7687020534646754274

.EXAMPLE
# 迁移到指定父节点下
.\Migrate-FeishuDocs.ps1 -SourceWikiUrls @("https://a.feishu.cn/wiki/xxx") -TargetParentWikiUrl "https://my.feishu.cn/wiki/yyy"
#>

param(
    [Parameter(Mandatory = $true)]
    [string[]]$SourceWikiUrls,

    [Parameter(Mandatory = $false)]
    [string]$TargetSpaceId = "",

    [Parameter(Mandatory = $false)]
    [string]$TargetParentWikiUrl = "",

    [string]$WorkDir = ".\lark_migration_temp",

    [int]$MaxRetries = 3,

    [int]$RetryBaseDelay = 3,

    [ValidateSet("user", "bot")]
    [string]$AsUser = "user",

    [bool]$FixInternalRefs = $true,

    # 每次写入最多携带的图片数；同步块/网格内的图片批量过大时绑定会歧义失败
    [int]$MaxImgsPerChunk = 1,

    # 仅重试 status=failed 的节点；partial（如图片无导出权限）本轮视为完成不再重试
    [switch]$OnlyRetryFailed
)

# ============================================================
# 参数校验
# ============================================================
if ([string]::IsNullOrWhiteSpace($TargetSpaceId) -and [string]::IsNullOrWhiteSpace($TargetParentWikiUrl)) {
    Write-Error "必须指定 -TargetSpaceId 或 -TargetParentWikiUrl 其中之一"
    exit 1
}

# ============================================================
# 全局状态
# ============================================================
$Script:MigratedCount = 0
$Script:FailedCount = 0
$Script:SkippedCount = 0
$Script:TotalDocs = 0
$Script:TotalFiles = 0
$Script:MigratedMap = @{}
$Script:DocIdMap = @{}
$Script:WikiTokenMap = @{}
$Script:LogFile = ""
$Script:ResultsFile = ""
$Script:TargetSpaceIdResolved = ""
$Script:TargetParentToken = ""

# ============================================================
# 工具函数
# ============================================================

function Write-Log {
    param(
        [string]$Message,
        [ValidateSet("INFO", "WARN", "ERROR", "SUCCESS", "PROGRESS")]
        [string]$Level = "INFO"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch ($Level) {
        "INFO" { "White" }
        "WARN" { "Yellow" }
        "ERROR" { "Red" }
        "SUCCESS" { "Green" }
        "PROGRESS" { "Cyan" }
    }
    $line = "[{0}] [{1}] {2}" -f $timestamp, $Level, $Message
    Write-Host $line -ForegroundColor $color
    if ($Script:LogFile) {
        Add-Content -Path $Script:LogFile -Value $line -Encoding UTF8
    }
}

function Write-ProgressBar {
    param(
        [int]$Current,
        [int]$Total,
        [string]$Activity,
        [string]$Status = ""
    )
    if ($Total -le 0) { return }
    $percent = [math]::Min(100, [math]::Round(($Current / $Total) * 100, 1))
    $barLen = 30
    $ratio = [math]::Min(1.0, [math]::Max(0.0, $Current / $Total))
    $filled = [math]::Floor($ratio * $barLen)
    $bar = ("#" * $filled) + ("-" * ($barLen - $filled))
    $msg = "[{0}] {1}% ({2}/{3}) {4}" -f $bar, $percent, $Current, $Total, $Activity
    if ($Status) { $msg += " - $Status" }
    Write-Log $msg -Level PROGRESS
}

function Invoke-LarkCli {
    param(
        [string[]]$Arguments,
        [switch]$Passthru,
        [string]$WorkingDir = ""
    )
    $attempt = 0
    $delay = $RetryBaseDelay

    while ($attempt -lt $MaxRetries) {
        $attempt++
        try {
            $procInfo = New-Object System.Diagnostics.ProcessStartInfo
            $procInfo.FileName = "lark-cli"
            $procInfo.Arguments = $Arguments -join " "
            $procInfo.RedirectStandardOutput = $true
            $procInfo.RedirectStandardError = $true
            $procInfo.UseShellExecute = $false
            $procInfo.CreateNoWindow = $true
            $procInfo.WorkingDirectory = if ($WorkingDir) { $WorkingDir } else { (Get-Location).Path }

            $proc = New-Object System.Diagnostics.Process
            $proc.StartInfo = $procInfo
            $proc.Start() | Out-Null
            $stdout = $proc.StandardOutput.ReadToEnd()
            $stderr = $proc.StandardError.ReadToEnd()
            $proc.WaitForExit()

            $combined = if ($stdout) { $stdout } else { $stderr }

            try {
                $result = $combined | ConvertFrom-Json -ErrorAction Stop
                if ($result.ok -eq $true) {
                    if ($Passthru) { return $result }
                    return $result.data
                }
                if ($result.error?.subtype -eq "rate_limit" -or $result.error?.code -eq 99991400 -or $result.error?.message -match "rate limit|too many requests") {
                    throw "Rate limited: $($result.error.message)"
                }
                Write-Log "API 错误 (不重试): $($result.error?.message ?? $combined)" -Level ERROR
                # 保留原始返回体供调用方判断“正文已写入但图片绑定歧义”这类部分成功
                if ($Passthru) { return $result }
                return $null
            }
            catch {
                if ($proc.ExitCode -eq 0) {
                    if ($Passthru) { return $stdout }
                    return $stdout
                }
                throw "ExitCode=$($proc.ExitCode): $combined"
            }
        }
        catch {
            if ($attempt -ge $MaxRetries) {
                Write-Log "lark-cli 调用失败（已重试 $attempt 次）: $($_.Exception.Message)" -Level ERROR
                return $null
            }
            Write-Log "lark-cli 调用失败，$delay 秒后重试 ($attempt/$MaxRetries): $($_.Exception.Message)" -Level WARN
            Start-Sleep -Seconds $delay
            $delay *= 2
        }
    }
    return $null
}

function SafeFileName {
    param([string]$Name)
    $invalid = [System.IO.Path]::GetInvalidFileNameChars()
    foreach ($c in $invalid) { $Name = $Name.Replace($c, '_') }
    $Name = $Name.Trim()
    if ($Name.Length -gt 80) { $Name = $Name.Substring(0, 80) }
    return $Name
}

function Resolve-RelativePath {
    param([string]$From, [string]$To)
    # 确保 From 以目录分隔符结尾，否则 Uri 会把它当作文件处理
    if (-not $From.EndsWith('\') -and -not $From.EndsWith('/')) {
        $From = $From + '\'
    }
    $fromUri = New-Object System.Uri($From)
    $toUri = New-Object System.Uri($To)
    $relativeUri = $fromUri.MakeRelativeUri($toUri)
    return [System.Uri]::UnescapeDataString($relativeUri.ToString()).Replace('/', '\')
}

# ============================================================
# Wiki 节点操作
# ============================================================

function Get-WikiNodeInfo {
    param([string]$NodeTokenOrUrl)
    Write-Log "解析节点: $NodeTokenOrUrl" -Level INFO
    $result = Invoke-LarkCli -Arguments @(
        "wiki", "+node-get",
        "--node-token", "`"$NodeTokenOrUrl`"",
        "--as", $AsUser
    )
    return $result
}

function Get-DriveDocInfo {
    param([string]$UrlOrToken)
    <#
    .DESCRIPTION
    解析独立云文档（不在知识库中的 /docx/ 等链接）。
    返回 @{ title; token; type; url }，失败返回 $null。
    #>
    Write-Log "非知识库节点，按独立云文档解析: $UrlOrToken" -Level INFO
    $result = Invoke-LarkCli -Arguments @(
        "drive", "+inspect",
        "--url", "`"$UrlOrToken`"",
        "--as", $AsUser
    ) -Passthru
    if ($result -and $result.ok -eq $true) {
        return $result.data
    }
    return $null
}

function Invoke-MigrateStandaloneDoc {
    param(
        [string]$SourceUrlOrToken,
        [string]$TargetParentToken,
        [string]$RootWorkDir
    )
    <#
    .DESCRIPTION
    迁移一个不属于任何知识库的独立云文档：直接读 docx、建目标节点、填内容。
    独立文档没有子节点，因此不走树扫描。
    #>
    $info = Get-DriveDocInfo -UrlOrToken $SourceUrlOrToken
    if (-not $info) {
        Write-Log "无法解析独立云文档: $SourceUrlOrToken" -Level ERROR
        $Script:FailedCount++
        return $null
    }

    if ($info.type -ne "docx") {
        Write-Log "跳过不支持的独立文档类型 [$($info.type)]: $($info.title)" -Level WARN
        $Script:SkippedCount++
        return $null
    }

    $node = [PSCustomObject]@{
        node_token        = $info.token
        obj_token         = $info.token
        obj_type          = "docx"
        title             = $info.title
        has_child         = $false
        parent_node_token = ""
        depth             = 0
    }

    Write-Log "独立文档: $($info.title) ($($info.token))" -Level INFO
    return Invoke-MigrateSingleDoc -SourceNode $node `
        -TargetParentToken $TargetParentToken `
        -RootWorkDir $RootWorkDir
}

function Get-WikiChildNodes {
    param(
        [string]$SpaceId,
        [string]$ParentNodeToken
    )
    $allNodes = @()
    $pageToken = ""
    $pageNum = 0

    do {
        $args = @(
            "wiki", "+node-list",
            "--space-id", $SpaceId,
            "--as", $AsUser,
            "--page-size", "50"
        )
        if ($ParentNodeToken) { $args += @("--parent-node-token", $ParentNodeToken) }
        if ($pageToken) { $args += @("--page-token", $pageToken) }

        $result = Invoke-LarkCli -Arguments $args
        if (-not $result) { break }

        $allNodes += $result.nodes
        $pageToken = $result.page_token
        $pageNum++

    } while ($result.has_more -and $pageToken -and $pageNum -lt 50)

    return $allNodes
}

function Get-WikiTreeRecursive {
    param(
        [string]$SpaceId,
        [string]$NodeToken,
        [int]$Depth = 0
    )
    $nodes = @()

    $nodeInfo = Get-WikiNodeInfo -NodeTokenOrUrl $NodeToken
    if (-not $nodeInfo) {
        Write-Log "无法获取节点信息: $NodeToken" -Level ERROR
        return $nodes
    }

    $nodes += [PSCustomObject]@{
        node_token        = $nodeInfo.node_token
        obj_token         = $nodeInfo.obj_token
        obj_type          = $nodeInfo.obj_type
        title             = $nodeInfo.title
        has_child         = $nodeInfo.has_child
        parent_node_token = $nodeInfo.parent_node_token
        space_id          = $nodeInfo.space_id
        depth             = $Depth
    }

    if ($nodeInfo.has_child) {
        $children = Get-WikiChildNodes -SpaceId $SpaceId -ParentNodeToken $NodeToken
        foreach ($child in $children) {
            $childNodes = Get-WikiTreeRecursive -SpaceId $SpaceId -NodeToken $child.node_token -Depth ($Depth + 1)
            $nodes += $childNodes
        }
    }

    return $nodes
}

function New-WikiDocNode {
    param(
        [string]$Title,
        [string]$TargetSpaceId,
        [string]$TargetParentToken = ""
    )
    <#
    .DESCRIPTION
    在目标知识库中创建空的 docx 节点（根目录或指定父节点下）
    #>
    $args = @(
        "wiki", "+node-create",
        "--space-id", $TargetSpaceId,
        "--title", "`"$Title`"",
        "--obj-type", "docx",
        "--as", $AsUser
    )
    if ($TargetParentToken) {
        $args += @("--parent-node-token", "`"$TargetParentToken`"")
    }

    Write-Log "  创建知识库节点: $Title" -Level INFO
    $result = Invoke-LarkCli -Arguments $args -Passthru

    if ($result -and $result.ok -eq $true) {
        return @{
            node_token = $result.data.node_token
            obj_token  = $result.data.obj_token
            url        = $result.data.url
            title      = $result.data.title
        }
    }
    return $null
}

# ============================================================
# 文档内容操作
# ============================================================

function Normalize-EmbeddedBlocks {
    param(
        [string]$XmlContent,
        [string]$DocLabel = ""
    )
    <#
    .DESCRIPTION
    写入前修正三类“API 不支持、但错误会被静默吞掉”的内嵌块，避免正文/图片丢失且不报错：
      1. <synced-source> 内部图片：无法绑定本地资源 → 移到同步块之后
      2. 含图片的 <grid>：列内图片同样无法绑定 → 扁平化为顺序块
      3. <sheet token> / <whiteboard token>：跨空间复制被服务端降级（2113/2105）→ 改为 blank 占位，
         表格数据与画板内容由 Fix-EmbeddedBlocks.ps1 迁移后回填
    #>
    $wrapped = "<root>" + ($XmlContent -replace '^\s*<\?xml[^>]*\?>', '') + "</root>"
    $doc = New-Object System.Xml.XmlDocument
    $doc.PreserveWhitespace = $false
    try { $doc.LoadXml($wrapped) }
    catch {
        Write-Log "  内嵌块规范化跳过（XML 解析异常）: $DocLabel $($_.Exception.Message)" -Level WARN
        return $XmlContent
    }

    # 1. 同步块内图片外移
    foreach ($ss in @($doc.SelectNodes("//synced-source"))) {
        $imgs = @($ss.SelectNodes(".//img"))
        if ($imgs.Count -eq 0) { continue }
        $anchorNode = $ss
        foreach ($img in $imgs) {
            $clone = $img.CloneNode($true)
            $anchorNode.ParentNode.InsertAfter($clone, $anchorNode)
            $anchorNode = $clone
            $img.ParentNode.RemoveChild($img) | Out-Null
        }
        Write-Log "  同步块内 $($imgs.Count) 张图片已外移: $DocLabel" -Level WARN
    }

    # 2. 含图片的 grid 扁平化
    foreach ($g in @($doc.SelectNodes("//grid"))) {
        if ($g.SelectNodes(".//img").Count -eq 0) { continue }
        $parent = $g.ParentNode
        if (-not $parent) { continue }
        $anchorNode = $g
        foreach ($col in @($g.SelectNodes("./column"))) {
            foreach ($child in @($col.ChildNodes)) {
                if ($child.NodeType -ne [System.Xml.XmlNodeType]::Element) { continue }
                $clone = $child.CloneNode($true)
                $parent.InsertAfter($clone, $anchorNode)
                $anchorNode = $clone
            }
        }
        $parent.RemoveChild($g) | Out-Null
        Write-Log "  含图片的 grid 已扁平化: $DocLabel" -Level WARN
    }

    # 3. 内嵌表格 / 画板：token 复制会被降级，改 blank 占位
    foreach ($sh in @($doc.SelectNodes("//sheet"))) {
        if ($sh.GetAttribute("type")) { continue }
        $blank = $doc.CreateElement("sheet")
        $blank.SetAttribute("type", "blank")
        $sh.ParentNode.ReplaceChild($blank, $sh) | Out-Null
        Write-Log "  内嵌表格 token=$($sh.GetAttribute('token')) 改为 blank，数据需迁移后回填: $DocLabel" -Level WARN
    }
    foreach ($wb in @($doc.SelectNodes("//whiteboard"))) {
        if ($wb.GetAttribute("type")) { continue }
        $wb.RemoveAllAttributes()
        $wb.SetAttribute("type", "blank")
        Write-Log "  画板 token 形式无法跨空间复制，已改为 blank 占位: $DocLabel" -Level WARN
    }

    $inner = ""
    foreach ($n in $doc.DocumentElement.ChildNodes) { $inner += $n.OuterXml }
    return $inner
}

function Get-DocContent {
    param([string]$DocUrlOrToken)
    Write-Log "读取文档内容: $DocUrlOrToken" -Level INFO
    $result = Invoke-LarkCli -Arguments @(
        "docs", "+fetch",
        "--doc", "`"$DocUrlOrToken`"",
        "--doc-format", "xml",
        "--detail", "full"
    ) -Passthru
    if ($result -and $result.ok) {
        # overwrite 只接受 <sub-page-list/>（带 space-id/wiki-token 属性的形式会被丢弃，
        # 并连带丢失其后的所有块），写入前统一收敛为自闭合无属性形式
        $content = $result.data.document.content
        $content = [regex]::Replace($content, '<sub-page-list[^>]*>.*?</sub-page-list>', '<sub-page-list/>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
        $content = [regex]::Replace($content, '<sub-page-list[^>]*/>', '<sub-page-list/>')
        # 修正无法通过 API 复制的内嵌块（同步块/网格图片、sheet、whiteboard）
        $content = Normalize-EmbeddedBlocks -XmlContent $content -DocLabel $DocUrlOrToken
        return @{
            content       = $content
            document_id   = $result.data.document.document_id
            revision_id   = $result.data.document.revision_id
            reference_map = $result.data.document.reference_map
        }
    }
    return $null
}

function Extract-ImageTokens {
    param([string]$XmlContent)
    $tokens = @()
    $pattern = '<img\s+[^>]*src="([^"]+)"'
    $matches = [regex]::Matches($XmlContent, $pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    foreach ($m in $matches) {
        $token = $m.Groups[1].Value
        if ($token -and $tokens -notcontains $token) {
            $tokens += $token
        }
    }
    return $tokens
}

function Extract-SourceTokens {
    param([string]$XmlContent)
    $sources = @()
    $pattern = '<source\s+[^>]*token="([^"]+)"[^>]*name="([^"]*)"'
    $matches = [regex]::Matches($XmlContent, $pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    foreach ($m in $matches) {
        $token = $m.Groups[1].Value
        $name = $m.Groups[2].Value
        if ($token) {
            $sources += [PSCustomObject]@{ token = $token; name = $name }
        }
    }
    return $sources
}

function Invoke-MediaDownload {
    param(
        [string]$Token,
        [string]$OutputPath,
        [string]$Type = "media"
    )
    $savedPath = $null
    # lark-cli 只允许把文件写到「当前工作目录」等白名单根目录内，
    # 因此让子进程在输出目录下运行，保证 --output 落在允许范围内
    $outDir = Split-Path $OutputPath -Parent
    if ($outDir -and -not (Test-Path $outDir)) {
        New-Item -ItemType Directory -Path $outDir -Force | Out-Null
    }

    # 1. 先尝试 media-download
    $result = Invoke-LarkCli -Arguments @(
        "docs", "+media-download",
        "--token", "`"$Token`"",
        "--output", "`"$OutputPath`"",
        "--type", $Type
    ) -Passthru -WorkingDir $outDir

    if ($result -and $result.ok) {
        $savedPath = $result.data?.saved_path
    }

    # 2. 失败则回退到 media-preview
    if (-not $savedPath) {
        Write-Log "    media-download 不可用，改用 media-preview" -Level WARN
        $previewResult = Invoke-LarkCli -Arguments @(
            "docs", "+media-preview",
            "--token", "`"$Token`"",
            "--output", "`"$OutputPath`"",
            "--overwrite"
        ) -Passthru -WorkingDir $outDir

        if ($previewResult -and $previewResult.ok) {
            $savedPath = $previewResult.data?.saved_path
        }
    }

    # 3. 验证文件存在
    if ($savedPath -and (Test-Path $savedPath)) {
        return $savedPath
    }
    if (Test-Path $OutputPath) { return $OutputPath }
    $dir = Split-Path $OutputPath -Parent
    $base = Split-Path $OutputPath -Leaf
    $found = Get-ChildItem -Path $dir -Filter "$base.*" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($found) { return $found.FullName }
    return $null
}

# ============================================================
# 文档创建（核心：wiki node-create + docs overwrite）
# ============================================================

function New-MigratedDocument {
    param(
        [string]$Title,
        [string]$XmlContent,
        [string]$TargetSpaceId,
        [string]$TargetParentToken,
        [string]$DocWorkDir,
        [hashtable]$TokenToLocalPath
    )
    <#
    .DESCRIPTION
    在目标知识库中创建文档并填充内容：
    1. wiki +node-create 创建空 docx 节点
    2. 将 XML 中图片/附件 token 替换为本地 path
    3. docs +update --command overwrite 填充完整内容（含图片上传）
    #>

    # 1. 在知识库中创建空节点
    $nodeInfo = New-WikiDocNode -Title $Title -TargetSpaceId $TargetSpaceId -TargetParentToken $TargetParentToken
    if (-not $nodeInfo) {
        Write-Log "  创建知识库节点失败: $Title" -Level ERROR
        return $null
    }

    $docToken = $nodeInfo.obj_token
    Write-Log "  节点已创建: $($nodeInfo.node_token)" -Level INFO

    # 2. 替换图片引用并 overwrite 填充内容
    $fill = Invoke-DocOverwrite -DocToken $docToken -XmlContent $XmlContent -DocWorkDir $DocWorkDir -TokenToLocalPath $TokenToLocalPath
    if ($fill.status -eq "failed") {
        # 关键：不删除节点。保留节点才能让子文档挂到正确父级，续跑时再重试填充，
        # 删除会导致其子孙被挂到上一级，出现层级错位。
        Write-Log "  填充内容失败，节点保留为空文档待续跑重试: $Title" -Level ERROR
        return @{
            document_id       = $docToken
            node_token        = $nodeInfo.node_token
            url               = $nodeInfo.url
            revision_id       = $null
            status            = "failed"
            image_bind_failed = 0
        }
    }

    if ($fill.status -eq "partial") {
        Write-Log "  正文已写入，但有 $($fill.image_bind_failed) 张图片未绑定（下次续跑会重试）: $Title" -Level WARN
    }
    return @{
        document_id       = $docToken
        node_token        = $nodeInfo.node_token
        url               = $nodeInfo.url
        revision_id       = $fill.revision_id
        status            = $fill.status
        image_bind_failed = $fill.image_bind_failed
    }
}

function Invoke-DocOverwriteChunked {
    param(
        [string]$DocToken,
        [string]$XmlContent,
        [string]$DocWorkDir,
        [int]$MaxChunkChars = 200000,
        [int]$MaxImgsPerChunk = 1
    )
    <#
    .DESCRIPTION
    超大文档单次 overwrite 会 server time out。按顶层块切分：
    第一块用 overwrite，后续用 append，逐块写入并汇总图片绑定失败数。
    同时按图片数量切分：同步块/网格图片一次性带太多会触发绑定歧义（1061044）。
    #>

    try {
        $wrapped = "<root>" + ($XmlContent -replace '^\s*<\?xml[^>]*\?>', '') + "</root>"
        $doc = New-Object System.Xml.XmlDocument
        $doc.LoadXml($wrapped)
    }
    catch {
        Write-Log "  分块失败：XML 解析异常 $($_.Exception.Message)" -Level ERROR
        return $null
    }

    $batches = @()
    $current = ""
    $curImgs = 0
    foreach ($node in $doc.DocumentElement.ChildNodes) {
        if ($node.NodeType -ne [System.Xml.XmlNodeType]::Element) { continue }
        $s = $node.OuterXml
        $nImgs = ([regex]::Matches($s, '<img\s')).Count
        $needSplit = $current -and (
            ($current.Length + $s.Length) -gt $MaxChunkChars -or
            ($curImgs + $nImgs) -gt $MaxImgsPerChunk
        )
        if ($needSplit) {
            $batches += $current
            $current = ""
            $curImgs = 0
        }
        $current += $s
        $curImgs += $nImgs
    }
    if ($current) { $batches += $current }

    Write-Log "  分块写入：共 $($batches.Count) 批" -Level INFO
    $imgFail = 0
    $last = $null
    for ($i = 1; $i -le $batches.Count; $i++) {
        $fileName = "chunk_$i.xml"
        $filePath = Join-Path $DocWorkDir $fileName
        $batches[$i - 1] | Out-File -LiteralPath $filePath -Encoding UTF8 -NoNewline

        $command = if ($i -eq 1) { "overwrite" } else { "append" }
        $updateArgs = @(
            "docs", "+update",
            "--doc", "`"$DocToken`"",
            "--command", $command,
            "--doc-format", "xml",
            "--content", "`"@./$fileName`"",
            "--as", $AsUser
        )
        Write-Log "  分块 $i/$($batches.Count) ($command)" -Level INFO
        $r = Invoke-LarkCli -Arguments $updateArgs -Passthru -WorkingDir $DocWorkDir
        if (-not $r -or ($r.ok -ne $true -and -not $r.data.document.url)) {
            Write-Log "  分块 $i 写入失败" -Level ERROR
            return $null
        }
        $imgFail += @($r.data.local_resource_failures | Where-Object { $_.kind -eq "image" }).Count
        $last = $r
    }

    return @{
        status            = if ($imgFail -gt 0 -or $last.ok -ne $true) { "partial" } else { "success" }
        image_bind_failed = $imgFail
        revision_id       = $last.data.document.revision_id
    }
}

function Invoke-DocOverwrite {
    param(
        [string]$DocToken,
        [string]$XmlContent,
        [string]$DocWorkDir,
        [hashtable]$TokenToLocalPath
    )
    <#
    .DESCRIPTION
    把图片/附件 token 替换为本地路径后执行 overwrite。
    返回 status：success（完整写入）/ partial（正文写入但部分图片未绑定）/ failed（未写入）
    #>

    # 替换图片引用
    $modifiedXml = $XmlContent
    foreach ($token in $TokenToLocalPath.Keys) {
        $localPath = $TokenToLocalPath[$token]
        if (-not $localPath) { continue }

        $relativePath = Resolve-RelativePath -From $DocWorkDir -To $localPath
        $safePath = [System.Security.SecurityElement]::Escape($relativePath)
        $pattern = '(<img\s+[^>]*)src="' + [regex]::Escape($token) + '"([^>]*>)'
        $replacement = "`$1path=`"@./$safePath`"`$2"
        $modifiedXml = [regex]::Replace($modifiedXml, $pattern, $replacement, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    }

    $xmlFileName = "content.xml"
    $xmlFilePath = Join-Path $DocWorkDir $xmlFileName
    if (-not (Test-Path -LiteralPath $DocWorkDir)) {
        New-Item -ItemType Directory -Path $DocWorkDir -Force | Out-Null
    }
    $modifiedXml | Out-File -LiteralPath $xmlFilePath -Encoding UTF8 -NoNewline

    $overwriteArgs = @(
        "docs", "+update",
        "--doc", "`"$DocToken`"",
        "--command", "overwrite",
        "--doc-format", "xml",
        "--content", "`"@./$xmlFileName`"",
        "--as", $AsUser
    )

    Write-Log "  填充内容（overwrite）" -Level INFO
    $result = Invoke-LarkCli -Arguments $overwriteArgs -Passthru -WorkingDir $DocWorkDir

    # 图片绑定歧义时 API 返回 ok=false，但正文块已写入（data.result=success/partial_success），需按 partial 处理
    $opResult = $result.data.result
    $wrote = $result -and ($result.ok -eq $true -or $opResult -eq "success" -or $opResult -eq "partial_success" -or $result.data.document.url)
    if (-not $wrote) {
        # 超大文档单次 overwrite 会 server time out，降级为“首块 overwrite + 后续 append”
        Write-Log "  单次写入失败，改用分块写入" -Level WARN
        $chunked = Invoke-DocOverwriteChunked -DocToken $DocToken -XmlContent $modifiedXml -DocWorkDir $DocWorkDir -MaxImgsPerChunk $MaxImgsPerChunk
        if ($chunked) { return $chunked }
        return @{ status = "failed"; image_bind_failed = 0; revision_id = $null }
    }

    $imgFail = @($result.data.local_resource_failures | Where-Object { $_.kind -eq "image" }).Count
    $status = if ($imgFail -gt 0 -or $opResult -eq "partial_success" -or $result.ok -ne $true) { "partial" } else { "success" }
    return @{
        status            = $status
        image_bind_failed = $imgFail
        revision_id       = $result.data.document.revision_id
    }
}

function Update-DocContent {
    param(
        [string]$DocToken,
        [string]$NewXmlContent,
        [string]$DocWorkDir
    )
    <#
    .DESCRIPTION
    用 overwrite 更新文档内容（用于修复内部引用后重新写入）
    #>
    $xmlFileName = "content_repaired.xml"
    $xmlFilePath = Join-Path $DocWorkDir $xmlFileName
    $NewXmlContent | Out-File -LiteralPath $xmlFilePath -Encoding UTF8 -NoNewline

    $args = @(
        "docs", "+update",
        "--doc", "`"$DocToken`"",
        "--command", "overwrite",
        "--doc-format", "xml",
        "--content", "`"@./$xmlFileName`"",
        "--as", $AsUser
    )

    Write-Log "  更新文档内容（修复引用）" -Level INFO

    $result = Invoke-LarkCli -Arguments $args -Passthru -WorkingDir $DocWorkDir
    if ($result -and $result.ok -eq $true) {
        return $true
    }
    Write-Log "  更新失败" -Level WARN
    return $false
}

# ============================================================
# 内部引用修复
# ============================================================

function Repair-InternalReferences {
    param(
        [string]$CurrentXml
    )
    <#
    .DESCRIPTION
    修复文档中的内部引用，使其指向迁移后的新文档
    修复内容：
    1. <sub-page-list space-id=X wiki-token=Y> -> 新 space-id / wiki-token
    2. <sub-page doc-id=Z> -> 新 doc-id
    3. <cite type="doc" doc-id=Z> -> 新 doc-id
    4. <a href="...feishu.cn/wiki/TOKEN"> -> 新 wiki URL
    5. <a href="...feishu.cn/docx/TOKEN"> -> 新 docx URL
    #>

    $modified = $CurrentXml
    $changed = $false

    # 1. 修复 sub-page-list 的 space-id 和 wiki-token
    $splPattern = '<sub-page-list\s+([^>]*)\s?/?>'
    $splMatches = [regex]::Matches($modified, $splPattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    foreach ($m in $splMatches) {
        $oldFullTag = $m.Value
        $attrs = $m.Groups[1].Value
        $newAttrs = $attrs

        # space-id 替换
        $spaceMatch = [regex]::Match($newAttrs, 'space-id="([^"]*)"', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
        if ($spaceMatch.Success -and $Script:TargetSpaceIdResolved) {
            $newAttrs = $newAttrs.Replace($spaceMatch.Value, 'space-id="' + $Script:TargetSpaceIdResolved + '"')
            $changed = $true
        }

        # wiki-token 替换
        $wikiMatch = [regex]::Match($newAttrs, 'wiki-token="([^"]*)"', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
        if ($wikiMatch.Success -and $Script:WikiTokenMap.ContainsKey($wikiMatch.Groups[1].Value)) {
            $newWiki = $Script:WikiTokenMap[$wikiMatch.Groups[1].Value]
            $newAttrs = $newAttrs.Replace($wikiMatch.Value, 'wiki-token="' + $newWiki + '"')
            $changed = $true
        }

        if ($changed -and $newAttrs -ne $attrs) {
            $newFullTag = $oldFullTag.Replace($attrs, $newAttrs)
            $modified = $modified.Replace($oldFullTag, $newFullTag)
        }
    }

    # 2. 修复 <sub-page doc-id="...">
    $subPagePattern = '<sub-page\s+[^>]*doc-id="([^"]*)"[^>]*/?>'
    $subPageMatches = [regex]::Matches($modified, $subPagePattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    foreach ($m in $subPageMatches) {
        $srcDocId = $m.Groups[1].Value
        # doc-id 可能是文档 obj_token，也可能是 wiki 节点 token，两者都要查
        $newDocId = $null
        if ($Script:DocIdMap.ContainsKey($srcDocId)) { $newDocId = $Script:DocIdMap[$srcDocId] }
        elseif ($Script:WikiTokenMap.ContainsKey($srcDocId)) { $newDocId = $Script:WikiTokenMap[$srcDocId] }
        if ($newDocId) {
            $oldVal = 'doc-id="' + $srcDocId + '"'
            $newVal = 'doc-id="' + $newDocId + '"'
            $modified = $modified.Replace($oldVal, $newVal)
            $changed = $true
        }
    }

    # 3. 修复 <cite type="doc" doc-id="...">
    $citePattern = 'cite\s+[^>]*doc-id="([^"]*)"'
    $citeMatches = [regex]::Matches($modified, $citePattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    foreach ($m in $citeMatches) {
        $srcDocId = $m.Groups[1].Value
        # cite 的 doc-id 也可能是 wiki 节点 token
        $newDocId = $null
        if ($Script:DocIdMap.ContainsKey($srcDocId)) { $newDocId = $Script:DocIdMap[$srcDocId] }
        elseif ($Script:WikiTokenMap.ContainsKey($srcDocId)) { $newDocId = $Script:WikiTokenMap[$srcDocId] }
        if ($newDocId) {
            $oldVal = 'doc-id="' + $srcDocId + '"'
            $newVal = 'doc-id="' + $newDocId + '"'
            $modified = $modified.Replace($oldVal, $newVal)
            $changed = $true
        }
    }

    # 4. 修复 <a href="...feishu.cn/wiki/TOKEN"> 链接
    $wikiLinkPattern = '<a\s+[^>]*href="([^"]*feishu\.cn/wiki/([A-Za-z0-9]+)[^"]*)"[^>]*>'
    $wikiLinkMatches = [regex]::Matches($modified, $wikiLinkPattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    foreach ($m in $wikiLinkMatches) {
        $fullUrl = $m.Groups[1].Value
        $wikiToken = $m.Groups[2].Value
        if ($Script:WikiTokenMap.ContainsKey($wikiToken)) {
            $newToken = $Script:WikiTokenMap[$wikiToken]
            $newUrl = $fullUrl.Replace($wikiToken, $newToken)
            $modified = $modified.Replace($fullUrl, $newUrl)
            $changed = $true
        }
    }

    # 5. 修复 <a href="...feishu.cn/docx/TOKEN"> 链接
    $docxLinkPattern = '<a\s+[^>]*href="([^"]*feishu\.cn/docx/([A-Za-z0-9]+)[^"]*)"[^>]*>'
    $docxLinkMatches = [regex]::Matches($modified, $docxLinkPattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    foreach ($m in $docxLinkMatches) {
        $fullUrl = $m.Groups[1].Value
        $docxToken = $m.Groups[2].Value
        if ($Script:DocIdMap.ContainsKey($docxToken)) {
            $newToken = $Script:DocIdMap[$docxToken]
            $newUrl = $fullUrl.Replace($docxToken, $newToken)
            $modified = $modified.Replace($fullUrl, $newUrl)
            $changed = $true
        }
    }

    if (-not $changed) {
        return $CurrentXml
    }
    return $modified
}

# ============================================================
# 核心迁移流程
# ============================================================

function Invoke-MigrateSingleDoc {
    param(
        [PSCustomObject]$SourceNode,
        [string]$TargetParentToken,
        [string]$RootWorkDir,
        [string]$ExistingNodeToken,
        [string]$ExistingObjToken
    )
    <#
    .DESCRIPTION
    迁移单个文档：
    1. 获取文档内容
    2. 下载图片和附件
    3. 在目标知识库创建节点并填充内容
    4. 返回目标节点信息
    #>
    $title = $SourceNode.title
    $nodeToken = $SourceNode.node_token
    $objType = $SourceNode.obj_type
    $sourceObjToken = $SourceNode.obj_token

    if ($objType -ne "docx") {
        Write-Log "跳过非 docx 类型节点 [$objType]: $title" -Level WARN
        $Script:SkippedCount++
        return $null
    }

    $safeTitle = SafeFileName $title
    $docDirName = "{0}_{1}" -f $nodeToken.Substring(0, [Math]::Min(8, $nodeToken.Length)), $safeTitle
    $docWorkDir = Join-Path $RootWorkDir $docDirName
    if (-not (Test-Path $docWorkDir)) {
        New-Item -ItemType Directory -Path $docWorkDir -Force | Out-Null
    }

    # 1. 获取文档内容
    $docContent = Get-DocContent -DocUrlOrToken $nodeToken
    if (-not $docContent) {
        Write-Log "无法读取文档内容: $title" -Level ERROR
        $Script:FailedCount++
        return $null
    }

    $xml = $docContent.content

    # 2. 提取并下载图片
    $imageTokens = Extract-ImageTokens -XmlContent $xml
    $tokenToPath = @{}

    if ($imageTokens.Count -gt 0) {
        Write-Log "  发现 $($imageTokens.Count) 张图片，开始下载..." -Level INFO
        $imgDir = Join-Path $docWorkDir "images"
        if (-not (Test-Path $imgDir)) {
            New-Item -ItemType Directory -Path $imgDir -Force | Out-Null
        }

        for ($i = 0; $i -lt $imageTokens.Count; $i++) {
            $token = $imageTokens[$i]
            $imgOutput = Join-Path $imgDir "img_$i"
            $shortToken = $token.Substring(0, [Math]::Min(12, $token.Length))
            Write-ProgressBar -Current ($i + 1) -Total $imageTokens.Count -Activity "下载图片" -Status $shortToken
            $downloaded = Invoke-MediaDownload -Token $token -OutputPath $imgOutput
            if ($downloaded) {
                $tokenToPath[$token] = $downloaded
            }
            else {
                Write-Log "  图片下载失败: $token" -Level WARN
            }
        }
        Write-Log "  图片下载完成: $($tokenToPath.Count)/$($imageTokens.Count) 成功" -Level INFO
    }

    # 3. 提取并下载文件附件
    $sourceTokens = Extract-SourceTokens -XmlContent $xml
    if ($sourceTokens.Count -gt 0) {
        Write-Log "  发现 $($sourceTokens.Count) 个附件，开始下载..." -Level INFO
        $fileDir = Join-Path $docWorkDir "files"
        if (-not (Test-Path $fileDir)) {
            New-Item -ItemType Directory -Path $fileDir -Force | Out-Null
        }

        for ($i = 0; $i -lt $sourceTokens.Count; $i++) {
            $src = $sourceTokens[$i]
            $baseName = if ($src.name) { SafeFileName $src.name } else { "file_$i" }
            $fileOutput = Join-Path $fileDir $baseName
            Write-ProgressBar -Current ($i + 1) -Total $sourceTokens.Count -Activity "下载附件" -Status $baseName
            $downloaded = Invoke-MediaDownload -Token $src.token -OutputPath $fileOutput
            if ($downloaded) {
                $tokenToPath[$src.token] = $downloaded
                $pattern = '(<source\s+[^>]*)token="' + [regex]::Escape($src.token) + '"([^>]*name="[^"]*"[^>]*>)'
                $relativePath = Resolve-RelativePath -From $docWorkDir -To $downloaded
                $safePath = [System.Security.SecurityElement]::Escape($relativePath)
                $replacement = "`$1path=`"@./$safePath`"`$2"
                $xml = [regex]::Replace($xml, $pattern, $replacement, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
            }
            else {
                Write-Log "  附件下载失败: $($src.token) ($($src.name))" -Level WARN
            }
        }
    }

    # 4. 创建节点并填充内容；续跑时直接复用已存在节点重试填充，不重复建节点
    if ($ExistingNodeToken -and $ExistingObjToken) {
        Write-Log "  复用已存在节点，重试内容填充: $ExistingNodeToken" -Level WARN
        $fill = Invoke-DocOverwrite -DocToken $ExistingObjToken -XmlContent $xml `
            -DocWorkDir $docWorkDir -TokenToLocalPath $tokenToPath
        if ($fill.status -eq "failed") {
            Write-Log "  内容填充重试失败，节点保留待下次重试: $title" -Level ERROR
            $Script:FailedCount++
            $Script:MigratedMap[$nodeToken] = @{
                title             = $title
                status            = "failed"
                target_node_token = $ExistingNodeToken
                target_obj_token  = $ExistingObjToken
            }
            return @{
                node_token = $ExistingNodeToken
                obj_token  = $ExistingObjToken
                title      = $title
                url        = $null
                status     = "failed"
            }
        }
        $created = @{
            document_id       = $ExistingObjToken
            node_token        = $ExistingNodeToken
            url               = "https://my.feishu.cn/wiki/$ExistingNodeToken"
            status            = $fill.status
            image_bind_failed = $fill.image_bind_failed
        }
    }
    else {
        $created = New-MigratedDocument -Title $title -XmlContent $xml `
            -TargetSpaceId $Script:TargetSpaceIdResolved `
            -TargetParentToken $TargetParentToken `
            -DocWorkDir $docWorkDir `
            -TokenToLocalPath $tokenToPath

        if (-not $created) {
            $Script:FailedCount++
            $Script:MigratedMap[$nodeToken] = @{ title = $title; status = "failed" }
            return $null
        }
    }

    $targetNodeToken = $created.node_token
    $targetObjToken = $created.document_id

    if ($created.status -eq "failed") {
        $Script:FailedCount++
        Write-Log "  迁移未完成（空文档已保留，续跑将重试填充）: $title" -Level ERROR
    }
    elseif ($created.status -eq "partial") {
        $Script:MigratedCount++
        Write-Log "  迁移完成（部分图片未绑定，待续跑重试）: $title" -Level WARN
    }
    else {
        $Script:MigratedCount++
        Write-Log "  迁移成功: $title" -Level SUCCESS
    }
    if ($created.url) { Write-Log "    文档: $($created.url)" -Level SUCCESS }

    # 保存迁移映射
    $Script:MigratedMap[$nodeToken] = @{
        title             = $title
        source_node_token = $nodeToken
        source_obj_token  = $sourceObjToken
        target_obj_token  = $targetObjToken
        target_node_token = $targetNodeToken
        image_count       = $imageTokens.Count
        status            = $created.status
        doc_work_dir      = $docWorkDir
        original_xml      = $xml
    }

    # 更新全局映射表（用于内部引用修复）
    $Script:DocIdMap[$sourceObjToken] = $targetObjToken
    $Script:WikiTokenMap[$nodeToken] = $targetNodeToken

    return @{
        node_token         = $targetNodeToken
        obj_token          = $targetObjToken
        title              = $title
        url                = $created.url
        doc_work_dir       = $docWorkDir
        status             = $created.status
        image_bind_failed  = $created.image_bind_failed
    }
}

function Invoke-MigrateSingleFile {
    param(
        [PSCustomObject]$SourceNode,
        [string]$TargetParentToken,
        [string]$RootWorkDir
    )
    <#
    .DESCRIPTION
    迁移单个文件附件：
    1. 下载源文件（media-preview 方式，兼容复制保护）
    2. 上传到目标知识库父节点下
    3. 返回目标节点信息
    #>
    $title = $SourceNode.title
    $nodeToken = $SourceNode.node_token
    $objToken = $SourceNode.obj_token

    $safeTitle = SafeFileName $title
    $docDirName = "{0}_{1}" -f $nodeToken.Substring(0, [Math]::Min(8, $nodeToken.Length)), $safeTitle
    $docWorkDir = Join-Path $RootWorkDir $docDirName
    if (-not (Test-Path $docWorkDir)) {
        New-Item -ItemType Directory -Path $docWorkDir -Force | Out-Null
    }

    # 1. 下载文件
    Write-Log "  下载文件: $title" -Level INFO
    $outputPath = Join-Path $docWorkDir "source_file"
    $downloaded = Invoke-MediaDownload -Token $objToken -OutputPath $outputPath -Type "file"

    if (-not $downloaded) {
        Write-Log "  文件下载失败: $title" -Level ERROR
        $Script:FailedCount++
        return $null
    }

    $fileSize = (Get-Item $downloaded).Length
    Write-Log "  下载完成: $([math]::Round($fileSize/1MB, 2)) MB" -Level INFO

    # 2. 上传到目标知识库
    Write-Log "  上传文件到知识库..." -Level INFO

    $args = @(
        "drive", "+upload",
        "--file", "`"$downloaded`"",
        "--name", "`"$title`"",
        "--as", $AsUser
    )
    if ($TargetParentToken) {
        $args += @("--wiki-token", "`"$TargetParentToken`"")
    }
    else {
        $args += @("--folder-token", "root")
    }

    $result = Invoke-LarkCli -Arguments $args -Passthru

    if (-not $result -or $result.ok -ne $true) {
        Write-Log "  文件上传失败: $title" -Level ERROR
        $Script:FailedCount++
        return $null
    }

    $Script:MigratedCount++
    $newFileToken = $result.data.file_token

    # 3. 获取对应的 wiki node token
    $targetNodeToken = ""
    if ($TargetParentToken) {
        # 上传到 wiki 节点下，需要查询子节点找到新创建的 file 节点
        $children = Get-WikiChildNodes -SpaceId $Script:TargetSpaceIdResolved -ParentNodeToken $TargetParentToken
        $newNode = $children | Where-Object { $_.obj_token -eq $newFileToken } | Select-Object -First 1
        if ($newNode) {
            $targetNodeToken = $newNode.node_token
        }
    }

    Write-Log "  迁移成功: $title" -Level SUCCESS

    # 保存迁移映射
    $Script:MigratedMap[$nodeToken] = @{
        title             = $title
        source_node_token = $nodeToken
        source_obj_token  = $objToken
        target_obj_token  = $newFileToken
        target_node_token = $targetNodeToken
        file_size         = $fileSize
        status            = "success"
    }

    return @{
        node_token = $targetNodeToken
        obj_token  = $newFileToken
        title      = $title
    }
}

function Invoke-RepairAllInternalRefs {
    param([array]$MigratedDocs, [string]$RootWorkDir)
    <#
    .DESCRIPTION
    所有文档迁移完成后，批量修复内部引用（overwrite 方式）
    #>
    Write-Log ""
    Write-Log "========================================" -Level INFO
    Write-Log "第二阶段：修复内部文档引用" -Level INFO
    Write-Log "========================================" -Level INFO

    $total = $MigratedDocs.Count
    $fixedCount = 0
    $skipCount = 0
    $failCount = 0

    for ($i = 0; $i -lt $total; $i++) {
        $doc = $MigratedDocs[$i]
        Write-Log "[$($i+1)/$total] 修复引用: $($doc.title)" -Level INFO

        # 直接读取目标文档当前 XML 再按 token 映射修复：已修复的文档不会被二次改写，
        # 断点续跑时无需依赖上一次运行的原始 XML
        $currentObjToken = if ($doc.target_obj_token) { $doc.target_obj_token } else { $Script:MigratedMap[$doc.source_node_token].target_obj_token }
        if (-not $currentObjToken) {
            Write-Log "  跳过（缺少目标文档 token）" -Level WARN
            $skipCount++
            continue
        }

        $current = Get-DocContent -DocUrlOrToken $currentObjToken
        if (-not $current) {
            Write-Log "  读取目标文档失败" -Level WARN
            $failCount++
            continue
        }

        $repairedXml = Repair-InternalReferences -CurrentXml $current.content
        if ($repairedXml -eq $current.content) {
            Write-Log "  无需修改" -Level INFO
            $skipCount++
            continue
        }

        $repairDir = Join-Path $RootWorkDir ("repair_" + $currentObjToken.Substring(0, [Math]::Min(10, $currentObjToken.Length)))
        if (-not (Test-Path $repairDir)) {
            New-Item -ItemType Directory -Path $repairDir -Force | Out-Null
        }

        $updated = Update-DocContent -DocToken $currentObjToken `
            -NewXmlContent $repairedXml `
            -DocWorkDir $repairDir

        if ($updated) {
            Write-Log "  修复完成 ✓" -Level SUCCESS
            $fixedCount++
        }
        else {
            Write-Log "  修复失败（内容已创建，但引用未更新）" -Level ERROR
            $failCount++
        }
    }

    Write-Log ""
    Write-Log "引用修复完成：修复 $fixedCount 个，无需修改 $skipCount 个，失败 $failCount 个" -Level SUCCESS
}

function Invoke-MigrateTree {
    param(
        [string]$SourceRootNodeToken,
        [string]$SourceSpaceId,
        [string]$TargetParentToken,
        [string]$RootWorkDir
    )
    <#
    .DESCRIPTION
    递归迁移整个文档树（深度优先，先父后子）
    第一阶段：迁移所有文档（内容+图片+创建wiki节点）
    第二阶段：修复所有内部引用
    #>

    # 第一阶段：扫描 + 迁移
    Write-Log "正在扫描源文档树..." -Level INFO
    $tree = Get-WikiTreeRecursive -SpaceId $SourceSpaceId -NodeToken $SourceRootNodeToken -Depth 0
    $docxCount = ($tree | Where-Object { $_.obj_type -eq "docx" }).Count
    $fileCount = ($tree | Where-Object { $_.obj_type -eq "file" }).Count
    $Script:TotalDocs = $docxCount
    $Script:TotalFiles = $fileCount
    $totalMigratable = $docxCount + $fileCount
    Write-Log "发现 $($tree.Count) 个节点：$docxCount 个文档 + $fileCount 个附件" -Level SUCCESS

    if ($totalMigratable -eq 0) {
        Write-Log "没有可迁移的内容" -Level WARN
        return
    }

    # 注意：$tree 已经是深度优先遍历的正确顺序（与源文档一致），不要重新排序
    $migratedDocs = @()
    $targetParentMap = @{}
    # 源节点的父节点映射（用于父节点被跳过/创建失败时向上回溯，避免子孙被挂到根目录）
    $sourceParentMap = @{}
    foreach ($n in $tree) {
        if ($n.node_token -and $n.parent_node_token) {
            $sourceParentMap[$n.node_token] = $n.parent_node_token
        }
    }

    # 断点续跑：checkpoint 记录每个节点的状态
    # success = 已完整迁移，跳过；partial / failed = 节点已存在但内容不完整，
    # 续跑时必须复用该节点重试填充，不允许「看到节点存在就跳过」
    $checkpointFile = Join-Path $RootWorkDir "migration_checkpoint.jsonl"
    $resumeMap = @{}
    if (Test-Path $checkpointFile) {
        foreach ($line in Get-Content $checkpointFile) {
            if (-not $line.Trim()) { continue }
            try { $entry = $line | ConvertFrom-Json } catch { continue }
            if (-not $entry.source_node_token -or -not $entry.target_node_token) { continue }
            $resumeMap[$entry.source_node_token] = $entry   # 后写入的状态覆盖先前状态
        }

        $doneCount = 0
        $retryCount = 0
        foreach ($entry in $resumeMap.Values) {
            $status = if ($entry.status) { $entry.status } else { "success" }
            if ($OnlyRetryFailed -and $status -eq "partial") { $status = "success" }
            $targetParentMap[$entry.source_node_token] = $entry.target_node_token
            if ($status -eq "success") {
                $doneCount++
                if ($entry.obj_type -eq "docx") {
                    $migratedDocs += [PSCustomObject]@{
                        source_node_token = $entry.source_node_token
                        title             = $entry.title
                        target_node_token = $entry.target_node_token
                        target_obj_token  = $entry.target_obj_token
                    }
                }
            }
            else { $retryCount++ }

            # 恢复全局 token 映射，保证续跑时内部引用也能正确修复
            if ($entry.obj_type -eq "docx" -and $entry.target_obj_token) {
                $Script:WikiTokenMap[$entry.source_node_token] = $entry.target_node_token
                if ($entry.source_obj_token) {
                    $Script:DocIdMap[$entry.source_obj_token] = $entry.target_obj_token
                }
            }
        }

        if ($doneCount -gt 0 -or $retryCount -gt 0) {
            Write-Log "断点续跑：已完成 $doneCount 个节点（跳过），$retryCount 个节点未完成（将复用节点重试填充）" -Level SUCCESS
            $Script:MigratedCount += $doneCount
        }
    }

    $processedCount = 0
    $migratedDocCount = 0
    Write-Log ""
    Write-Log "========================================" -Level INFO
    Write-Log "第一阶段：文档迁移" -Level INFO
    Write-Log "========================================" -Level INFO

    foreach ($node in $tree) {
        $processedCount++
        $indent = "  " * $node.depth
        Write-Log ""
        Write-Log "[$processedCount/$($tree.Count)] $indent[$($node.depth)] $($node.title) [$($node.obj_type)]" -Level PROGRESS

        # 确定目标父节点：沿源祖先链向上查找最近一个已成功迁移（或本身被跳过）的祖先
        $targetParent = $TargetParentToken
        $cursor = $node.parent_node_token
        $hops = 0
        while ($cursor -and $hops -lt 50) {
            if ($targetParentMap.ContainsKey($cursor)) {
                $targetParent = $targetParentMap[$cursor]
                break
            }
            $cursor = $sourceParentMap[$cursor]
            $hops++
        }

        # 断点续跑状态判断：只有 success 才跳过；partial/failed 复用已存在节点重试填充
        $existingNodeToken = $null
        $existingObjToken = $null
        $resumeEntry = $null
        if ($node.node_token -and $resumeMap.ContainsKey($node.node_token)) {
            $resumeEntry = $resumeMap[$node.node_token]
        }
        if ($resumeEntry) {
            $resumeStatus = if ($resumeEntry.status) { $resumeEntry.status } else { "success" }
            if ($OnlyRetryFailed -and $resumeStatus -eq "partial") { $resumeStatus = "success" }
            if ($resumeStatus -eq "success") {
                Write-Log "  已完成，跳过（断点续跑）" -Level WARN
                continue
            }
            $checkArgs = @("wiki", "+node-get", "--node-token", "`"$($resumeEntry.target_node_token)`"", "--as", $AsUser)
            $nodeCheck = Invoke-LarkCli -Arguments $checkArgs -Passthru
            if ($nodeCheck -and $nodeCheck.ok -eq $true) {
                $existingNodeToken = $resumeEntry.target_node_token
                $existingObjToken = $resumeEntry.target_obj_token
                Write-Log "  上次状态=$resumeStatus，复用节点重试填充" -Level WARN
            }
            else {
                Write-Log "  上次未完成且目标节点已不存在，重新创建" -Level WARN
                $targetParentMap.Remove($node.node_token)
            }
        }

        $result = $null
        if ($node.obj_type -eq "docx") {
            $migratedDocCount++
            $result = Invoke-MigrateSingleDoc -SourceNode $node `
                -TargetParentToken $targetParent `
                -RootWorkDir $RootWorkDir `
                -ExistingNodeToken $existingNodeToken `
                -ExistingObjToken $existingObjToken
        }
        elseif ($node.obj_type -eq "file") {
            $result = Invoke-MigrateSingleFile -SourceNode $node `
                -TargetParentToken $targetParent `
                -RootWorkDir $RootWorkDir
        }
        else {
            Write-Log "  跳过不支持的类型: $($node.obj_type)" -Level WARN
            $Script:SkippedCount++
        }

        if ($result) {
            $nodeStatus = if ($result.status) { $result.status } else { "success" }
            $targetParentMap[$node.node_token] = $result.node_token
            if ($node.obj_type -eq "docx" -and $nodeStatus -ne "failed") {
                $migratedDocs += [PSCustomObject]@{
                    source_node_token = $node.node_token
                    title             = $node.title
                    target_node_token = $result.node_token
                    target_obj_token  = $result.obj_token
                }
            }
            # 落盘 checkpoint：status 为 success/partial/failed，续跑据此决定跳过还是重试
            $checkpointEntry = @{
                source_node_token        = $node.node_token
                source_obj_token         = $node.obj_token
                parent_source_node_token = $node.parent_node_token
                target_node_token        = $result.node_token
                target_obj_token         = $result.obj_token
                title                    = $node.title
                obj_type                 = $node.obj_type
                depth                    = $node.depth
                status                   = $nodeStatus
                image_bind_failed        = $result.image_bind_failed
            } | ConvertTo-Json -Compress
            Add-Content -Path $checkpointFile -Value $checkpointEntry -Encoding UTF8
        }

        Write-ProgressBar -Current $processedCount -Total $($tree.Count) -Activity "迁移进度" -Status "成功:$Script:MigratedCount 失败:$Script:FailedCount 跳过:$Script:SkippedCount"
    }

    # 第二阶段：修复内部引用
    if ($FixInternalRefs -and $migratedDocs.Count -gt 0) {
        Invoke-RepairAllInternalRefs -MigratedDocs $migratedDocs -RootWorkDir $RootWorkDir
    }

    Write-Log ""
    Write-Log "========================================" -Level SUCCESS
    Write-Log "迁移完成！" -Level SUCCESS
    Write-Log "  总计成功: $Script:MigratedCount（文档 + 附件）" -Level SUCCESS
    Write-Log "  失败: $Script:FailedCount" -Level ERROR
    Write-Log "  跳过: $Script:SkippedCount" -Level WARN
    Write-Log "========================================" -Level SUCCESS
}

# ============================================================
# 主入口
# ============================================================

function Main {
    Write-Log ""
    Write-Log "========================================" -Level INFO
    Write-Log "  飞书文档迁移工具 v3" -Level INFO
    Write-Log "  （wiki node-create + overwrite 方案）" -Level INFO
    Write-Log "========================================" -Level INFO
    Write-Log "源文档数量: $($SourceWikiUrls.Count)"
    if ($TargetSpaceId) { Write-Log "目标空间 ID: $TargetSpaceId (根目录)" }
    if ($TargetParentWikiUrl) { Write-Log "目标父节点: $TargetParentWikiUrl" }
    Write-Log "工作目录: $WorkDir"
    Write-Log "重试次数: $MaxRetries"
    Write-Log "身份: $AsUser"
    Write-Log "修复内部引用: $FixInternalRefs"
    Write-Log "========================================"
    Write-Log ""

    # 初始化工作目录
    $absWorkDir = Resolve-Path $WorkDir -ErrorAction SilentlyContinue
    if (-not $absWorkDir) {
        $absWorkDir = New-Item -ItemType Directory -Path $WorkDir -Force | Select-Object -ExpandProperty FullName
    }
    else {
        $absWorkDir = $absWorkDir.Path
    }
    $Script:LogFile = Join-Path $absWorkDir ("migration_{0}.log" -f (Get-Date -Format "yyyyMMdd_HHmmss"))
    $Script:ResultsFile = Join-Path $absWorkDir ("migration_results_{0}.json" -f (Get-Date -Format "yyyyMMdd_HHmmss"))
    Write-Log "日志文件: $Script:LogFile" -Level INFO
    Write-Log "结果文件: $Script:ResultsFile" -Level INFO

    # 解析目标
    if ($TargetParentWikiUrl) {
        Write-Log "正在解析目标父节点..." -Level INFO
        $targetInfo = Get-WikiNodeInfo -NodeTokenOrUrl $TargetParentWikiUrl
        if (-not $targetInfo) {
            Write-Log "无法解析目标父节点，请检查 URL 和权限" -Level ERROR
            exit 1
        }
        $Script:TargetSpaceIdResolved = $targetInfo.space_id
        $Script:TargetParentToken = $targetInfo.node_token
        Write-Log "目标空间: $($targetInfo.space_id)" -Level SUCCESS
        Write-Log "目标父节点: $($targetInfo.title) ($($targetInfo.node_token))" -Level SUCCESS
    }
    else {
        $Script:TargetSpaceIdResolved = $TargetSpaceId
        $Script:TargetParentToken = ""
        Write-Log "目标空间: $TargetSpaceId（根目录）" -Level SUCCESS
    }

    # 逐个迁移源文档
    foreach ($sourceUrl in $SourceWikiUrls) {
        Write-Log ""
        Write-Log "========================================" -Level INFO
        Write-Log "开始迁移: $sourceUrl" -Level INFO
        Write-Log "========================================" -Level INFO

        $sourceInfo = Get-WikiNodeInfo -NodeTokenOrUrl $sourceUrl
        if (-not $sourceInfo) {
            # 不在知识库中的独立云文档（常见于直接给的 /docx/ 链接）
            Write-Log "源链接不是知识库节点，按独立云文档方式迁移" -Level WARN

            $Script:MigratedCount = 0
            $Script:FailedCount = 0
            $Script:SkippedCount = 0
            $Script:TotalDocs = 0
            $Script:TotalFiles = 0

            $standaloneResult = Invoke-MigrateStandaloneDoc `
                -SourceUrlOrToken $sourceUrl `
                -TargetParentToken $Script:TargetParentToken `
                -RootWorkDir $absWorkDir

            if (-not $standaloneResult) {
                Write-Log "独立云文档迁移失败: $sourceUrl" -Level ERROR
            }
            continue
        }

        $sourceSpaceId = $sourceInfo.space_id
        $sourceNodeToken = $sourceInfo.node_token
        Write-Log "源空间: $sourceSpaceId" -Level INFO
        Write-Log "源文档: $($sourceInfo.title) ($sourceNodeToken)" -Level INFO

        $safeRootName = SafeFileName $sourceInfo.title
        $rootWorkDir = Join-Path $absWorkDir $safeRootName
        if (-not (Test-Path $rootWorkDir)) {
            New-Item -ItemType Directory -Path $rootWorkDir -Force | Out-Null
        }

        $Script:MigratedCount = 0
        $Script:FailedCount = 0
        $Script:SkippedCount = 0
        $Script:TotalDocs = 0
        $Script:TotalFiles = 0

        Invoke-MigrateTree -SourceRootNodeToken $sourceNodeToken `
            -SourceSpaceId $sourceSpaceId `
            -TargetParentToken $Script:TargetParentToken `
            -RootWorkDir $rootWorkDir
    }

    # 保存结果
    $docResults = @{}
    foreach ($key in $Script:MigratedMap.Keys) {
        $val = $Script:MigratedMap[$key]
        $cleanVal = @{}
        foreach ($k in $val.Keys) {
            if ($k -ne "original_xml" -and $k -ne "doc_work_dir") {
                $cleanVal[$k] = $val[$k]
            }
        }
        $docResults[$key] = $cleanVal
    }

    $results = @{
        migrated_at        = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        source_urls        = $SourceWikiUrls
        target_space_id    = $Script:TargetSpaceIdResolved
        target_parent      = $Script:TargetParentToken
        fix_internal_refs  = $FixInternalRefs
        total_migrated     = $Script:MigratedCount
        total_failed       = $Script:FailedCount
        total_skipped      = $Script:SkippedCount
        documents          = $docResults
        doc_id_mapping     = $Script:DocIdMap
        wiki_token_mapping = $Script:WikiTokenMap
    }
    $results | ConvertTo-Json -Depth 10 | Out-File -FilePath $Script:ResultsFile -Encoding UTF8
    Write-Log ""
    Write-Log "结果已保存到: $Script:ResultsFile" -Level SUCCESS
    Write-Log "日志已保存到: $Script:LogFile" -Level SUCCESS
}

# 启动
Main
