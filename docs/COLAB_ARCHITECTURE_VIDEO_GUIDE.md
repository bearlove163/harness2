# 🏛️ Google Colab 建筑结构与人文历史视频生成流水线实战指南

> **基于 Wan2.1 (万象) 模型与跨 Agent 资产接力架构**  
> 专为建筑空间漫游、空间结构力学、构造节点细部与建筑人文历史演进打造。

---

## 目录
1. [一键启动与环境准备](#1-一键启动与环境准备)
2. [跨 Agent 资产接力工作流 (核心)](#2-跨-agent-资产接力工作流-核心)
3. [四大建筑专业镜头与提示词实战](#3-四大建筑专业镜头与提示词实战)
4. [Gradio 可视化工作台使用指引](#4-gradio-可视化工作台使用指引)
5. [免费版 T4 显存调优与防 OOM 指南](#5-免费版-t4-显存调优与防-oom-指南)
6. [成果归档与下游剪辑对接](#6-成果归档与下游剪辑对接)

---

## 1. 一键启动与环境准备

### 步骤 1：在 Google Colab 中打开 Notebook
- **方式 A (直接点击徽章)**：  
  在 GitHub 仓库主页或点击下方徽章：  
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bearlove163/harness2/blob/colab_video_generation/notebooks/Wan2_1_Architecture_Video_Colab.ipynb)
- **方式 B (手动上传)**：  
  打开 [Google Colab](https://colab.research.google.com/) -> 选择 `Upload` (上传) -> 选择本项目中的 `notebooks/Wan2_1_Architecture_Video_Colab.ipynb` 文件。

### 步骤 2：切换为 GPU 硬件加速
1. 点击 Colab 顶部菜单栏：`代码执行程序 (Runtime)` -> `更改运行时类型 (Change runtime type)`。
2. 硬件加速器选择：
   - **免费用户**：选择 **T4 GPU**。
   - **Colab Pro/Pro+ 用户**：选择 **A100 GPU** 或 **L4 GPU**。
3. 点击 **保存 (Save)**。

---

## 2. 跨 Agent 资产接力工作流 (核心)

本流水线专为**“上游 Agent 创作模型/图纸 -> Colab 批量生成动态素材 -> 下游视频剪辑/研报发布”**的接力设计：

```
[上游 3D/渲染/文献 Agent]
   │ (产出渲染效果图、BIM 剖面图、历史黑白测绘照片)
   ▼
[Google Drive: /MyDrive/Colab_Video_Relay/inputs/]
   │
   ▼
[Colab Wan2.1 引擎: 自动扫描 + 智能匹配运镜 + 显存切片渲染]
   │
   ▼
[Google Drive: /MyDrive/Colab_Video_Relay/outputs/]
   │ 包含：
   │ ├── *_wan21.mp4  (高清影视级动态镜头)
   │ └── *_wan21.json (镜头元数据：Prompt, Seed, 镜头运镜)
   ▼
[下游剪辑 Agent / 视频合成软件]
```

### 资产接力三步法：
1. **上游写入**：其他 Agent 完成绘图或建模渲染后，将静态图（`.png`, `.jpg`, `.webp`）保存至云端硬盘的：
   ```
   /content/drive/MyDrive/Colab_Video_Relay/inputs/
   ```
2. **执行接力单元格**：在 Notebook 中运行 **第 5 单元格【资产接力：批量图生视频】**。
3. **自动输出**：脚本将自动把图片缩放至模型支持的 16 倍数尺寸，匹配建筑与工程运镜提示词，完成渲染并连同 JSON 元数据存入 `outputs/`。

---

## 3. 四大建筑专业镜头与提示词实战

我们内置了经过严密调优的影视级提示词模版库（位于 `configs/architectural_video_prompts.json`）：

### ① 建筑形态与空间体量 (Massing & Exterior)
- **流线型展馆全景环绕 (Drone Orbit)**：
  - *适用场景*：现代扎哈/马岩松风格大空间展馆、曲面屋顶。
  - *镜头语言*：平滑 360 度低空环绕航拍，展现日光反射与水面倒影。
- **巨型中庭天光垂直拉升 (Vertical Pedestal)**：
  - *适用场景*：博物馆、交通枢纽大厅、多层通高挑空。
  - *镜头语言*：垂直升降起吊镜头，丁达尔丁达尔光束洒落，空间层次丰富。

### ② 结构体系与力学之美 (Structural Systems)
- **大跨度空间管桁架轴测动态拼装 (Space Truss)**：
  - *适用场景*：体育场馆网架、马鞍形曲面屋盖、机场航站楼。
  - *镜头语言*：轴测爆炸图，构件由天而降自动精准插接咬合，带有微光应力流线。
- **斜拉张弦体系受力与风动响应 (Tension Cables)**：
  - *适用场景*：悬索桥、大跨度张弦梁、桅杆拉索。
  - *镜头语言*：微距与中景结合，索夹阻尼器微幅呼吸动态，金属冷峻光泽。
- **中国古建斗栱榫卯旋转咬合 (Dougong)**：
  - *适用场景*：应县木塔、佛光寺东大殿、重翘双昂大木作。
  - *镜头语言*：老杉木纹理环绕旋转，栌斗与华栱层层严丝合缝拼装。

### ③ 细部构造与节点大样 (Tectonic Details)
- **点支承玻璃幕墙驳接爪微距特写 (Spider Fitting)**：
  - *适用场景*：玻璃幕墙大样、不锈钢驳接爪、防震万向球铰。
  - *镜头语言*：微距滑轨缓慢推近，展现 CNC 车削拉丝质感、紧固螺栓与光斑折射。
- **清水混凝土明缝与对拉螺栓孔 (Fair-faced Concrete)**：
  - *适用场景*：安藤忠雄风格、现代极简主义立面。
  - *镜头语言*：水平横向移轨，午后斜阳在丝绸质感墙面投下诗意几何阴影。

### ④ 建筑人文历史与时空演化 (Humanities & History)
- **历史黑白老照片动态彩色复活 (Vintage Archival Motion)**：
  - *适用场景*：近代历史保护建筑、老街道测绘图、民国黑白照片。
  - *镜头语言*：老照片黑白质感逐渐唤醒为暖色日光，行人与老电车开始自然行走穿梭。
- **古建筑遗存晨昏日月与星轨延时 (Heritage Timelapse)**：
  - *适用场景*：石窟遗址、古城墙、长城烽燧。
  - *镜头语言*：固定机位 4K 延时，日月如梭日影飞旋，银河星轨划过飞檐。
- **历史残垣断壁逆向时光复原 (Ruin Reverse Reconstruction)**：
  - *适用场景*：圆明园、罗马斗兽场、大雁塔修缮前对比。
  - *镜头语言*：时光倒流特效，散落石块升起归位，梁架重新搭建，金碧辉煌重现。

---

## 4. Gradio 可视化工作台使用指引

在 Notebook 中运行 **第 6 单元格**，将自动启动 Gradio 服务并输出两个访问链接：
1. **本地内嵌视图**：直接在 Colab 页面内操作。
2. **Public URL (公网链接 `https://xxxx.gradio.live`)**：
   - 可在任意电脑浏览器或手机端打开。
   - 界面包含**提示词下拉预设**、**反向提示词**、**步数 (默认30)**、**画幅选择 (16:9 / 9:16)** 与 **即时播放下载** 功能。

---

## 5. 免费版 T4 显存调优与防 OOM 指南

Google Colab 免费版分配的 Tesla T4 显存约为 15GB，运行百亿参数视频模型极易显存溢出 (CUDA Out of Memory)。我们在流水线中做了以下专属优化：

1. **自动启用 CPU Offload (`enable_model_cpu_offload`)**：
   - 文本编码器与 VAE 在不参与当前去噪计算时自动移出显存，显存峰值降低 40% 以上。
2. **VAE 切片与平铺 (`vae.enable_slicing()` & `vae.enable_tiling()`)**：
   - 避免在高清视频逐帧解码时发生突发显存爆炸。
3. **分辨率控制**：
   - 推荐横屏采用 `832 x 480` 或 `768 x 432`；竖屏采用 `480 x 832`。此分辨率兼顾极高的细节清晰度与毫秒级解码安全。

---

## 6. 成果归档与下游剪辑对接

所有渲染生成的素材均带有结构化命名与 JSON 记录：
```
/content/drive/MyDrive/Colab_Video_Relay/outputs/
  ├── pavilion_01_wan21.mp4
  ├── pavilion_01_wan21.json
  ├── dougong_02_wan21.mp4
  └── dougong_02_wan21.json
```
- **一键打包**：运行第 7 单元格即可生成 `architectural_videos_package.zip`。
- **下游剪辑**：可以直接导入剪映 (CapCut)、Adobe Premiere 或 DaVinci Resolve，结合元数据中的提示词进行解说音画配对。
