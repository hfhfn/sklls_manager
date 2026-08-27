# 抖音在线视频下载的 cookies 绕过方案

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