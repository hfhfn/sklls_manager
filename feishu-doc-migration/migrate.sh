#!/bin/bash
# ============================================================
# 飞书文档迁移工具 - 纯 Bash 版本 v4.0
# 依赖: lark-cli, jq
# 支持: macOS / Linux
# 功能: wiki 递归迁移 + 独立 docx 迁移 + 图片/附件 + 内部引用修复
# ============================================================

set -euo pipefail

# ---- 颜色定义 ----
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ---- 全局变量 ----
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORK_DIR="./lark_migration_temp"
MAX_RETRIES=3
RETRY_BASE_DELAY=3
AS_USER="user"
FIX_INTERNAL_REFS=true
TARGET_SPACE_ID=""
TARGET_PARENT_WIKI_URL=""
SOURCE_URLS=()
LOG_FILE=""
RESULT_FILE=""

# 映射表文件
WIKI_TOKEN_MAP=""   # source_wiki_token -> target_wiki_token
DOC_ID_MAP=""       # source_doc_id -> target_doc_id
MIGRATION_LOG=""    # 详细迁移记录

# 计数器
TOTAL_DOCS=0
SUCCESS_DOCS=0
FAILED_DOCS=0
SKIPPED_DOCS=0

# 失败的父节点 token 集合（用于跳过其子节点）
FAILED_PARENTS_FILE=""

# ============================================================
# 工具函数
# ============================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1" >> "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [SUCCESS] $1" >> "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WARN] $1" >> "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" >> "$LOG_FILE"
}

# 带重试的 lark-cli 调用
# 用法: lark_cli <输出变量名> <子命令> [参数...]
lark_cli() {
    local out_var="$1"
    shift
    local cmd_args=("$@")
    local attempt=1
    local delay=$RETRY_BASE_DELAY
    local result
    local exit_code

    while [ $attempt -le $MAX_RETRIES ]; do
        # 执行 lark-cli 命令，捕获输出和错误
        set +e
        result=$(lark-cli "${cmd_args[@]}" --as "$AS_USER" 2>&1)
        exit_code=$?
        set -e

        if [ $exit_code -eq 0 ]; then
            # 检查 JSON 是否有效（含 data 或 code:0，或 partial_success）
            if echo "$result" | jq -e '.code == 0 or .data or (.data.result == "partial_success")' > /dev/null 2>&1; then
                eval "$out_var=\$result"
                return 0
            fi
        fi

        # 检查是否 rate limited（需要重试）
        local is_rate_limit=false
        if echo "$result" | jq -e '.error.subtype == "rate_limit" or .error.code == 99991400' > /dev/null 2>&1; then
            is_rate_limit=true
        fi
        if echo "$result" | grep -qi "rate limit\|too many requests" > /dev/null 2>&1; then
            is_rate_limit=true
        fi

        # partial_success 不重试，直接返回
        if echo "$result" | jq -e '.data.result == "partial_success"' > /dev/null 2>&1; then
            eval "$out_var=\$result"
            return 0
        fi

        if [ $attempt -lt $MAX_RETRIES ]; then
            log_warn "lark-cli 调用失败 (第 $attempt 次)，${delay}秒后重试..."
            log_warn "  命令: lark-cli ${cmd_args[*]}"
            log_warn "  错误: $(echo "$result" | head -3)"
            sleep "$delay"
            delay=$((delay * 2))
        fi
        attempt=$((attempt + 1))
    done

    log_error "lark-cli 调用失败，已重试 $MAX_RETRIES 次"
    log_error "  命令: lark-cli ${cmd_args[*]}"
    log_error "  输出: $result"
    return 1
}

# 标记父节点为失败（其子节点将被跳过）
mark_parent_failed() {
    local parent_token="$1"
    echo "$parent_token" >> "$FAILED_PARENTS_FILE"
}

# 检查父节点是否失败
is_parent_failed() {
    local parent_token="$1"
    if [ -z "$parent_token" ]; then
        return 1
    fi
    grep -qxF "$parent_token" "$FAILED_PARENTS_FILE" 2>/dev/null
}

# 从 wiki URL 提取 token
extract_wiki_token() {
    local url="$1"
    # 匹配 /wiki/TOKEN 或 /wiki/TOKEN?xxx
    echo "$url" | sed -n 's|.*/wiki/\([A-Za-z0-9_-]*\).*|\1|p'
}

# 从 wiki URL 提取 space-id（如果 URL 中包含）
extract_space_id() {
    local url="$1"
    echo "$url" | sed -n 's|.*space_id=\([0-9]*\).*|\1|p'
}

# 进度条
show_progress() {
    local current=$1
    local total=$2
    local label=$3
    local percent=$((current * 100 / total))
    local filled=$((percent / 2))
    local empty=$((50 - filled))
    printf "\r${CYAN}[%3d%%]${NC} [%-50s] %d/%d %s" "$percent" "$(printf '%0.s#' $(seq 1 $filled) 2>/dev/null)" "$current" "$total" "$label"
}

# ============================================================
# Wiki 节点操作
# ============================================================

# 获取 wiki 节点信息
# 用法: get_wiki_node_info <result_var> <wiki_token>
get_wiki_node_info() {
    local out_var="$1"
    local wiki_token="$2"
    local result

    log_info "获取节点信息: $wiki_token"
    lark_cli result "wiki +node-get --wiki-token $wiki_token" || return 1
    eval "$out_var=\$result"
}

# 获取 wiki 子节点列表
# 用法: get_wiki_children <result_var> <space_id> <parent_token>
get_wiki_children() {
    local out_var="$1"
    local space_id="$2"
    local parent_token="$3"
    local result
    local all_items="[]"
    local page_token=""
    local has_more=true

    while [ "$has_more" = true ]; do
        local cmd="wiki +node-list --space-id $space_id"
        if [ -n "$parent_token" ]; then
            cmd="$cmd --parent-node-token $parent_token"
        fi
        if [ -n "$page_token" ]; then
            cmd="$cmd --page-token $page_token"
        fi

        lark_cli result "$cmd" || return 1

        local items
        items=$(echo "$result" | jq -c '.data.items // []')
        all_items=$(echo "$all_items $items" | jq -s '.[0] + .[1]')

        has_more=$(echo "$result" | jq -r '.data.has_more // false')
        page_token=$(echo "$result" | jq -r '.data.page_token // ""')
    done

    eval "$out_var=\$all_items"
}

