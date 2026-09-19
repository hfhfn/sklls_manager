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

    [bool]$FixInternalRefs = $true
)

# ============================================================
# lark-cli 路径配置（自动探测）
# ============================================================
$Script:LarkCliPath = $null
$possiblePaths = @(
    "C:\Users\hfhfn\.trae-cn\plugins\trae-remote-official\lark\1.0.5\bin\lark-cli.exe",
    (Get-Command lark-cli -ErrorAction SilentlyContinue)?.Source
)
foreach ($p in $possiblePaths) {
    if ($p -and (Test-Path $p)) {
        $Script:LarkCliPath = $p
        break
    }
}
if (-not $Script:LarkCliPath) {
    Write-Error "找不到 lark-cli，请确保已安装并在 PATH 中"
    exit 1
}

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
        [switch]$Passthru
    )
    $attempt = 0
    $delay = $RetryBaseDelay

    while ($attempt -lt $MaxRetries) {
        $attempt++
        try {
            $procInfo = New-Object System.Diagnostics.ProcessStartInfo
            $procInfo.FileName = $Script:LarkCliPath
            # 使用 ArgumentList 正确处理含空格的参数
            foreach ($arg in $Arguments) {
                $procInfo.ArgumentList.Add($arg) | Out-Null
            }
            $procInfo.RedirectStandardOutput = $true
            $procInfo.RedirectStandardError = $true
            $procInfo.UseShellExecute = $false
            $procInfo.CreateNoWindow = $true
            $procInfo.WorkingDirectory = (Get-Location).Path

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
                # partial_success：ok=false 但内容已写入，透传给调用方处理
                if ($result.data -and $result.data.result -eq "partial_success") {
                    if ($Passthru) { return $result }
                    return $result.data
                }
                if ($result.error?.subtype -eq "rate_limit" -or $result.error?.code -eq 99991400 -or $result.error?.message -match "rate limit|too many requests") {
                    throw "Rate limited: $($result.error.message)"
                }
                Write-Log "API 错误 (不重试): $($result.error?.message ?? $combined)" -Level ERROR
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
        "--node-token", $NodeTokenOrUrl,
        "--as", $AsUser
    )
    return $result
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
        "--title", $Title,
        "--obj-type", "docx",
        "--as", $AsUser
    )
    if ($TargetParentToken) {
        $args += @("--parent-node-token", $TargetParentToken)
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

function Get-DocContent {
    param([string]$DocUrlOrToken)
    Write-Log "读取文档内容: $DocUrlOrToken" -Level INFO
    $result = Invoke-LarkCli -Arguments @(
        "docs", "+fetch",
        "--doc", $DocUrlOrToken,
        "--doc-format", "xml",
        "--detail", "full"
    ) -Passthru
    if ($result -and $result.ok) {
        return @{
            content       = $result.data.document.content
            document_id   = $result.data.document.document_id
            revision_id   = $result.data.document.revision_id
            reference_map = $result.data.document.reference_map
        }
    }
    return $null
}

function Extract-ImageTokens {
    param([string]$XmlContent)
    $tokens = New-Object System.Collections.Generic.List[string]
    $pattern = '<img\s+[^>]*src="([^"]+)"'
    $matches = [regex]::Matches($XmlContent, $pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    foreach ($m in $matches) {
        $token = $m.Groups[1].Value
        if ($token -and $tokens -notcontains $token) {
            $tokens.Add($token)
        }
    }
    return ,$tokens.ToArray()
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

    # 1. 先尝试 media-download
    $result = Invoke-LarkCli -Arguments @(
        "docs", "+media-download",
        "--token", $Token,
        "--output", $OutputPath,
        "--type", $Type
    ) -Passthru

    if ($result -and $result.ok) {
        $savedPath = $result.data?.saved_path
    }

    # 2. 失败则回退到 media-preview
    if (-not $savedPath) {
        Write-Log "    media-download 不可用，改用 media-preview" -Level WARN
        $previewResult = Invoke-LarkCli -Arguments @(
            "docs", "+media-preview",
            "--token", $Token,
            "--output", $OutputPath
        ) -Passthru

        if ($previewResult -and $previewResult.ok) {
            $savedPath = $previewResult.data?.saved_path
        }
    }

    # 3. 验证文件存在
    if ($savedPath -and (Test-Path -LiteralPath $savedPath)) {
        return $savedPath
    }
    if (Test-Path -LiteralPath $OutputPath) { return $OutputPath }
    $dir = Split-Path $OutputPath -Parent
    $base = Split-Path $OutputPath -Leaf
    $found = Get-ChildItem -LiteralPath $dir -Filter "$base.*" -ErrorAction SilentlyContinue | Select-Object -First 1
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

    # 2. 替换图片引用（使用相对路径，overwrite 时切换工作目录）
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

    # 3. 写入 XML 文件（用 .NET 方法避免 PowerShell 通配符解析问题）
    $xmlFileName = "content.xml"
    $xmlFilePath = Join-Path $DocWorkDir $xmlFileName
    [System.IO.File]::WriteAllText($xmlFilePath, $modifiedXml, [System.Text.UTF8Encoding]::new($false))

    # 4. overwrite 填充内容
    $args = @(
        "docs", "+update",
        "--doc", $docToken,
        "--command", "overwrite",
        "--doc-format", "xml",
        "--content", "@$xmlFilePath",
        "--as", $AsUser
    )

    Write-Log "  填充内容（overwrite）: $Title" -Level INFO

    $originalCwd = Get-Location
    try {
        Set-Location $DocWorkDir
        $result = Invoke-LarkCli -Arguments $args -Passthru
        if ($result -and $result.ok -eq $true) {
            return @{
                document_id = $docToken
                node_token  = $nodeInfo.node_token
                url         = $nodeInfo.url
                revision_id = $result.data.document.revision_id
            }
        }
        
        # partial_success：文档内容已写入，只是部分资源（图片/附件）失败，视为成功
        if ($result -and $result.data -and $result.data.result -eq "partial_success") {
            $failCount = ($result.data.local_resource_failures | Measure-Object).Count
            Write-Log "  部分成功: $Title（$failCount 个资源失败，文档内容已写入）" -Level WARN
            return @{
                document_id = $docToken
                node_token  = $nodeInfo.node_token
                url         = $nodeInfo.url
                revision_id = $result.data.document.revision_id
                partial     = $true
                failed_resources = $failCount
            }
        }
        
        Write-Log "  填充内容失败: $Title" -Level ERROR
        
        # 回滚：删除已创建的空节点
        Write-Log "  回滚：删除已创建的空节点" -Level WARN
        $nodeUrl = "https://my.feishu.cn/wiki/$($nodeInfo.node_token)"
        Invoke-LarkCli -Arguments @("wiki", "+node-delete", "--node-token", $nodeUrl, "--yes") | Out-Null
        
        return $null
    }
    finally {
        Set-Location $originalCwd
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
    [System.IO.File]::WriteAllText($xmlFilePath, $NewXmlContent, [System.Text.UTF8Encoding]::new($false))

    $args = @(
        "docs", "+update",
        "--doc", $DocToken,
        "--command", "overwrite",
        "--doc-format", "xml",
        "--content", "@$xmlFilePath",
        "--as", $AsUser
    )

    Write-Log "  更新文档内容（修复引用）" -Level INFO

    $originalCwd = Get-Location
    try {
        $result = Invoke-LarkCli -Arguments $args -Passthru
        if ($result -and $result.ok -eq $true) {
            return $true
        }
        Write-Log "  更新失败" -Level WARN
        return $false
    }
    finally {
        Set-Location $originalCwd
    }
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
        if ($Script:DocIdMap.ContainsKey($srcDocId)) {
            $newDocId = $Script:DocIdMap[$srcDocId]
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
        if ($Script:DocIdMap.ContainsKey($srcDocId)) {
            $newDocId = $Script:DocIdMap[$srcDocId]
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
        [string]$RootWorkDir
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
    if (-not (Test-Path -LiteralPath $docWorkDir)) {
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
        if (-not (Test-Path -LiteralPath $imgDir)) {
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
        if (-not (Test-Path -LiteralPath $fileDir)) {
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

    # 4. 在目标知识库创建文档并填充内容
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

    $Script:MigratedCount++
    $targetNodeToken = $created.node_token
    $targetObjToken = $created.document_id

    Write-Log "  迁移成功: $title" -Level SUCCESS
    Write-Log "    Wiki: https://my.feishu.cn/wiki/$targetNodeToken" -Level SUCCESS

    # 保存迁移映射
    $Script:MigratedMap[$nodeToken] = @{
        title             = $title
        source_node_token = $nodeToken
        source_obj_token  = $sourceObjToken
        target_obj_token  = $targetObjToken
        target_node_token = $targetNodeToken
        image_count       = $imageTokens.Count
        status            = "success"
        doc_work_dir      = $docWorkDir
        original_xml      = $xml
    }

    # 更新全局映射表（用于内部引用修复）
    $Script:DocIdMap[$sourceObjToken] = $targetObjToken
    $Script:WikiTokenMap[$nodeToken] = $targetNodeToken

    return @{
        node_token   = $targetNodeToken
        obj_token    = $targetObjToken
        title        = $title
        doc_work_dir = $docWorkDir
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
    if (-not (Test-Path -LiteralPath $docWorkDir)) {
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
        "--file", $downloaded,
        "--name", $title,
        "--as", $AsUser
    )
    if ($TargetParentToken) {
        $args += @("--wiki-token", $TargetParentToken)
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
    param([array]$MigratedDocs)
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

        $migInfo = $Script:MigratedMap[$doc.source_node_token]
        if (-not $migInfo -or $migInfo.status -ne "success") {
            Write-Log "  跳过（迁移未成功）" -Level WARN
            $skipCount++
            continue
        }

        # 修复 XML 中的引用
        $repairedXml = Repair-InternalReferences -CurrentXml $migInfo.original_xml

        if ($repairedXml -eq $migInfo.original_xml) {
            Write-Log "  无需修改" -Level INFO
            $skipCount++
            continue
        }

        # 写入修复后的 XML 并更新文档
        $updated = Update-DocContent -DocToken $migInfo.target_obj_token `
            -NewXmlContent $repairedXml `
            -DocWorkDir $migInfo.doc_work_dir

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

        # 确定目标父节点
        $targetParent = $TargetParentToken
        if ($node.parent_node_token -and $targetParentMap.ContainsKey($node.parent_node_token)) {
            $targetParent = $targetParentMap[$node.parent_node_token]
        }
        elseif ($node.depth -gt 0 -and $node.parent_node_token) {
            # 父节点迁移失败，跳过所有子节点，避免乱跑到根目录
            Write-Log "  父节点迁移失败，跳过: $($node.title)" -Level WARN
            $Script:FailedCount++
            $Script:MigratedMap[$node.node_token] = @{ title = $node.title; status = "skipped_parent_failed" }
            Write-ProgressBar -Current $processedCount -Total $($tree.Count) -Activity "迁移进度" -Status "成功:$Script:MigratedCount 失败:$Script:FailedCount 跳过:$Script:SkippedCount"
            continue
        }

        $result = $null
        if ($node.obj_type -eq "docx") {
            $migratedDocCount++
            $result = Invoke-MigrateSingleDoc -SourceNode $node `
                -TargetParentToken $targetParent `
                -RootWorkDir $RootWorkDir
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
            $targetParentMap[$node.node_token] = $result.node_token
            if ($node.obj_type -eq "docx") {
                $migratedDocs += [PSCustomObject]@{
                    source_node_token = $node.node_token
                    title             = $node.title
                    target_node_token = $result.node_token
                }
            }
        }

        Write-ProgressBar -Current $processedCount -Total $($tree.Count) -Activity "迁移进度" -Status "成功:$Script:MigratedCount 失败:$Script:FailedCount 跳过:$Script:SkippedCount"
    }

    # 第二阶段：修复内部引用
    if ($FixInternalRefs -and $migratedDocs.Count -gt 0) {
        Invoke-RepairAllInternalRefs -MigratedDocs $migratedDocs
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
            Write-Log "无法解析源文档: $sourceUrl，跳过" -Level ERROR
            $Script:FailedCount++
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
