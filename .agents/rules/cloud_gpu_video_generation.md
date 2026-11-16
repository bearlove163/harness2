---
name: cloud-gpu-video-generation
description: "Universal guardrails for Cloud GPU quota management and AI video generation workflows"
trigger: always_on
---

# 云端 GPU 算力配额管理与 AI 视频生成行为准则

在执行 Google Colab、Kaggle、AutoDL 等有限算力平台上的 AI 视频生成或大模型任务时，必须严格遵守以下红线准则：

## 1. 严格执行“首片/单帧快速抽检 (Sanity Check)”，禁止盲目批量渲染
- 在进行多镜头、长片或批处理渲染前，**必须且只能先执行极小规模试跑**（如：单镜头、15-20步、测试帧/单帧抽检）。
- 必须通过检查输出文件像素、直方图或让用户确认样张有效后，**严禁在未经质检的前提下直接执行长达数十分钟的全量多镜头流水线**。

## 2. 模型核心组件完整性校验（防解码失效）
- 在挂载任何 Stable Diffusion / AnimateDiff / Flux 衍生模型时，必须核验 VAE、Text Encoder、Scheduler 的完整性。
- 若底模带有 `_noVAE`，必须强制显式挂载官方推荐的专用 VAE（如 `stabilityai/sd-vae-ft-mse`），杜绝因无 VAE 产生的大黄雾、大光斑和色偏废片。
- AnimateDiff 引导系数（Guidance Scale）严禁超调（保持在 7.0-7.5 区间），防止潜空间烧焦 (Latent Burn)。

## 3. 严格区分计算指标，严禁误导用户
- 在所有报告中，必须严格区分并明确标注：
  - **【显卡计算渲染耗时】**（GPU 计算所需时间，如：40秒、5分钟）；
  - **【视频成品播放时长】**（导出的 MP4 文件实际播放时长，如：2秒、10秒）。
  - 严禁使用模糊的“耗时40秒”指代视频内容时长。

## 4. 云端免费/计量配额透明度与风险预警
- 对于 Colab 等免费 GPU 配额，必须建立强烈的“算力预算意识”：
  - 单次任务预计耗时若超过 10 分钟，必须在执行前向用户主动预警预计 GPU 消耗量；
  - 严禁在未确认前序成果质量的情况下连续消耗配额。