# 递归获取整个 wiki 树
# 用法: get_wiki_tree <result_var> <space_id> <root_token> <depth>
# 输出: JSON 数组，每项包含 token, title, obj_type, obj_token, parent_token, depth
get_wiki_tree() {
    local out_var="$1"
    local space_id="$2"
    local root_token="$3"
    local depth="${4:-0}"
    local result="[]"

    log_info "扫描 wiki 节点 (depth=$depth): $root_token"

    # 获取子节点
    local children
    get_wiki_children children "$space_id" "$root_token" || return 1

    local count
    count=$(echo "$children" | jq 'length')

    for ((i=0; i<count; i++)); do
        local child
        child=$(echo "$children" | jq -c ".[$i]")

        local token title obj_type obj_token parent_tok
        token=$(echo "$child" | jq -r '.node_token')
        title=$(echo "$child" | jq -r '.title')
        obj_type=$(echo "$child" | jq -r '.obj_type')
        obj_token=$(echo "$child" | jq -r '.obj_token')
        parent_tok=$(echo "$child" | jq -r '.parent_node_token // ""')

        local node_info
        node_info=$(jq -n \
            --arg token "$token" \
            --arg title "$title" \
            --arg obj_type "$obj_type" \
            --arg obj_token "$obj_token" \
            --arg parent "$parent_tok" \
            --argjson depth "$depth" \
            '{node_token: $token, title: $title, obj_type: $obj_type, obj_token: $obj_token, parent_token: $parent, depth: $depth}')

        result=$(echo "$result" | jq --argjson node "$node_info" '. + [$node]')

        # 递归处理子节点
        local subtree
        if get_wiki_tree subtree "$space_id" "$token" $((depth + 1)) 2>/dev/null; then
            result=$(echo "$result $subtree" | jq -s '.[0] + .[1]')
        fi
    done

    eval "$out_var=\$result"
}

# 在目标知识库创建 wiki 节点
# 用法: create_wiki_node <result_var> <space_id> <title> <obj_type> <parent_token>
create_wiki_node() {
    local out_var="$1"
    local space_id="$2"
    local title="$3"
    local obj_type="$4"
    local parent_token="$5"
    local result

    local cmd="wiki +node-create --space-id $space_id --title '$title' --obj-type $obj_type"
    if [ -n "$parent_token" ]; then
        cmd="$cmd --parent-node-token $parent_token"
    fi

    lark_cli result "$cmd" || return 1
    eval "$out_var=\$result"
}

# ============================================================
# 文档操作
# ============================================================

# 获取文档内容 (XML)
# 用法: get_doc_content <result_var> <doc_token>
get_doc_content() {
    local out_var="$1"
    local doc_token="$2"
    local result

    lark_cli result "docs +fetch --doc $doc_token --doc-format xml --detail full" || return 1

    # 提取 content 字段
    local content
    content=$(echo "$result" | jq -r '.data.document.content // ""')

    if [ -z "$content" ]; then
        log_error "文档内容为空: $doc_token"
        return 1
    fi

    eval "$out_var=\$content"
}

# 更新文档内容 (overwrite)
# 返回值: 0=成功, 1=失败, 2=partial_success（内容已写入，部分资源失败）
# 用法: update_doc_content <doc_token> <xml_file> <result_var>
update_doc_content() {
    local doc_token="$1"
    local xml_file="$2"
    local out_var="${3:-}"
    local result

    if ! lark_cli result "docs +update --doc $doc_token --command overwrite --content @$xml_file --doc-format xml"; then
        return 1
    fi

    # 检查是否 partial_success
    local is_partial
    is_partial=$(echo "$result" | jq -r '.data.result // ""')

    if [ -n "$out_var" ]; then
        eval "$out_var=\$result"
    fi

    if [ "$is_partial" = "partial_success" ]; then
        return 2
    fi
    return 0
}

# ============================================================
# 图片处理
# ============================================================

# 从 XML 中提取所有图片的 src token
# 用法: extract_image_tokens <xml_file> <output_file>
extract_image_tokens() {
    local xml_file="$1"
    local output_file="$2"

    # 匹配 <img src="xxx">  中的 src 值
    grep -oP '<img[^>]*src="[^"]*"' "$xml_file" 2>/dev/null | \
        sed 's/.*src="//;s/"$//' | \
        sort -u > "$output_file"

    # 兼容 token 属性
    grep -oP '<img[^>]*token="[^"]*"' "$xml_file" 2>/dev/null | \
        sed 's/.*token="//;s/"$//' | \
        sort -u >> "$output_file"

    # 去重
    sort -u "$output_file" -o "$output_file"
}

# 下载图片（带 media-preview 回退）
# 用法: download_image <image_token> <output_file>
download_image() {
    local image_token="$1"
    local output_file="$2"
    local result

    # 先尝试 media-download
    set +e
    result=$(lark-cli docs +media-download --token "$image_token" --file "$output_file" --as "$AS_USER" 2>&1)
    local exit_code=$?
    set -e

    if [ $exit_code -eq 0 ] && [ -f "$output_file" ] && [ -s "$output_file" ]; then
        return 0
    fi

    # 回退到 media-preview
    log_warn "media-download 失败，尝试 media-preview: $image_token"
    set +e
    result=$(lark-cli docs +media-preview --token "$image_token" --file "$output_file" --as "$AS_USER" 2>&1)
    exit_code=$?
    set -e

    if [ $exit_code -eq 0 ] && [ -f "$output_file" ] && [ -s "$output_file" ]; then
        return 0
    fi

    log_error "图片下载失败: $image_token"
    return 1
}

# 上传图片到文档
# 用法: upload_image <doc_token> <image_file> <result_var>
upload_image() {
    local doc_token="$1"
    local image_file="$2"
    local out_var="$3"
    local result

    lark_cli result "docs +media-upload --doc $doc_token --file $image_file" || return 1

    # 提取上传后的图片 token
    local img_token
    img_token=$(echo "$result" | jq -r '.data.file_token // .data.token // ""')

    if [ -z "$img_token" ]; then
        log_error "图片上传后未获取到 token"
        return 1
    fi

    eval "$out_var=\$img_token"
}

# ============================================================
# 文件附件处理
# ============================================================

# 下载文件附件
# 用法: download_file_attachment <file_token> <output_file>
download_file_attachment() {
    local file_token="$1"
    local output_file="$2"
    local result

    # 尝试 media-download
    set +e
    result=$(lark-cli docs +media-download --token "$file_token" --file "$output_file" --as "$AS_USER" 2>&1)
    local exit_code=$?
    set -e

    if [ $exit_code -eq 0 ] && [ -f "$output_file" ] && [ -s "$output_file" ]; then
        return 0
    fi

    # 回退到 media-preview
    log_warn "media-download 失败，尝试 media-preview: $file_token"
    set +e
    result=$(lark-cli docs +media-preview --token "$file_token" --file "$output_file" --as "$AS_USER" 2>&1)
    exit_code=$?
    set -e

    if [ $exit_code -eq 0 ] && [ -f "$output_file" ] && [ -s "$output_file" ]; then
        return 0
    fi

    log_error "文件下载失败: $file_token"
    return 1
}

# 上传文件到 wiki 节点
# 用法: upload_file_to_wiki <wiki_token> <file_path> <result_var>
upload_file_to_wiki() {
    local wiki_token="$1"
    local file_path="$2"
    local out_var="$3"
    local result

    lark_cli result "drive +upload --file $file_path --wiki-token $wiki_token" || return 1

    local file_token
    file_token=$(echo "$result" | jq -r '.data.file_token // .data.token // ""')

    eval "$out_var=\$file_token"
}

# ============================================================
# 内部引用修复
# ============================================================

