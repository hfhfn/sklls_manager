# 抖音在线视频下载的 cookies 绕过方案

> ⚡ **现已自动化**：`scripts/douyin_download.py` + `video2md.py` 的抖音自动兜底已经把这套方法封成命令。
> 直接 `python video2md.py "https://v.douyin.com/xxxx/"` 即可，yt-dlp 被拦时会自动走 CDN 直链，
> 无需手动开浏览器抓 URL。依赖 `pip install playwright`。本文保留作为「原理 + 手动应急步骤」，供无命令/无 Playwright 的环境或排障参考。

## 背景
yt-dlp 直连 `https://www.douyin.com/video/<modal_id>` 常报：
```
ERROR: [Douyin] <id>: Fresh cookies (not necessarily logged in) are needed; please report...
```
原因是抖音 web 端对该详情接口的 cookie 签名（`__ac_signature` / `a_bogus` / `x-secsdk-web-signature`）校验严苛。
即使手写一批 `__ac_signature` 等 cookie 也常被判定过期。

## 可靠方案：浏览器内抓 CDN 直链（无需 cookies 通行）

步骤：
1. 用浏览器打开 `https://www.douyin.com/video/<modal_id>`（无需登录，页面能加载视频本体）。
2. 在浏览器控制台执行，抓取真实播放地址（video 轨 + audio 轨）：
   ```js
   var res = performance.getEntriesByType('resource').map(function(e){return e.name})
              .filter(function(n){return n.indexOf('douyinvod.com')>-1});
   JSON.stringify(res)
   ```
   会得到若干条 `https://v26-web.douyinvod.com/..../media-video-avc1/?...`（视频轨）和
   `..../media-audio-und-mp4a/?...`（音频轨）。
3. 保存各 URL 到独立文本文件（注意 URL 内带 `&` 和 `%3D`，务必整串引用，用 `$(cat file)`）。
4. 用 curl 直连下载（抖音国内 CDN 不走代理，但需带 Referer 防 302 防盗链）：
   ```bash
   curl -m 300 -s -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/151.0.0.0" \
        -e "https://www.douyin.com/" -o video_raw.mp4 "$(cat video_url.txt)"
   curl -m 300 -s -L -A "iOS/Android 同 UA" -e "https://www.douyin.com/" -o audio_raw.m4a "$(cat audio_url.txt)"
   ```
5. ffmpeg 合并：
   ```bash
   ffmpeg -y -i video_raw.mp4 -i audio_raw.m4a -c copy -movflags +faststart final.mp4
   ```

### 验证
- curl 下载后 `file final` 应显示 `ISO Media, MP4 Base Media`；ffprobe 时长应>0。
- 视频轨 filesize 一般 >10MB，音频轨几 MB。若某条 URL 404，可能是临时的，刷新页面重抓。

## 其他提示
- 页面标题可用 `document.title` 取（含话题标签）。
- 分享口令形式 `https://v.douyin.com/xxxx/` 先经浏览器展开为 `modal_id`，或直接浏览器打开后从地址栏拿 `www.douyin.com/video/<id>`。

## 何时用
- 当 yt-dlp 报 cookies 错，或想要比 yt-dlp 更可靠的第 2 条路径时。
- 全程可离线在浏览器完成，无 cookie 依赖。

## 实测端到端流程（2026-08 已验证，含清理）

完整跑通的一套命令（git-bash，`vid_work` 为工作目录）。**抖音国内 CDN 全程直连**，
先 `unset HTTPS_PROXY HTTP_PROXY ALL_PROXY https_proxy http_proxy all_proxy`。

```bash
# 1) 短链 → video id（curl 直连展开，不走代理）
curl -sL -A "Mozilla/5.0" "https://v.douyin.com/xxxx/" -o /dev/null -w "%{url_effective}"
#    → https://www.douyin.com/video/<modal_id>?previous_page=app_code_link

# 2) 浏览器打开 https://www.douyin.com/video/<modal_id>（无需登录）
#    控制台抓 CDN 直链：
#    performance.getEntriesByType('resource').map(e=>e.name).filter(n=>n.includes('douyinvod.com'))
#    取 media-video-avc1/...（视频轨）+ media-audio-und-mp4a/...（音频轨）两条 URL。
#    URL 含 & 和 %3D，整串存文件，别手动复制变形。

# 3) curl 直连下载两轨（带 Referer 防 302 防盗链，不走代理）
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/151.0.0.0"
curl -m 300 -s -L -A "$UA" -e "https://www.douyin.com/" -o video_raw.mp4 "$(cat video_url.txt)"
curl -m 300 -s -L -A "$UA" -e "https://www.douyin.com/" -o audio_raw.m4a "$(cat audio_url.txt)"

# 4) 合并
ffmpeg -y -i video_raw.mp4 -i audio_raw.m4a -c copy -movflags +faststart final.mp4

# 5) 转录本地 final.mp4（用 llm_gpu 全路径 python，勿 activate）
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV
/d/software/miniconda3/envs/llm_gpu/python.exe C:/Users/hfhfn/.claude/skills/video2markdown/scripts/video2md.py "C:/.../final.mp4"

# 6) 清理中间产物（成品仅留 .md / .mp4 / .jpg）
rm -f video_raw.mp4 audio_raw.m4a video_url.txt audio_url.txt
rm -rf video              # 历次转录的内部工作目录（含 .vid_* 关键帧/wav/jsonl）

# 7) 验证
file final.mp4 && ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 final.mp4
```

> 本次视频时长约 6 分 51 秒：ASR 144 段 + OCR 42 帧 + VLM 41 帧，整条约 6 分钟。
> 结束时的 `FileNotFoundError: .vid_*/.progress.log`（退出码 1）是无害的清理日志 bug，
> md 产物完整，忽略。