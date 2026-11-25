export type MotionType =
  | "zoomInPanRight"
  | "craneTiltUp"
  | "macroSlowPush"
  | "pullBackTwilight";

export interface CalloutSpec {
  id: string;
  /** Target point X percentage in 1920x1080 frame (safe range 16..74) */
  xPct: number;
  /** Target point Y percentage in 1920x1080 frame (safe range 24..66) */
  yPct: number;
  /** Direction the leader line & telemetry card extend from the pin */
  cardAlign: "left" | "right";
  label: string;
  detail: string;
  /** Delay in frames relative to scene start */
  delayFrames: number;
}

export interface SceneSpec {
  id: string;
  from: number;
  durationInFrames: number;
  image: string;
  audio: string;
  chapter: string;
  title: string;
  subtitle: string;
  narration: string;
  motion: MotionType;
  callouts: CalloutSpec[];
}

export const FPS = 30;
export const TOTAL_DURATION_FRAMES = 900; // Exact 30.0s @ 30fps
export const CROSSFADE_FRAMES = 15;

export const SCENES: SceneSpec[] = [
  {
    id: "scene_01",
    from: 0,
    durationInFrames: 240,
    image: "assets/scene_01_aerial_canopy.png",
    audio: "audio/scene_01.mp3",
    chapter: "01 / 宏观体量",
    title: "大阪站城 · 巨型斜向天幕",
    subtitle: "横跨铁道上空约百米，银色斜向玻璃天幕重塑关西门户天际线",
    narration: "横跨铁道上空约百米，银色斜向玻璃天幕重塑了关西门户的天际线。",
    motion: "zoomInPanRight",
    callouts: [
      {
        id: "s1_c1",
        xPct: 30,
        yPct: 35,
        cardAlign: "right",
        label: "南北倾斜玻璃大屋盖",
        detail: "长约 180m · 宽约 100m",
        delayFrames: 28,
      },
      {
        id: "s1_c2",
        xPct: 68,
        yPct: 56,
        cardAlign: "left",
        label: "立体站城开发体量",
        detail: "无缝衔接南北商业塔楼",
        delayFrames: 78,
      },
    ],
  },
  {
    id: "scene_02",
    from: 225,
    durationInFrames: 240,
    image: "assets/scene_02_space_truss.png",
    audio: "audio/scene_02.mp3",
    chapter: "02 / 结构力学",
    title: "大跨度空间钢管桁架",
    subtitle: "在不停运的繁忙铁道上方，巨型立体管桁架实现无柱大跨度跨越",
    narration: "在不停运的繁忙铁道上方，巨型立体管桁架实现了无柱大跨度跨越。",
    motion: "craneTiltUp",
    callouts: [
      {
        id: "s2_c1",
        xPct: 28,
        yPct: 31,
        cardAlign: "right",
        label: "斜交三角空间管桁架",
        detail: "高强钢管立体受力网格",
        delayFrames: 28,
      },
      {
        id: "s2_c2",
        xPct: 66,
        yPct: 58,
        cardAlign: "left",
        label: "时空之广场 · 跨线连廊",
        detail: "悬挑公共空间俯瞰站台",
        delayFrames: 78,
      },
    ],
  },
  {
    id: "scene_03",
    from: 450,
    durationInFrames: 240,
    image: "assets/scene_03_tectonic_joint.png",
    audio: "audio/scene_03.mp3",
    chapter: "03 / 细部构造",
    title: "抗震节点与点支承幕墙",
    subtitle: "精密铸钢球铰节点与不锈钢四爪驳接件，兼顾抗震变形与通透采光",
    narration: "精密铸钢球铰与不锈钢四爪驳接件，兼顾了抗震变形与通透采光。",
    motion: "macroSlowPush",
    callouts: [
      {
        id: "s3_c1",
        xPct: 31,
        yPct: 40,
        cardAlign: "right",
        label: "重型铸钢销轴节点",
        detail: "吸收强震与风压多向位移",
        delayFrames: 28,
      },
      {
        id: "s3_c2",
        xPct: 68,
        yPct: 55,
        cardAlign: "left",
        label: "点支承夹胶玻璃天幕",
        detail: "不锈钢驳接爪精密锚固",
        delayFrames: 78,
      },
    ],
  },
  {
    id: "scene_04",
    from: 675,
    durationInFrames: 225,
    image: "assets/scene_04_twilight_hub.png",
    audio: "audio/scene_04.mp3",
    chapter: "04 / 城市脉动",
    title: "梅田立体交通枢纽",
    subtitle: "日均承接数百万客流，让硬核钢构骨架升华为充满温度的城市客厅",
    narration: "日均承接数百万客流，让硬核钢构骨架升华为充满温度的城市客厅。",
    motion: "pullBackTwilight",
    callouts: [
      {
        id: "s4_c1",
        xPct: 26,
        yPct: 36,
        cardAlign: "right",
        label: "多层级轨交立交体系",
        detail: "JR · 阪急 · 阪神 · 地铁全域换乘",
        delayFrames: 24,
      },
      {
        id: "s4_c2",
        xPct: 68,
        yPct: 57,
        cardAlign: "left",
        label: "蓝调时刻城市光影",
        detail: "从交通节点到立体都市客厅",
        delayFrames: 72,
      },
    ],
  },
];