# 修复文档中的内部引用
# 用法: fix_internal_refs <xml_file>
fix_internal_refs() {
    local xml_file="$1"
    local tmp_file="${xml_file}.tmp"
    local fixed_count=0

    cp "$xml_file" "$tmp_file"

    # 1. 修复 sub-page-list 的 wiki-token
    # <sub-page-list space-id="XXX" wiki-token="YYY">
    while IFS= read -r src_token; do
        [ -z "$src_token" ] && continue
        local tgt_token
        tgt_token=$(get_mapped_wiki_token "$src_token")
        if [ -n "$tgt_token" ] && [ "$tgt_token" != "$src_token" ]; then
            sed -i "s/wiki-token=\"$src_token\"/wiki-token=\"$tgt_token\"/g" "$tmp_file"
            fixed_count=$((fixed_count + 1))
        fi
    done < <(grep -oP 'wiki-token="[^"]*"' "$tmp_file" 2>/dev/null | sed 's/wiki-token="//;s/"$//' | sort -u)

    # 2. 修复 cite 标签中的 doc-id
    # <cite type="doc" doc-id="XXX">
    while IFS= read -r src_doc_id; do
        [ -z "$src_doc_id" ] && continue
        local tgt_doc_id
        tgt_doc_id=$(get_mapped_doc_id "$src_doc_id")
        if [ -n "$tgt_doc_id" ] && [ "$tgt_doc_id" != "$src_doc_id" ]; then
            sed -i "s/doc-id=\"$src_doc_id\"/doc-id=\"$tgt_doc_id\"/g" "$tmp_file"
            fixed_count=$((fixed_count + 1))
        fi
    done < <(grep -oP 'doc-id="[^"]*"' "$tmp_file" 2>/dev/null | sed 's/doc-id="//;s/"$//' | sort -u)

    # 3. 修复 sub-page 的 doc-id
    while IFS= read -r src_doc_id; do
        [ -z "$src_doc_id" ] && continue
        local tgt_doc_id
        tgt_doc_id=$(get_mapped_doc_id "$src_doc_id")
        if [ -n "$tgt_doc_id" ] && [ "$tgt_doc_id" != "$src_doc_id" ]; then
            sed -i "s/<sub-page doc-id=\"$src_doc_id\"/<sub-page doc-id=\"$tgt_doc_id\"/g" "$tmp_file"
            fixed_count=$((fixed_count + 1))
        fi
    done < <(grep -oP '<sub-page doc-id="[^"]*"' "$tmp_file" 2>/dev/null | sed 's/<sub-page doc-id="//;s/"$//' | sort -u)

    # 4. 修复 <a href="...feishu.cn/wiki/TOKEN"> 链接
    while IFS= read -r src_token; do
        [ -z "$src_token" ] && continue
        local tgt_token
        tgt_token=$(get_mapped_wiki_token "$src_token")
        if [ -n "$tgt_token" ] && [ "$tgt_token" != "$src_token" ]; then
            # 替换各种域名下的 wiki 链接
            sed -i "s|feishu\.cn/wiki/$src_token|my.feishu.cn/wiki/$tgt_token|g" "$tmp_file"
            sed -i "s|feishu\.cn/wiki/$src_token|my.feishu.cn/wiki/$tgt_token|g" "$tmp_file"
            fixed_count=$((fixed_count + 1))
        fi
    done < <(grep -oP 'feishu\.cn/wiki/[A-Za-z0-9_-]*' "$tmp_file" 2>/dev/null | sed 's|.*/wiki/||' | sort -u)

    # 5. 修复 <a href="...feishu.cn/docx/TOKEN"> 链接
    while IFS= read -r src_doc_id; do
        [ -z "$src_doc_id" ] && continue
        local tgt_doc_id
        tgt_doc_id=$(get_mapped_doc_id "$src_doc_id")
        if [ -n "$tgt_doc_id" ] && [ "$tgt_doc_id" != "$src_doc_id" ]; then
            sed -i "s|feishu\.cn/docx/$src_doc_id|my.feishu.cn/docx/$tgt_doc_id|g" "$tmp_file"
            fixed_count=$((fixed_count + 1))
        fi
    done < <(grep -oP 'feishu\.cn/docx/[A-Za-z0-9_-]*' "$tmp_file" 2>/dev/null | sed 's|.*/docx/||' | sort -u)

    mv "$tmp_file" "$xml_file"
    echo "$fixed_count"
}

# ============================================================
# 映射表管理
# ============================================================

# 保存 wiki token 映射
save_wiki_mapping() {
    local src_token="$1"
    local tgt_token="$2"
    echo "$src_token|$tgt_token" >> "$WIKI_TOKEN_MAP"
}

# 获取映射后的 wiki token
get_mapped_wiki_token() {
    local src_token="$1"
    grep "^$src_token|" "$WIKI_TOKEN_MAP" 2>/dev/null | head -1 | cut -d'|' -f2
}

# 保存 doc id 映射
save_doc_mapping() {
    local src_id="$1"
    local tgt_id="$2"
    echo "$src_id|$tgt_id" >> "$DOC_ID_MAP"
}

# 获取映射后的 doc id
get_mapped_doc_id() {
    local src_id="$1"
    grep "^$src_id|" "$DOC_ID_MAP" 2>/dev/null | head -1 | cut -d'|' -f2
}

# 记录迁移结果
log_migration_result() {
    local src_node="$1"
    local src_title="$2"
    local src_obj_type="$3"
    local src_obj_token="$4"
    local tgt_node="$5"
    local tgt_obj_token="$6"
    local status="$7"
    local message="${8:-}"

    jq -n \
        --arg src_node "$src_node" \
        --arg title "$src_title" \
        --arg obj_type "$src_obj_type" \
        --arg src_obj_token "$src_obj_token" \
        --arg tgt_node "$tgt_node" \
        --arg tgt_obj_token "$tgt_obj_token" \
        --arg status "$status" \
        --arg message "$message" \
        '{source_node_token: $src_node, title: $title, obj_type: $obj_type, source_obj_token: $src_obj_token, target_node_token: $tgt_node, target_obj_token: $tgt_obj_token, status: $status, message: $message}' \
        >> "$MIGRATION_LOG"
}

# ============================================================
# 迁移单个文档
# ============================================================

