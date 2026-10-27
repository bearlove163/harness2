# 多模态工程视觉证据采集与真实性溯源规范指南 (Visual Evidentiary Guidelines)

在运用 Research Harness² 开展重大工程、大跨空间结构、超高层建筑及复杂交通枢纽的法医级调研（Recursive Forensic Research）时，由于研究对象涉及大量三维空间传力路径、地质分层嵌固关系、地下管网矩阵以及极端工况下的突变改造，单纯依靠文字描述与二维公式往往难以建立全景空间直觉。

本指南确立了智能体在为工程报告匹配图像资产时的**“真实出处优先、逐章就地嵌入、实证参数锚定生成、双轨路径固化”**的核心铁律。

---

## 1. 图像证据真实性层级与采集策略

### 第一层级：网络与历史档案真实出处（优先度：最高，必须优先执行）
* **W1-W4 级真实图片库**：
  * **权威历史与开放媒体图库**（优先：Wikimedia Commons、城市历史档案馆、国家图书馆数字化档案）：搜索原点规划蓝图手稿、开工奠基照、母体施工现场、历次重大改建历史对比照片；
  * **主创设计院/大师事务所官网**（如 Populous, Thornton Tomasetti, Foster + Partners, SOM, SBP）：官方高精度竣工摄影、剖面与轴测概念分析图；
  * **施工总包与专业分包商档案**（如 Mortenson, Bachy Soletanche, Severfield, Keller）：现场打桩作业、大吨位液压托换提升、基坑支护监测等施工工法实景照片；
  * **行业学术期刊与专业工程媒体**（如《Structure Magazine》、《Modern Steel Construction》、《Detail》、ASCE / DFI 论文集）：结构细部构造大样图、节点详图。
* **检索与抓取工法**：
  * 编写 Python 脚本调用开放 API（如 Wikimedia MediaWiki API）或网络检索图片直链；
  * 本地持久化保存至当前会话产物目录 `brain/<conversation-id>/images/`；
  * 规范命名：`<domain>_<topic>_<source_or_year>.jpg`。

### 第二层级：基于实证素材与物理计算锚定的 AI 工程图谱合成（云图/剖切图/仪表盘）
* **不可替代性场景（Why AI Infographics Excel Over Raw Photos）**：
  * 真实摄影只能记录建筑暴露在外的表面宏观形态，而对于深层力学本构、隐蔽物理机理与极端灾害工况，**相机无法拍摄“不可见的物理过程”**；
  * 在表达**有限元受力云图（FEA Stress Contours）**、**逆作托换三维工程剖切图（3D Structural Cutaways）**、**计算流体力学流场与防排烟云图（CFD Velocity/Smoke Maps）**、**工艺水工闭环流程图**以及**出处仲裁沙盒仪表盘**时，AI 信息图表在信息密度、传力机理直观性上具有压倒性优势。
* **网络素材锚定铁律（Grounded Material Constraint）**：
  * **实证参数前置输入**：AI 生图所依据的几何跨度（如 122m 跨度）、构件尺寸（如 8m 桁高）、载荷吨位（4,400 万磅）、深挖深度（53~65 ft）、地质分层及计算耗时（5.81 min），必须直接来自真实检索到的官方图纸、工法白皮书或沙盒核算真值；
  * **严禁凭空想象**：提示词工程中必须显式输入网络检索到的真实力学参数与空间尺度，杜绝科幻化、卡通化或臆造构件，保持 CAE/BIM 蓝图级的专业严谨度。

---

## 2. 全流程章节级图文闭环矩阵（Chapter-by-Chapter Anchoring）

在撰写正式调研白皮书时，**必须在每个核心章节的正文下方紧随嵌入专属视觉证据**，严禁堆砌于文末附录：

