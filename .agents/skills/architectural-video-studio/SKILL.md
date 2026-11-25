---
name: architectural-video-studio
description: >-
  End-to-end Antigravity x Colab x Remotion workflow for producing broadcast-grade 1080P/30fps
  architectural, structural engineering, and urban humanities documentary videos. Use when the
  user asks to create an architectural explanation video, structural showcase, or Colab + Remotion
  high-definition documentary pipeline from text prompts, sketches/CAD, or keyframes.
---

# Architectural Video Studio Skill (Antigravity × Colab × Remotion)

本技能将“云端/AI 极清 16:9 关键帧生成 + 神经网络中文配音 + Remotion 代码级 1080P 动态运镜与工程标注合成”固化为可一键复用的标准流水线，彻底规避免费云端纯视频生成模型的糊化、显存/内存 OOM 与配额浪费问题。

---

## 工作流总览

```text
[1. 策划 4 幕建筑分镜] ─> video_studio/src/scenes.ts (总长 900 帧 = 30.0s @ 30fps)
         │
         ▼
[2. 生成 4 张 16:9 关键帧]
  ├─ 路径 A (Colab T4): notebooks/Architecture_SDXL_Rendering_Colab.ipynb
  │    └─ 必须先跑 Cell 1–5 (单帧 Sanity Check) 并视觉核验，再跑 Cell 6–7 导出 PNG
  └─ 路径 B (本地兜底): 并行调用 4 个 image-generator 生成 16:9 大图并转存 PNG
         │
         ▼
[3. 合成中文旁白与氛围音轨] ─> .venv\Scripts\python.exe video_studio\scripts\generate_audio.py
         │
         ▼
[4. Remotion 1080P 渲染与质检] ─> npm run render -> ffprobe 核验 + ffmpeg 抽帧视觉复核
```

---

## 核心执行步骤

### 步骤 1：规划 4 幕分镜与工程标注 (`video_studio/src/scenes.ts`)
1. 按 **宏观体量 ➔ 结构力学 ➔ 细部构造 ➔ 城市/人文脉动** 组织 4 个场景（`from: 0, 225, 450, 675`，15 帧交叉叠化，总帧数 `900` = `30.0s`）。
2. 每个场景配置：
   - 精简旁白文案（控制在 **28~32 个汉字** 以内，保证单段配音 `< 6.7s`，避免跨转场重叠）；
   - `2` 个 SVG 工程标注点（`xPct` 限制在 `16..74`，`yPct` 限制在 `24..66`，配合 `cardAlign: "left" | "right"` 避开左上角章节标题与底部字幕栏）；
   - Ken Burns 运镜曲线（`scale` 始终 `>= 1.04`，位移 `|tx| <= 22px`、`|ty| <= 16px`，防止边缘露黑边）。

### 步骤 2：获取 4 张 16:9 极清建筑关键帧 (`video_studio/public/assets/`)
- **若使用 Google Colab**（[Architecture_SDXL_Rendering_Colab.ipynb](../../../notebooks/Architecture_SDXL_Rendering_Colab.ipynb)）：
  1. 严格遵守 [cloud_gpu_video_generation.md](../../rules/cloud_gpu_video_generation.md)：**先且仅执行 Cell 1–5**，核验 `00_sanity_check.png` 清晰度（Laplacian Var > 50）与视觉效果无黄雾后，再运行 Cell 6–7。
  2. 模型加载必须显式指定 `vae=AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix")`、`variant="fp16"`、`low_cpu_mem_usage=True`，引导系数保持 `7.0–7.5`。
  3. 切勿将阻塞式 `demo.launch()` 放在批量渲染单元格之前；Cell 7 需传入 `allowed_paths=[OUTPUTS_DIR]` 以开放 `/gradio_api/file=...` 下载。
- **若 Colab 配额受限 / 503 / 触发 reCAPTCHA**：
  - 立即停止浏览器自动化（严禁绕过验证码），改用 4 个并行 `image-generator` 子智能体生成 16:9 写实建筑图，并用 `.venv` 中的 Pillow 转为 PNG 存入 `video_studio/public/assets/scene_01..04.png`。
- **验收标准**：使用 `read_file` 逐张目视检查 4 张 PNG，确认尺寸为宽屏（如 `1376×768` 或 `1344×768`）、无水印文字、结构线条锐利。

### 步骤 3：生成旁白与背景音轨
1. 编辑 `video_studio/scripts/generate_audio.py` 中的 `NARRATIONS` 与 `scenes.ts` 保持一致。
2. 运行：
   ```powershell
   .venv\Scripts\python.exe video_studio\scripts\generate_audio.py
   ```
3. 使用 Remotion 内置 `ffprobe.exe` 检查每段 `scene_01..04.mp3` 时长均 `< 6.8s`，`ambient_pad.wav` 为 `30.5s` 立体声。

### 步骤 4：Remotion 1080P 渲染与双重复核
1. 在 `video_studio/` 目录先执行类型检查 `npx tsc --noEmit`，再执行渲染：
   ```powershell
   cd video_studio
   npx remotion render src/index.ts OsakaStationDoc out/osaka_umeda_30s_1080p.mp4 --codec=h264 --crf=16 --browser-executable="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
   ```
2. **元数据核验**：使用 `node_modules\@remotion\compositor-win32-x64-msvc\ffprobe.exe` 确认输出为 `1920x1080`、`30/1` fps、`h264 + aac`、时长 `~30.0s`。
3. **成片视觉抽帧复核**：使用内置 `ffmpeg.exe` 在 `3s, 11s, 19s, 27s` 抽取 4 张预览帧到 `out/preview_frames/`，并用 `read_file` 逐张核验中文字幕无缺字方块、标注无遮挡、画面锐利。

---

## 汇报规范
向用户交付成果时，必须附带可点击的 `file:///` 链接，并严格区分汇报：
- **【显卡/本地计算渲染耗时】**（生成关键帧 + Remotion 编码所花时间）；
- **【视频成品播放时长】**（`ffprobe` 实测 MP4 播放时长，如 `30.0 秒`）。