migrate_doc() {
    local src_node_token="$1"
    local src_title="$2"
    local src_obj_token="$3"
    local tgt_parent_token="$4"
    local doc_work_dir="$5"
    local target_space="$6"

    log_info "迁移文档: $src_title"
    mkdir -p "$doc_work_dir"

    # 1. 获取文档内容
    local xml_content
    if ! get_doc_content xml_content "$src_obj_token"; then
        log_error "获取文档内容失败: $src_title"
        log_migration_result "$src_node_token" "$src_title" "docx" "$src_obj_token" "" "" "failed" "获取内容失败"
        FAILED_DOCS=$((FAILED_DOCS + 1))
        return 1
    fi

    local xml_file="$doc_work_dir/source.xml"
    echo "$xml_content" > "$xml_file"

    # 2. 提取并下载图片
    local img_tokens_file="$doc_work_dir/image_tokens.txt"
    extract_image_tokens "$xml_file" "$img_tokens_file"

    local img_count
    img_count=$(wc -l < "$img_tokens_file" | tr -d ' ')
    if [ "$img_count" -gt 0 ]; then
        log_info "  发现 $img_count 张图片，开始下载..."
        mkdir -p "$doc_work_dir/images"

        local img_idx=0
        while IFS= read -r img_token; do
            [ -z "$img_token" ] && continue
            img_idx=$((img_idx + 1))

            local img_file="$doc_work_dir/images/img_${img_idx}.bin"
            if download_image "$img_token" "$img_file"; then
                log_info "  图片 $img_idx/$img_count 下载完成"
            else
                log_warn "  图片 $img_idx/$img_count 下载失败，跳过"
            fi
        done < "$img_tokens_file"
    fi

    # 3. 在目标知识库创建 docx 节点
    local create_result
    if ! create_wiki_node create_result "$target_space" "$src_title" "docx" "$tgt_parent_token"; then
        log_error "创建目标节点失败: $src_title"
        log_migration_result "$src_node_token" "$src_title" "docx" "$src_obj_token" "" "" "failed" "创建节点失败"
        FAILED_DOCS=$((FAILED_DOCS + 1))
        mark_parent_failed "$src_node_token"
        return 1
    fi

    local tgt_node_token tgt_doc_token tgt_doc_id
    tgt_node_token=$(echo "$create_result" | jq -r '.data.node_token // ""')
    tgt_doc_token=$(echo "$create_result" | jq -r '.data.obj_token // ""')
    tgt_doc_id=$(echo "$create_result" | jq -r '.data.obj_token // ""')

    if [ -z "$tgt_node_token" ] || [ -z "$tgt_doc_token" ]; then
        log_error "创建节点后未获取到 token"
        log_migration_result "$src_node_token" "$src_title" "docx" "$src_obj_token" "" "" "failed" "节点 token 为空"
        FAILED_DOCS=$((FAILED_DOCS + 1))
        mark_parent_failed "$src_node_token"
        return 1
    fi

    log_info "  目标节点创建成功: $tgt_node_token"

    # 4. 上传图片并替换 token
    if [ "$img_count" -gt 0 ]; then
        log_info "  上传图片并替换引用..."
        local img_idx=0
        while IFS= read -r img_token; do
            [ -z "$img_token" ] && continue
            img_idx=$((img_idx + 1))

            local img_file="$doc_work_dir/images/img_${img_idx}.bin"
            if [ -f "$img_file" ] && [ -s "$img_file" ]; then
                local new_img_token
                if upload_image "$tgt_doc_token" "$img_file" new_img_token; then
                    # 替换 XML 中的图片 token
                    sed -i "s|src=\"$img_token\"|src=\"$new_img_token\"|g" "$xml_file"
                    sed -i "s|token=\"$img_token\"|token=\"$new_img_token\"|g" "$xml_file"
                    log_info "    图片 $img_idx/$img_count 上传完成"
                else
                    log_warn "    图片 $img_idx/$img_count 上传失败"
                fi
            fi
        done < "$img_tokens_file"
    fi

    # 5. 写入文档内容
    log_info "  写入文档内容..."
    local update_result
    set +e
    update_doc_content "$tgt_doc_token" "$xml_file" update_result
    local update_status=$?
    set -e

    if [ $update_status -eq 1 ]; then
        log_error "写入文档内容失败: $src_title"
        # 回滚：删除已创建的空节点
        log_warn "  回滚：删除已创建的空节点"
        lark-cli wiki +node-delete --node-token "https://my.feishu.cn/wiki/$tgt_node_token" --yes --as "$AS_USER" 2>&1 || true
        log_migration_result "$src_node_token" "$src_title" "docx" "$src_obj_token" "" "" "failed" "写入内容失败"
        FAILED_DOCS=$((FAILED_DOCS + 1))
        mark_parent_failed "$src_node_token"
        return 1
    fi

    if [ $update_status -eq 2 ]; then
        # partial_success：内容已写入，部分资源失败
        local fail_count
        fail_count=$(echo "$update_result" | jq '.data.local_resource_failures | length' 2>/dev/null || echo "?")
        log_warn "  部分成功: $src_title（$fail_count 个资源失败，文档内容已写入）"
    fi

    # 6. 保存映射
    save_wiki_mapping "$src_node_token" "$tgt_node_token"
    save_doc_mapping "$src_obj_token" "$tgt_doc_token"
    log_migration_result "$src_node_token" "$src_title" "docx" "$src_obj_token" "$tgt_node_token" "$tgt_doc_token" "success"

    SUCCESS_DOCS=$((SUCCESS_DOCS + 1))
    log_success "  文档迁移完成: $src_title"

    # 返回目标节点 token（用于子节点的父节点）
    echo "$tgt_node_token" > "$doc_work_dir/target_node_token.txt"
    return 0
}

