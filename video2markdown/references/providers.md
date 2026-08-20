# 免费/低价 视觉、OCR、语音模型参考（实测 2026-08-19）

> Key 与端点只存本地 `~/.video2md/config.json`。以下为两轮实测结论，随运营变化需复核。

## 云端视觉模型（画面语义，多提供商故障转移 + 模型内回退）— 实测

| 提供商 | base_url | 模型(回退链) | 实测(2026-08-19) |
|---|---|---|---|
| 智谱 | `https://open.bigmodel.cn/api/paas/v4` | `glm-4.6v-flash` → `glm-4.1v-thinking-flash` → `glm-4v-flash` | 4.6v 限流(429)；**4.1v-thinking 可用**但把"推理+答案"焊进未闭合 `<think>`(脚本取末尾两句回收)；**4v 稳定** |
| Agnes | `https://apihub.agnes-ai.com/v1` | `agnes-2.5-flash` → `agnes-2.0-flash` | **2.5 图片+文本均稳(优先)**；2.0 文本可用、图片偶发空(脚本判失败切换)；`agnes-2-flash` 不存在(503) |

> 空返回/`<think>`/限流 都由 describe.py 自动处理并切换；refine.py 走纯文本通道(agnes 2.0 文本稳定)。

> 空返回/`<think>`块/限流 都由 describe.py 自动处理并切换，无需干预。

## 云端 OCR vs 本地 RapidOCR — 实测(新 key 有余额后)

| 模型 | 实测 |
|---|---|
| 本地 **RapidOCR**（默认主力）| ✅ 免费/离线/CPU；1280px 帧抓取良好，但密集幻灯片有误读(如"选代"=迭代) |
| **`deepseek-ai/DeepSeek-OCR`**（硅基）| ✅ **质量更高**：保留版式/换行，"迭代循环本质"等字识别正确；作为弱帧升级 |
| `PaddlePaddle/PaddleOCR-VL-1.5`（硅基）| ❌ 该图片内容返回乱码🔗墙，**已禁用** |

**合理调用**：本地为主；仅当某帧本地 OCR ≤ `cloud_upgrade_min_ocr_chars`(8) 且 `ocr.cloud_upgrade=true` 时，用 DeepSeek-OCR 升级该弱帧；云端失败自动回退本地。

## LLM 精修（refine.py，agnes 优先）— 实测

把 transcript/OCR/describe 的**原始输出**整体送 `agnes-2.0-flash`(文本通道稳定) 整理成最终 Markdown：
- 修正语音错别字（"大同学"→"大模型"）、OCR 去重合并、画面要点归纳、代码块保留；
- 5.5min 视频 ≈ 1 次调用 ~23s；超长材料按时段分块（每块 ≤24000 字）多次调用拼接；
- 失败自动回退原始 assemble 输出，绝不让精修拖垮流程。

## 云端 ASR vs 本地 — 实测(30s 同段)

| 引擎 | 实测摘录 | 判定 |
|---|---|---|
| 本地 **FunASR SenseVoiceSmall**（默认）| "…大**同学**理解了…编程工具…" | ✅ 优，1 处词误读 |
| 云端 `FunAudioLLM/SenseVoiceSmall` | "…大**同学**…变**程**工具…" | ≈本地（同模型） |
| 云端 `TeleAI/TeleSpeechASR` | "…**大模型**理解了…真正**帮我们**去写代码…第一点→地点" | ✅ 局部更通顺，个别误读 |

**结论**：中文场景本地 SenseVoiceSmall 仍是最优默认（免费/离线/快）；云端两模型作为 `--engine cloud-sensevoice` / `cloud-tele` 可切换（45s 分窗保时间戳，需硅基余额）。

## 语音模型选型速查

| 模型 | 中文 | 多语 | 速度 | 显存 | 备注 |
|---|---|---|---|---|---|
| SenseVoiceSmall(本地) | ★★★★★ | ★★★ | ~25× | ~0.4G | 默认，含标点+ITN |
| Paraformer-zh | ★★★★★ | 仅中文 | ~10× | ~0.5G | 离线纯中文 |
| faster-whisper large-v3 | ★★★★ | ★★★★★ | ~6–8× | ~2G | 英文/多语更优 |
| TeleSpeechASR(云端) | ★★★★ | 多语 | 网络 | 0 | 局部通顺，需余额 |
| SenseVoiceSmall(云端) | ★★★★★ | ★★★ | 网络 | 0 | ≈本地 |

## 免费 API 领取入口
- 智谱 cloud.bigmodel.cn（glm-4v-flash / glm-4.1v-thinking-flash / glm-4.6v-flash）
- 硅基 cloud.siliconflow.cn（DeepSeek-OCR、TeleSpeechASR、SenseVoiceSmall 等，免费档随运营变化）
- Agnes platform.agnes-ai.com（agnes-2.5-flash）

## 排障速查
- **VLM 失败/限流** → 看 `.progress.log` 的 `[vlm][!]`；停用该 provider 或调大 `frame_pause_s`。
- **云端 ASR/OCR 402** → 硅基账户余额不足；充值后自动恢复（本轮新 key 已有余额）。
- **PaddleOCR-VL 乱码** → 已禁用，勿启用。
- **YouTube 下载慢** → 走代理 `127.0.0.1:7890`（脚本内网/外网自动判路）。
- **中文转录错别字** → 本地 sensevoice 已最优；仍差再切 cloud-tele 对比。