| 章节与探针模块 | 必备图像资产类别 | 典型内容与视觉标准 | 推荐来源路径 |
| :--- | :--- | :--- | :--- |
| **阶段 1：时空锚点与全景定位** | **项目概览与参建网络图板 (Dashboard)** | 包含时空锚点、核心运营指标、权威认证徽章与核心参建联合体拓扑卡片 | 实证参数锚定生成 (V3) |
| **2.1 Probe-Alpha（源流考古探针）** | **大师手稿蓝图 / 原始建造实录** | 主创总师审阅图纸现场、母体初建工地三叉桥台与大跨吊装、历史改建旧照 | 网络真实档案照片 (V1/V4) |
| **2.2 Probe-Beta（力学本构穿透探针）** | **① 临时托换深开挖三维剖切图<br>② FEA 彩虹应力云图<br>③ 特色水工/机电流程图** | ① 悬空屋盖、临时钢格构柱、深坑排桩与永久地锚拓扑<br>② Von Mises 应力彩虹谱（0~350 MPa）与动力解耦滑动支座<br>③ 虹吸雨水汇流、超纯脱盐脱气至热泵制冰闭环流程 | 实证参数锚定生成 (V3) |
| **2.3 Probe-Gamma（对抗与隐患质疑探针）** | **① 极端灾害/疏散流场图解<br>② 高负荷满场运营实况** | ① 地下逆重力人员疏散路线、正压送风防烟楼梯间与事故排烟风机流场<br>② 满负荷赛事/演艺现场，验证无柱大跨与地下沉降碗实际运行状态 | ① 实证参数锚定生成 (V3)<br>② 网络真实赛事摄影 (V4) |
| **阶段 3 与 4：信度仲裁与沙盒核验** | **五级出处金字塔与沙盒双联仪表盘** | 左侧展示 W1 至 W5 级文献金字塔与争议数据消解表；右侧通过发光表盘展示跨高比与疏散时限验算真值 | 实证参数锚定生成 (V3) |
| **阶段 5：全生命周期反思** | **当代宏观全景实录 (Hero Shot)** | 当代现状全貌、夜景航拍或城市地标共生全景，见证历史保护与地下科技地宫的共生 | 网络真实高清摄影 (V1/V4) |

---

## 3. 实证信息图 Prompt 工程黄金模板库（Tested Prompt Recipes）

调用 `image-generator` 子智能体生成实证工程图谱时，必须遵循以下标准化提示词结构：

### 模板 1：项目概览与参建网络信息图板（Project Profile & Consortium Dashboard）
```text
Generate a professional, high-resolution executive project dashboard infographic for [Project Name] based on:
1. Header: [PROJECT NAME] — PROJECT PROFILE & OPERATIONAL TOPOLOGY ([Location] | [Coordinates])
2. Operational Metrics Card: Milestone years, primary tenants/events, seating capacity, square footage, subterranean depth.
3. Sustainability / Certification Badge: Glowing certification badge (e.g. Net Zero Carbon, LEED Platinum), key environmental systems.
4. Engineering Consortium Card Grid: Clean, modular non-overlapping cards for Owner/Operator, Lead Architect, Structural Engineer, Geotechnical Engineer, General Contractor, and Specialty Suppliers.
5. Aesthetic: Modern dark-navy architectural infographic dashboard, clean modular cards, sleek vector icons, sharp typography, Engineering News-Record (ENR) / AIA presentation poster style.
```

### 模板 2：三维轴测工程剖切图（3D Structural Cutaway）
```text
Generate a detailed architectural and structural engineering cutaway illustration of [Project Name] during its major reconstruction:
1. Show the iconic preserved historic roof ([Weight in lbs/tonnes], [Span dimensions]) suspended in mid-air.
2. Supported by temporary heavy steel shoring columns ([Color e.g. bright orange], [Number of columns e.g. 72]) drilled deep into bedrock/glacial till.
3. Below the floating roof, show the deep subterranean excavation pit ([Depth in ft/m]) with soldier-pile retaining walls and drilled permanent tiebacks.
4. Show early concrete/steel framing for the new lower bowl emerging from the pit bottom.
5. Style: High-end architectural engineering illustration, detailed structural cross-section diagram style (similar to Architectural Record / ENR / Detail magazine), realistic lighting, crisp technical rendering.
```