# ============================================================
# 迁移独立 docx 文档（非 wiki 节点）
# ============================================================
# 用法: migrate_standalone_docx <docx_url> <tgt_parent_token> <target_space> <root_work_dir>
migrate_standalone_docx() {
    local docx_url="$1"
    local tgt_parent_token="$2"
    local target_space="$3"
    local root_work_dir="$4"

    log_info "迁移独立 docx: $docx_url"

    # 从 URL 提取 token
    local docx_token
    if [[ "$docx_url" =~ /docx/([A-Za-z0-9]+) ]]; then
        docx_token="${BASH_REMATCH[1]}"
    else
        log_error "无法从 URL 提取 docx token: $docx_url"
        FAILED_DOCS=$((FAILED_DOCS + 1))
        return 1
    fi

    # 1. 获取文档内容
    local xml_content
    if ! get_doc_content xml_content "$docx_token"; then
        log_error "无法读取 docx 内容: $docx_url"
        FAILED_DOCS=$((FAILED_DOCS + 1))
        return 1
    fi

    # 从 XML 提取标题（第一个 h1，没有就用 token）
    local title
    title=$(echo "$xml_content" | grep -oP '<h1[^>]*>\K.*?(?=</h1>)' 2>/dev/null | head -1 | sed 's/<[^>]*>//g')
    if [ -z "$title" ]; then
        title=$(echo "$xml_content" | grep -oP '<title[^>]*>\K.*?(?=</title>)' 2>/dev/null | head -1 | sed 's/<[^>]*>//g')
    fi
    title=$(echo "$title" | xargs echo -n 2>/dev/null || echo "$title")
    if [ -z "$title" ] || [ ${#title} -gt 100 ]; then
        title="文档_${docx_token:0:8}"
    fi

    log_info "文档标题: $title"
    log_info "文档 ID: $docx_token"

    # 准备工作目录
    local safe_title
    safe_title=$(echo "$title" | tr '/\\:*?"<>| ' '_' | cut -c1-50)
    local doc_work_dir="${root_work_dir}/${docx_token:0:8}_${safe_title}"
    mkdir -p "$doc_work_dir"

    local xml_file="$doc_work_dir/source.xml"
    echo "$xml_content" > "$xml_file"

    # 2. 提取并下载图片
    local img_tokens_file="$doc_work_dir/image_tokens.txt"
    extract_image_tokens "$xml_file" "$img_tokens_file"

    local img_count
    img_count=$(wc -l < "$img_tokens_file" | tr -d ' ')
    if [ "$img_count" -gt 0 ]; then
        log_info "  发现 $img_count 张图片，开始下载..."
        mkdir -p "$doc_work_dir/images"

        local img_idx=0
        while IFS= read -r img_token; do
            [ -z "$img_token" ] && continue
            img_idx=$((img_idx + 1))
            local img_file="$doc_work_dir/images/img_${img_idx}.bin"
            if download_image "$img_token" "$img_file"; then
                :
            else
                log_warn "  图片 $img_idx/$img_count 下载失败，跳过"
            fi
        done < "$img_tokens_file"
        log_info "  图片下载完成"
    fi

    # 3. 提取并下载文件附件（source token）
    local file_tokens_file="$doc_work_dir/file_tokens.txt"
    # 匹配 <source token="..." name="...">
    grep -oP '<source[^>]*token="[^"]*"[^>]*name="[^"]*"' "$xml_file" 2>/dev/null | \
        while IFS= read -r line; do
            local ftkn fname
            ftkn=$(echo "$line" | grep -oP 'token="[^"]*"' | sed 's/token="//;s/"$//')
            fname=$(echo "$line" | grep -oP 'name="[^"]*"' | sed 's/name="//;s/"$//')
            echo "$ftkn|$fname"
        done > "$file_tokens_file" 2>/dev/null || true

    local file_count
    file_count=$(wc -l < "$file_tokens_file" | tr -d ' ')
    if [ "$file_count" -gt 0 ]; then
        log_info "  发现 $file_count 个附件，开始下载..."
        mkdir -p "$doc_work_dir/files"

        local file_idx=0
        while IFS='|' read -r ftkn fname; do
            [ -z "$ftkn" ] && continue
            file_idx=$((file_idx + 1))
            local safe_fname
            safe_fname=$(echo "$fname" | tr '/\\:*?"<>|' '_')
            local ffile="$doc_work_dir/files/${safe_fname}"
            if download_file_attachment "$ftkn" "$ffile"; then
                # 替换 XML 中的 token 为 path
                local rel_path="./files/${safe_fname}"
                sed -i "s|token=\"$ftkn\"|path=\"@$rel_path\"|g" "$xml_file"
            else
                log_warn "  附件 $file_idx/$file_count 下载失败: $fname"
            fi
        done < "$file_tokens_file"
    fi

    # 4. 创建目标 wiki 节点
    local create_result
    if ! create_wiki_node create_result "$target_space" "$title" "docx" "$tgt_parent_token"; then
        log_error "创建目标节点失败: $title"
        FAILED_DOCS=$((FAILED_DOCS + 1))
        return 1
    fi

    local tgt_node_token tgt_doc_token
    tgt_node_token=$(echo "$create_result" | jq -r '.data.node_token // ""')
    tgt_doc_token=$(echo "$create_result" | jq -r '.data.obj_token // ""')

    if [ -z "$tgt_node_token" ] || [ -z "$tgt_doc_token" ]; then
        log_error "创建节点后未获取到 token"
        FAILED_DOCS=$((FAILED_DOCS + 1))
        return 1
    fi

    log_info "  目标节点创建成功: $tgt_node_token"

    # 5. 上传图片并替换 token
    if [ "$img_count" -gt 0 ]; then
        log_info "  上传图片并替换引用..."
        local img_idx=0
        while IFS= read -r img_token; do
            [ -z "$img_token" ] && continue
            img_idx=$((img_idx + 1))
            local img_file="$doc_work_dir/images/img_${img_idx}.bin"
            if [ -f "$img_file" ] && [ -s "$img_file" ]; then
                local new_img_token
                if upload_image "$tgt_doc_token" "$img_file" new_img_token; then
                    sed -i "s|src=\"$img_token\"|src=\"$new_img_token\"|g" "$xml_file"
                    sed -i "s|token=\"$img_token\"|token=\"$new_img_token\"|g" "$xml_file"
                fi
            fi
        done < "$img_tokens_file"
    fi

    # 6. 写入文档内容
    log_info "  写入文档内容..."
    local update_result
    local update_status=0
    set +e
    update_doc_content "$tgt_doc_token" "$xml_file" update_result
    update_status=$?
    set -e

    if [ $update_status -eq 1 ]; then
        log_error "写入文档内容失败: $title"
        log_warn "  回滚：删除已创建的空节点"
        lark-cli wiki +node-delete --node-token "https://my.feishu.cn/wiki/$tgt_node_token" --yes --as "$AS_USER" 2>&1 || true
        FAILED_DOCS=$((FAILED_DOCS + 1))
        return 1
    fi

    if [ $update_status -eq 2 ]; then
        local fail_count
        fail_count=$(echo "$update_result" | jq '.data.local_resource_failures | length' 2>/dev/null || echo "?")
        log_warn "  部分成功: $title（$fail_count 个资源失败，文档内容已写入）"
    fi

    # 7. 保存映射
    save_wiki_mapping "$docx_token" "$tgt_node_token"
    save_doc_mapping "$docx_token" "$tgt_doc_token"
    log_migration_result "$docx_token" "$title" "docx" "$docx_token" "$tgt_node_token" "$tgt_doc_token" "success" "standalone_docx"

    SUCCESS_DOCS=$((SUCCESS_DOCS + 1))
    TOTAL_DOCS=$((TOTAL_DOCS + 1))
    log_success "  迁移成功: $title"
    log_info "    Wiki: https://my.feishu.cn/wiki/$tgt_node_token"

    return 0
}

# ============================================================
# 迁移单个文件附件
# ============================================================

migrate_file() {
    local src_node_token="$1"
    local src_title="$2"
    local src_obj_token="$3"
    local tgt_parent_token="$4"
    local file_work_dir="$5"
    local target_space="$6"

    log_info "迁移文件附件: $src_title"
    mkdir -p "$file_work_dir"

    # 1. 下载源文件
    local src_file="$file_work_dir/source_$src_title"
    if ! download_file_attachment "$src_obj_token" "$src_file"; then
        log_error "文件下载失败: $src_title"
        log_migration_result "$src_node_token" "$src_title" "file" "$src_obj_token" "" "" "failed" "下载失败"
        FAILED_DOCS=$((FAILED_DOCS + 1))
        mark_parent_failed "$src_node_token"
        return 1
    fi

    local file_size
    file_size=$(wc -c < "$src_file" | tr -d ' ')
    log_info "  文件大小: $file_size 字节"

    # 2. 上传到目标 wiki 节点下
    local upload_result
    if ! upload_file_to_wiki "$tgt_parent_token" "$src_file" upload_result; then
        log_error "文件上传失败: $src_title"
        log_migration_result "$src_node_token" "$src_title" "file" "$src_obj_token" "" "" "failed" "上传失败"
        FAILED_DOCS=$((FAILED_DOCS + 1))
        mark_parent_failed "$src_node_token"
        return 1
    fi

    # 文件上传后会自动成为 wiki 子节点，但我们需要获取它的 node_token
    # 稍等一下让系统创建节点
    sleep 2

    # 3. 获取新创建的文件节点 token
    local children
    get_wiki_children children "$target_space" "$tgt_parent_token"

    local tgt_node_token=""
    local child_count
    child_count=$(echo "$children" | jq 'length')

    for ((i=0; i<child_count; i++)); do
        local child
        child=$(echo "$children" | jq -c ".[$i]")
        local c_title c_type c_node
        c_title=$(echo "$child" | jq -r '.title')
        c_type=$(echo "$child" | jq -r '.obj_type')
        c_node=$(echo "$child" | jq -r '.node_token')

        if [ "$c_title" = "$src_title" ] && [ "$c_type" = "file" ]; then
            tgt_node_token="$c_node"
            break
        fi
    done

    if [ -z "$tgt_node_token" ]; then
        log_warn "  未找到新创建的文件节点（文件已上传但可能未在子列表中立即显示）"
        tgt_node_token="unknown"
    fi

    # 4. 保存映射
    save_wiki_mapping "$src_node_token" "$tgt_node_token"
    log_migration_result "$src_node_token" "$src_title" "file" "$src_obj_token" "$tgt_node_token" "" "success"

    SUCCESS_DOCS=$((SUCCESS_DOCS + 1))
    log_success "  文件迁移完成: $src_title"

    echo "$tgt_node_token" > "$file_work_dir/target_node_token.txt"
    return 0
}

# ============================================================
# 递归迁移 wiki 树
# ============================================================

# 迁移一棵文档树
# 用法: migrate_tree <src_tree_json> <target_parent_token> <target_space_id> <work_dir>
migrate_tree() {
    local tree_json="$1"
    local tgt_parent_token="$2"
    local target_space="$3"
    local root_work_dir="$4"

    local total
    total=$(echo "$tree_json" | jq 'length')

    if [ "$total" -eq 0 ]; then
        return 0
    fi

    log_info "开始迁移文档树，共 $total 个节点"

    # 按深度分组，先迁移深度小的（父节点先创建）
    local max_depth
    max_depth=$(echo "$tree_json" | jq '[.[].depth] | max')

    for ((d=0; d<=max_depth; d++)); do
        # 获取当前深度的所有节点（保持原始顺序）
        local nodes_at_depth
        nodes_at_depth=$(echo "$tree_json" | jq -c "[.[] | select(.depth == $d)]")

        local count_at_depth
        count_at_depth=$(echo "$nodes_at_depth" | jq 'length')

        if [ "$count_at_depth" -eq 0 ]; then
            continue
        fi

        log_info "第 $d 层: $count_at_depth 个节点"

        for ((i=0; i<count_at_depth; i++)); do
            local node
            node=$(echo "$nodes_at_depth" | jq -c ".[$i]")

            local node_token title obj_type obj_token parent_tok
            node_token=$(echo "$node" | jq -r '.node_token')
            title=$(echo "$node" | jq -r '.title')
            obj_type=$(echo "$node" | jq -r '.obj_type')
            obj_token=$(echo "$node" | jq -r '.obj_token')
            parent_tok=$(echo "$node" | jq -r '.parent_token')

            # 检查源父节点是否失败（失败则跳过所有子节点）
            if [ "$d" -gt 0 ] && is_parent_failed "$parent_tok"; then
                log_warn "  父节点迁移失败，跳过子节点: $title"
                log_migration_result "$node_token" "$title" "$obj_type" "$obj_token" "" "" "skipped" "父节点迁移失败"
                SKIPPED_DOCS=$((SKIPPED_DOCS + 1))
                continue
            fi

            # 确定目标父节点
            local current_tgt_parent
            if [ "$d" -eq 0 ]; then
                current_tgt_parent="$tgt_parent_token"
            else
                current_tgt_parent=$(get_mapped_wiki_token "$parent_tok")
                if [ -z "$current_tgt_parent" ]; then
                    log_warn "未找到父节点映射: $parent_tok，跳过 $title"
                    continue
                fi
            fi

            local node_work_dir="$root_work_dir/${d}_${i}_$(echo "$title" | tr -c 'A-Za-z0-9_' '_' | cut -c1-50)"

            case "$obj_type" in
                docx)
                    migrate_doc "$node_token" "$title" "$obj_token" "$current_tgt_parent" "$node_work_dir" "$target_space" || true
                    ;;
                file)
                    migrate_file "$node_token" "$title" "$obj_token" "$current_tgt_parent" "$node_work_dir" "$target_space" || true
                    ;;
                *)
                    log_warn "  跳过不支持的类型: $obj_type ($title)"
                    log_migration_result "$node_token" "$title" "$obj_type" "$obj_token" "" "" "skipped" "不支持的类型: $obj_type"
                    SKIPPED_DOCS=$((SKIPPED_DOCS + 1))
                    ;;
            esac
        done
    done
}

