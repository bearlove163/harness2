---
name: recursive-forensic-research
description: >-
  Conducts multi-dimensional recursive deep research, engineering provenance archaeology,
  cross-disciplinary physical verification, and multimodal technical infographic synthesis for mega-structures
  (spatial steel structures, supertall buildings), transit hubs, and major conference/sports venues based on
  the Research Harness² methodology. Use when investigating engineering feats, forensic failure analyses,
  urban transit systems, supertall towers, or complex project provenance requiring multi-perspective validation
  and visual evidence beyond surface-level web summaries.
---

# Recursive Forensic Research Skill (基于 Harness² 的多维递归深度调研与溯源)

本技能指导智能体在面对复杂重大工程、科技设施、大跨空间结构、超高层摩天大楼、综合交通枢纽或高规格政体场馆等课题时，运用双层递归、对抗探针、多领域力学/物理基准核验以及多模态工程视觉图谱生成，交付具备工程级信度、图文互证与反思深度的专业研究简报与学术专著。

---

## 核心执行流程架构

```
[阶段 1: 时空锚点锁定] ──> [阶段 2: 任务级三阶段探针生成] ──> [阶段 3: 五级出处拓扑仲裁]
                                │                                     │
                                ▼                                     ▼
                     [阶段 4: 多领域沙盒参数复核]              [阶段 4.5: 多模态工程视觉转译与信息图生成]
                                │                                     │
                                └─────────────────┬───────────────────┘
                                                  ▼
                                      [阶段 5: 全景简报与图文融合交付]
```

---

## 阶段 1：时空锚点前置锁定（Temporal Guardrail）

1. **提取系统当前时间**：在执行任何检索之前，读取环境元数据或提示词中的当前物理时间（年、月、日）；
2. **构建时效硬约束关键词**：
   * 严禁无时间限制地搜索宽泛历史词条；
   * 搜索词必须显式绑定目标时间窗口（如查询近期1个月，若系统当前时间为 2026-10，则检索式必须强制锁定 `"September 2026"`、`"October 2026"` 或 `"2026"`）；
3. **前置跨年校验**：若抓取到的公开页面为往届信息（如 2024 年旧闻），必须明确标识为“历史对比样本”，不得当做当前现状汇报。

---

## 阶段 2：任务级递归探针生成（Propose–Probe–Compose）

面对调研目标，智能体不可直接单兵搜索，应在任务级递归中自发构建 3 组对抗探针：

* **Probe-Alpha（源流与演变考古探针）**：
  * 追溯项目原点：何时由谁构想？最初的结构/规划范式是什么？
  * 关键突变节点：中间是否经历过灾变事故（如风暴坍塌、地质沉降、火灾）、重大赛事升级改造或产权易手？
  * 主导大师与设计流派：主持建筑师与核心结构顾问（如 SBP, Arup, SOM, Thornton Tomasetti）的设计哲学与技术渊源。
* **Probe-Beta（力学与本构穿透探针）**：
  * 穿透 PR 营销公关词汇，探究核心受力与物理机制：
    * **空间钢结构**：支座反力传递路径、外压环与内拉环自平衡、可开合动力机构与折叠膜运动学、减隔震支座；
    * **超高层建筑**：高宽比、巨型组合柱、伸臂桁架、风致振动与阻尼器（TMD/粘滞阻尼器）；
    * **交通枢纽**：空铁轨接驳动线、高峰小时人流通量、大跨悬挑挑篷防风吸。
* **Probe-Gamma（对抗与隐患质疑探针）**：
  * 主动寻找反例与隐患：极端天气（暴风雪、台风、大温差）下的安全余量、材料疲劳周期、历史事故记录、实际施工维权工期延误与高昂全生命周期运维成本。

---

## 阶段 3：五级出处信度拓扑仲裁（Evidence Hierarchy）

当不同渠道数据发生冲突（如用钢量、跨度、疏散时限、造价）时，依据五级信度拓扑进行仲裁，详见规范指南：
👉 **[五级出处信度权重与冲突消解规范](./references/provenance_hierarchy.md)**

* **W1 级（最高，100% 采信）**：主持大师/结构总工签名图纸、学术学报论文（IASS, ASCE, SBP 学术论文集）、发明专利；
* **W2 级（90% 采信）**：国家/国际行业规范标准（Eurocode, AISC, GB 规范）、政府验收审计报告；
* **W3 级（80% 采信）**：总承包商工法技术总结、现场传感器监测日志（SHM Logs）；
* **W4 级（65% 采信）**：专业建筑/工程期刊杂志深度报道（如《Detail》、《Structure Magazine》）；
* **W5 级（30% 审慎）**：商业宣传通稿、体育新闻、维基百科（存在公关夸大或口径混淆时做纠偏提示）。

---

## 阶段 4：多领域沙盒参数复核（Sandbox Sanity Check）

在推演报告生成前，智能体可调用内置的工程参数复核脚本，对跨度、用钢量、高宽比或疏散通量进行常识验算：
👉 **[工程参数核验脚本](./scripts/engineering_sanity_check.py)**
👉 **[多领域工程经验基准表](./references/multi_domain_benchmarks.md)**