### 模板 3：有限元 FEA 彩虹应力与变形云图（CAE / FEA Stress Simulation）
```text
Generate an advanced engineering Finite Element Analysis (FEA) computer simulation visualization of [Project Name] structural system:
1. A 3D CAE/FEA finite element structural model displaying the long-span roof trusses, massive concrete abutments, and subterranean retaining walls.
2. Color-coded Von Mises stress contour field across the steel trusses and supports: rainbow gradient spectrum from cool blue (low stress 0-50 MPa), green (nominal), to yellow and red stress concentrations (250-350 MPa) at truss joints and seismic fuse interfaces.
3. Aesthetic: Structural analysis software screen (ANSYS, SAP2000, Abaqus), subtle mesh lines, color calibration scale/legend on the side (in MPa), nodal load vectors, clean technical CAD viewport background.
```

### 模板 4：地下逆重力人员疏散与防排烟动力学图解（Egress & Smoke Purge Dynamics）
```text
Generate an architectural and engineering safety cutaway diagram illustrating subterranean crowd evacuation and smoke purge dynamics for [Project Name]:
1. Cutaway cross-section of the deep subterranean seating bowl ([Depth in ft/m]).
2. Upward crowd evacuation dynamics: safety-green flow arrows moving upwards from bowl floor/concourses towards ground-level plaza exits.
3. Life-safety mechanics: pressurized positive-pressure emergency stairwells (cool cyan airflow) and overhead mechanical smoke purge plenums extracting buoyant fire smoke plumes (warm orange gradient) away from egress corridors.
4. Technical callouts: "NFPA Egress Limit: [X] min", "Calculated Evacuation Flow: [Y] min (PASS)", "Total Exit Width: [Z]m", "Positive-Pressure Stairwells".
5. Style: NFPA / ENR magazine technical life-safety graphic, dark background with luminous vector routes and airflow vectors.
```

### 模板 5：五级信度金字塔与沙盒验算双联仪表盘（Provenance & Sanity Check Dashboard）
```text
Generate a high-end engineering infographic dashboard illustrating the "5-Tier Provenance Hierarchy (W1-W5)" and "Sandbox Sanity Check Benchmarks" for [Project Name]:
1. Header: RESEARCH HARNESS² — PROVENANCE ARBITRATION & SANDBOX SANITY CHECK
2. Left Section: 5-Tier Evidence Pyramid showing W1 (Calculations/Patents) down to W5 (PR Press), with an arbitration table resolving core disputed parameters (Weight, Steel Tonnage, Excavation, Cost).
3. Right Section: Engineering Sandbox Sanity Check Gauges with glowing PASS status badges (Gauge 1: Roof Span-to-Depth Ratio; Gauge 2: Subterranean Evacuation Flow vs NFPA limits).
4. Style: Crisp dark-mode engineering HUD dashboard, sleek vector gauges, scientific presentation poster format.
```

---

## 4. 图像资产命名与双轨持久化规范

1. **命名统一小写下划线**：`<project_prefix>_<topic_slug>.jpg`（如 `climate_pledge_rain_to_rink.jpg`、`century_21_exposition_construction_1961.jpg`）；
2. **会话产物目录**：存储在 `<appDataDir>\brain\<conversation-id>\images\`，供即时对话渲染；
3. **仓库沉淀目录**：同步复制至 `docs/research/<project_slug>/images/`；
4. **相对路径转换**：在同步至 Git 仓库的 Markdown 报告中，必须将绝对路径替换为标准相对路径 `./images/<filename>.jpg`，确保在 GitHub 网页、本地 IDE 与离线 Markdown 渲染器中完全免配置秒开。