# ============================================================
# 第二阶段：修复所有文档的内部引用
# ============================================================

fix_all_refs() {
    log_info "========================================"
    log_info "第二阶段：修复内部引用"
    log_info "========================================"

    local fixed_docs=0
    local total_docs=0

    # 遍历所有成功迁移的 docx 文档
    while IFS='|' read -r src_node tgt_node; do
        [ -z "$tgt_node" ] || [ "$tgt_node" = "unknown" ] && continue

        # 只处理 docx 类型（需要从 migration log 中判断）
        local obj_type
        obj_type=$(grep "\"source_node_token\":\"$src_node\"" "$MIGRATION_LOG" 2>/dev/null | \
            jq -r '.obj_type // ""' 2>/dev/null | head -1)

        if [ "$obj_type" != "docx" ]; then
            continue
        fi

        total_docs=$((total_docs + 1))
    done < "$WIKI_TOKEN_MAP"

    log_info "需要修复引用的文档: $total_docs 个"

    local current=0
    while IFS='|' read -r src_node tgt_node; do
        [ -z "$tgt_node" ] || [ "$tgt_node" = "unknown" ] && continue

        # 判断是否 docx
        local obj_type
        obj_type=$(grep "\"source_node_token\":\"$src_node\"" "$MIGRATION_LOG" 2>/dev/null | \
            jq -r '.obj_type // ""' 2>/dev/null | head -1)

        if [ "$obj_type" != "docx" ]; then
            continue
        fi

        current=$((current + 1))

        # 获取文档的 obj_token (docx token)
        local tgt_obj_token
        tgt_obj_token=$(grep "\"source_node_token\":\"$src_node\"" "$MIGRATION_LOG" 2>/dev/null | \
            jq -r '.target_obj_token // ""' 2>/dev/null | head -1)

        if [ -z "$tgt_obj_token" ]; then
            continue
        fi

        local doc_title
        doc_title=$(grep "\"source_node_token\":\"$src_node\"" "$MIGRATION_LOG" 2>/dev/null | \
            jq -r '.title // ""' 2>/dev/null | head -1)

        show_progress "$current" "$total_docs" "修复引用"
        log_info "修复引用: $doc_title"

        # 获取当前文档内容
        local xml_content xml_file
        xml_file="$WORK_DIR/_fix_refs_${current}.xml"

        if ! get_doc_content xml_content "$tgt_obj_token"; then
            log_warn "  获取文档内容失败，跳过"
            continue
        fi

        echo "$xml_content" > "$xml_file"

        # 修复引用
        local fixed_count
        fixed_count=$(fix_internal_refs "$xml_file")

        if [ "$fixed_count" -gt 0 ]; then
            log_info "  修复了 $fixed_count 处引用"
            # 更新文档
            if update_doc_content "$tgt_obj_token" "$xml_file"; then
                fixed_docs=$((fixed_docs + 1))
            else
                log_warn "  更新文档失败"
            fi
        else
            log_info "  无需修复"
        fi

        rm -f "$xml_file"
    done < "$WIKI_TOKEN_MAP"

    echo ""
    log_info "引用修复完成: $fixed_docs/$total_docs 个文档有更新"
}