### 调用示例（根据涉及领域自主选择）：
```powershell
# 1. 大跨度空间网格/索网结构核验
python .agents/skills/recursive-forensic-research/scripts/engineering_sanity_check.py spatial --span 200 --depth 15 --area 37800 --steel 7200 --type spoke_wheel

# 2. 超高层建筑细长比与周期核验
python .agents/skills/recursive-forensic-research/scripts/engineering_sanity_check.py supertall --height 450 --width 45 --area 250000 --floors 100 --steel 35000

# 3. 交通枢纽/大型场馆人群安全疏散核验
python .agents/skills/recursive-forensic-research/scripts/engineering_sanity_check.py transit --capacity 54500 --width 120 --distance 80 --limit 8.0
```

---

## 阶段 4.5：多模态工程视觉证据采集与素材锚定图谱合成（Visual Evidentiary Synthesis）

重大工程与法医级调研涉及极为复杂的空间受力、地质嵌岩剖面、水工绝缘及历史改建突变，单纯依赖 Markdown 文本与公式易产生空间感知与力学认知盲区。为保证研究成果具备高度的直观性与学术/工程信度，必须建立**“真实摄影档案与实证素材锚定 AI 图谱双轨协同”**的视觉证据采集范式：

### 1. 视觉证据双轨协同范式（Dual-Track Evidentiary Paradigm）
* **轨道 A：网络实景与历史档案摄影轨（宏观现状与历史真值）**：
  * **第一优先（W1-W3 级）**：必须优先检索官方渠道（主创建筑师官网、总承包商工法总结、行业学报期刊图纸、施工现场实录及开放档案图库如 Wikimedia Commons）；
  * **允许直接引注与截图**：只要能真实表达工程力学本构、构造节点、地质水工或改建场景的实景照片或图纸，均应下载或截图归档，并在报告中注明权威出处（如 `[来源: Grimshaw / New Steel Construction / Bachy Soletanche]`）。
* **轨道 B：基于实证素材锚定的 AI 工程图谱合成轨（深层机理与隐蔽物理学）**：
  * **不可替代性优势**：很多关键工程本构（如大跨度桁架有限元受力云图、暖通气流 CFD 流速矢量场、地下隐蔽综合管沟三维爆炸架构图）是相机无法直接拍摄的。此时使用 **AI 信息图表（Infographics）与工程仿真云图** 往往比单张表面照片能更透彻、更本质地阐明物理规律；
  * **素材锚定硬约束（Grounded Material Constraint）**：AI 生图绝不能凭空想象或虚构科幻造型，其底层素材、几何拓扑、边界条件必须来源于网络检索到的真实图纸、实景抓取与计算书数据（如以真实的 86.9m 净跨、5m 桁高、34~44m 桩基入岩深度、18 kN/m² 荷载为素材骨架）；
  * **宁缺毋滥底线**：严禁调用生成与工程本体无关、卡通化或虚假幻觉的泛化图像；对于云图、受力图与系统架构图，必须保持现代工程 CAE/BIM 蓝图级的专业严谨度。

### 2. 核心图谱类型与适用场景
1. **有限元力学云图（FEA Stress & Deflection Contour Cloud Maps）**：
   * 展示屋盖桁架、索膜节点在极端风雪或吊载下的 Von Mises 应力集中红黄蓝彩虹色谱分布及形变挠度曲线；
2. **计算流体力学流场云图（CFD Airflow & Diffusion Velocity Maps）**：
   * 展示战时改建或大跨空间内的全新风置换气流矢量、负压梯度云图及气溶胶扩散阻隔效应；
3. **三维立体系统架构图（Exploded Architectural & MEP Infrastructure Maps）**：
   * 表达多层复合地坪（预应力连续板 + 5m×3m 综合管沟矩阵 + 跑车表层改性）与水工桩基平台的三维分层装配关系。

### 3. 图像资产归档与报告内嵌规范
* **资产固化**：检索下载的实景图片或合规生成的工程云图/架构图，必须统一持久化保存在当前会话的产物目录（Artifact Directory）下：`<appDataDir>\brain\<conversation-id>\images\`；
* **标准引用语法**：在交付的专业研究报告或白皮书 Markdown 产物中，必须使用标准的绝对路径进行内嵌引用：`![图释描述](/绝对路径/image_name.jpg)`，并在下方附带斜体详细工程图注、出处评级与机理说明。

---

## 阶段 5：结构化交付标准（Professional Brief & Visual Output）

最终交付的项目专业简报或技术专著必须包含以下标准模块：
1. **时空与事件定位**：严格以系统当前时间为锚点，明确赛事/会议名称、精确日期与交通枢纽空铁接驳；
2. **出处源流与范式演变**：清晰梳理项目从最初母体到当今形态的进化脉络（包含事故/改建驱动力）；
3. **核心物理与工程技术精剖**：建筑面积、跨度（受力净跨）、用钢量（注明主体还是总含钢量）、大师团队哲学、特殊空间受力本构与抗震减隔震；
4. **多模态工程视觉图谱**：内嵌至少 1~2 幅高精度工程剖切信息图或极限场景法医对比图；
5. **多维批判性思辨与运维大考**：剖析极端气候应对、生命周期运维痛点及未来承接顶级负荷的考验；
6. **数据源拓扑与信度溯源**：对关键争议数据标明其信度等级（W1-W5）并阐明消解结论。