# ============================================================
# 生成结果报告
# ============================================================

generate_report() {
    local report_file="$1"

    # 读取所有迁移记录
    local docs_json="[]"
    if [ -f "$MIGRATION_LOG" ]; then
        while IFS= read -r line; do
            [ -z "$line" ] && continue
            docs_json=$(echo "$docs_json" | jq --argjson d "$line" '. + [$d]')
        done < "$MIGRATION_LOG"
    fi

    # 构建 wiki token 映射
    local wiki_map_json="{}"
    if [ -f "$WIKI_TOKEN_MAP" ]; then
        while IFS='|' read -r src tgt; do
            [ -z "$src" ] && continue
            wiki_map_json=$(echo "$wiki_map_json" | jq --arg s "$src" --arg t "$tgt" '. + {($s): $t}')
        done < "$WIKI_TOKEN_MAP"
    fi

    # 构建 doc id 映射
    local doc_map_json="{}"
    if [ -f "$DOC_ID_MAP" ]; then
        while IFS='|' read -r src tgt; do
            [ -z "$src" ] && continue
            doc_map_json=$(echo "$doc_map_json" | jq --arg s "$src" --arg t "$tgt" '. + {($s): $t}')
        done < "$DOC_ID_MAP"
    fi

    jq -n \
        --argjson total $TOTAL_DOCS \
        --argjson success $SUCCESS_DOCS \
        --argjson failed $FAILED_DOCS \
        --argjson skipped $SKIPPED_DOCS \
        --argjson documents "$docs_json" \
        --argjson wiki_token_mapping "$wiki_map_json" \
        --argjson doc_id_mapping "$doc_map_json" \
        --arg timestamp "$(date '+%Y-%m-%d %H:%M:%S')" \
        '{
            timestamp: $timestamp,
            total_migrated: $success,
            total_failed: $failed,
            total_skipped: $skipped,
            total_nodes: $total,
            documents: $documents,
            wiki_token_mapping: $wiki_token_mapping,
            doc_id_mapping: $doc_id_mapping
        }' > "$report_file"

    log_info "结果报告已生成: $report_file"
}

# ============================================================
# 帮助信息
# ============================================================

show_help() {
    cat <<EOF
飞书文档迁移工具 (纯 Bash 版本)

用法: $0 [选项]

必选参数:
  -s, --source URL           源 Wiki URL（可多次指定多个源）
  或 --sources URL1,URL2     多个源 URL，用逗号分隔

目标参数 (二选一):
  -t, --target-space ID      目标知识库空间 ID（迁移到根目录）
  -p, --parent-url URL       目标父节点 Wiki URL（迁移到指定节点下）

可选参数:
  -w, --workdir PATH         临时工作目录 (默认: ./lark_migration_temp)
  -r, --retries N            最大重试次数 (默认: 3)
  --no-fix-refs              不修复内部文档引用
  --bot                      以 bot 身份调用 (默认: user)
  -h, --help                 显示帮助信息

前置依赖:
  lark-cli                   飞书命令行工具 (brew install lark-cli)
  jq                         JSON 处理工具 (brew install jq)

示例:
  # 迁移到知识库根目录
  $0 -s "https://source.feishu.cn/wiki/xxx" -t 7687020534646754274

  # 迁移到指定父节点下
  $0 -s "https://source.feishu.cn/wiki/xxx" -p "https://my.feishu.cn/wiki/yyy"

  # 批量迁移多个根文档
  $0 --sources "URL1,URL2,URL3" -t 7687020534646754274 -w ./my_migration
EOF
}

# ============================================================
# 参数解析
# ============================================================

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -s|--source)
                SOURCE_URLS+=("$2")
                shift 2
                ;;
            --sources)
                IFS=',' read -ra ADDR <<< "$2"
                for i in "${ADDR[@]}"; do
                    SOURCE_URLS+=("$i")
                done
                shift 2
                ;;
            -t|--target-space)
                TARGET_SPACE_ID="$2"
                shift 2
                ;;
            -p|--parent-url)
                TARGET_PARENT_WIKI_URL="$2"
                shift 2
                ;;
            -w|--workdir)
                WORK_DIR="$2"
                shift 2
                ;;
            -r|--retries)
                MAX_RETRIES="$2"
                shift 2
                ;;
            --no-fix-refs)
                FIX_INTERNAL_REFS=false
                shift
                ;;
            --bot)
                AS_USER="bot"
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo "❌ 未知参数: $1"
                echo ""
                show_help
                exit 1
                ;;
        esac
    done
}

# ============================================================
# 环境检查
# ============================================================

check_dependencies() {
    local missing=0

    if ! command -v lark-cli &> /dev/null; then
        echo "❌ 错误: 未找到 lark-cli"
        echo "安装方式: brew install lark-cli"
        echo ""
        missing=1
    fi

    if ! command -v jq &> /dev/null; then
        echo "❌ 错误: 未找到 jq (JSON 处理工具)"
        echo "安装方式: brew install jq"
        echo ""
        missing=1
    fi

    if [ $missing -eq 1 ]; then
        echo "请先安装缺失的依赖后重试。"
        exit 1
    fi
}

# ============================================================
# 主函数
# ============================================================

main() {
    parse_args "$@"

    # 环境检查
    check_dependencies

    # 参数校验
    if [ ${#SOURCE_URLS[@]} -eq 0 ]; then
        echo "❌ 错误: 请指定源文档 URL (-s/--source)"
        echo ""
        show_help
        exit 1
    fi

    if [ -z "$TARGET_SPACE_ID" ] && [ -z "$TARGET_PARENT_WIKI_URL" ]; then
        echo "❌ 错误: 请指定目标空间 ID (-t) 或目标父节点 URL (-p)"
        echo ""
        show_help
        exit 1
    fi

    if [ -n "$TARGET_SPACE_ID" ] && [ -n "$TARGET_PARENT_WIKI_URL" ]; then
        echo "❌ 错误: -t 和 -p 只能指定一个"
        exit 1
    fi

    # 创建工作目录
    mkdir -p "$WORK_DIR"
    WORK_DIR="$(cd "$WORK_DIR" && pwd)"

    local timestamp
    timestamp=$(date '+%Y%m%d_%H%M%S')
    LOG_FILE="$WORK_DIR/migration_${timestamp}.log"
    RESULT_FILE="$WORK_DIR/migration_results_${timestamp}.json"
    WIKI_TOKEN_MAP="$WORK_DIR/wiki_token_map_${timestamp}.txt"
    DOC_ID_MAP="$WORK_DIR/doc_id_map_${timestamp}.txt"
    MIGRATION_LOG="$WORK_DIR/migration_log_${timestamp}.jsonl"
    FAILED_PARENTS_FILE="$WORK_DIR/failed_parents_${timestamp}.txt"

    touch "$LOG_FILE" "$WIKI_TOKEN_MAP" "$DOC_ID_MAP" "$MIGRATION_LOG" "$FAILED_PARENTS_FILE"

    # 输出启动信息
    echo ""
    echo "========================================"
    echo "  飞书文档迁移工具 (纯 Bash 版)"
    echo "========================================"
    echo ""
    echo "源文档数量: ${#SOURCE_URLS[@]}"
    for src in "${SOURCE_URLS[@]}"; do
        echo "  - $src"
    done
    echo ""
    if [ -n "$TARGET_SPACE_ID" ]; then
        echo "目标: 知识库根目录 (space-id: $TARGET_SPACE_ID)"
    fi
    if [ -n "$TARGET_PARENT_WIKI_URL" ]; then
        echo "目标: 父节点下 ($TARGET_PARENT_WIKI_URL)"
    fi
    echo "工作目录: $WORK_DIR"
    echo "重试次数: $MAX_RETRIES"
    echo "身份: $AS_USER"
    echo "修复引用: $FIX_INTERNAL_REFS"
    echo ""
    echo "========================================"
    echo ""

    # 如果指定了父节点 URL，解析出 space-id 和 node token
    local target_parent_token=""
    local target_space=""

    if [ -n "$TARGET_PARENT_WIKI_URL" ]; then
        log_info "解析目标父节点信息..."
        local parent_token
        parent_token=$(extract_wiki_token "$TARGET_PARENT_WIKI_URL")

        if [ -z "$parent_token" ]; then
            log_error "无法从 URL 提取 wiki token: $TARGET_PARENT_WIKI_URL"
            exit 1
        fi

        # 获取父节点信息以得到 space-id
        local parent_info
        if ! get_wiki_node_info parent_info "$parent_token"; then
            log_error "获取目标父节点信息失败"
            exit 1
        fi

        target_space=$(echo "$parent_info" | jq -r '.data.space_id // ""')
        target_parent_token="$parent_token"

        if [ -z "$target_space" ]; then
            log_error "无法获取目标知识库 space-id"
            exit 1
        fi

        log_info "目标知识库: $target_space"
        log_info "目标父节点: $target_parent_token"
    else
        target_space="$TARGET_SPACE_ID"
        target_parent_token=""
        log_info "目标知识库: $target_space (根目录)"
    fi

    # 第一阶段：迁移每个源文档
    local idx=0
    for src_url in "${SOURCE_URLS[@]}"; do
        idx=$((idx + 1))
        log_info "========================================"
        log_info "处理源文档 $idx/${#SOURCE_URLS[@]}: $src_url"
        log_info "========================================"

        # 判断 URL 类型
        local is_docx=false
        if [[ "$src_url" =~ /docx/ ]]; then
            is_docx=true
        fi

        # 独立 docx 文档：走独立迁移路径
        if [ "$is_docx" = true ]; then
            local docx_work_dir="$WORK_DIR/docx_${idx}"
            mkdir -p "$docx_work_dir"
            migrate_standalone_docx "$src_url" "$target_parent_token" "$target_space" "$docx_work_dir" || true
            continue
        fi

        # Wiki 文档：走原有的递归迁移路径
        # 提取源 wiki token
        local src_token
        src_token=$(extract_wiki_token "$src_url")
        if [ -z "$src_token" ]; then
            log_error "无法从 URL 提取 wiki token: $src_url"
            FAILED_DOCS=$((FAILED_DOCS + 1))
            continue
        fi

        # 获取源节点信息（space-id, title）
        local src_node_info
        if ! get_wiki_node_info src_node_info "$src_token"; then
            log_error "获取源节点信息失败，跳过"
            FAILED_DOCS=$((FAILED_DOCS + 1))
            continue
        fi

        local src_space src_title src_obj_type src_obj_token
        src_space=$(echo "$src_node_info" | jq -r '.data.space_id // ""')
        src_title=$(echo "$src_node_info" | jq -r '.data.title // ""')
        src_obj_type=$(echo "$src_node_info" | jq -r '.data.obj_type // ""')
        src_obj_token=$(echo "$src_node_info" | jq -r '.data.obj_token // ""')

        log_info "源文档: $src_title (type: $src_obj_type)"

        # 扫描整个文档树
        log_info "扫描文档树..."
        local tree_json
        if ! get_wiki_tree tree_json "$src_space" "$src_token" 0; then
            log_error "扫描文档树失败"
            FAILED_DOCS=$((FAILED_DOCS + 1))
            continue
        fi

        # 加上根节点自身
        local root_node
        root_node=$(jq -n \
            --arg token "$src_token" \
            --arg title "$src_title" \
            --arg obj_type "$src_obj_type" \
            --arg obj_token "$src_obj_token" \
            --arg parent "" \
            --argjson depth -1 \
            '{node_token: $token, title: $title, obj_type: $obj_type, obj_token: $obj_token, parent_token: $parent, depth: $depth}')

        tree_json=$(echo "[$root_node] $tree_json" | jq -s '.[0] + .[1]')

        # 调整深度：根节点 depth 0，子节点 depth 1，以此类推
        tree_json=$(echo "$tree_json" | jq '[.[] | .depth = (.depth + 1)]')

        local tree_total
        tree_total=$(echo "$tree_json" | jq 'length')
        TOTAL_DOCS=$((TOTAL_DOCS + tree_total))

        log_info "文档树共 $tree_total 个节点"

        # 迁移这棵树
        local tree_work_dir="$WORK_DIR/tree_${idx}"
        mkdir -p "$tree_work_dir"

        migrate_tree "$tree_json" "$target_parent_token" "$target_space" "$tree_work_dir"
    done

    # 第二阶段：修复内部引用
    if [ "$FIX_INTERNAL_REFS" = true ]; then
        fix_all_refs
    fi

    # 生成结果报告
    generate_report "$RESULT_FILE"

    # 输出总结
    echo ""
    echo "========================================"
    echo "  迁移完成"
    echo "========================================"
    echo ""
    echo "总计: $TOTAL_DOCS 个节点"
    echo -e "${GREEN}成功: $SUCCESS_DOCS${NC}"
    if [ $FAILED_DOCS -gt 0 ]; then
        echo -e "${RED}失败: $FAILED_DOCS${NC}"
    fi
    if [ $SKIPPED_DOCS -gt 0 ]; then
        echo -e "${YELLOW}跳过: $SKIPPED_DOCS${NC}"
    fi
    echo ""
    echo "日志文件: $LOG_FILE"
    echo "结果报告: $RESULT_FILE"
    echo ""

    if [ $FAILED_DOCS -gt 0 ]; then
        exit 1
    fi
}

# 运行主函数
main "$@"
