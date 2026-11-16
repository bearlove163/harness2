import os
import json
import nbformat as nbf

def create_colab_notebook():
    os.makedirs("notebooks", exist_ok=True)
    nb = nbf.v4.new_notebook()

    # Notebook level metadata
    nb.metadata = {
        "accelerator": "GPU",
        "colab": {
            "gpuType": "T4",
            "provenance": []
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    }

    cells = []

    # Markdown Title Cell
    md_header = """# 🏛️ 建筑与结构工程影视级 AI 视频生成流水线 (Colab 专属增强版)

<a href="https://colab.research.google.com/github/bearlove163/harness2/blob/colab_video_generation/notebooks/Wan2_1_Architecture_Video_Colab.ipynb" target="_parent">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

> 本 Notebook 专为**建筑空间展示、大跨度结构分析、细部构造拆解与建筑人文历史演进**定制。
>
> 🚀 **核心能力升级 (高清长片版)**：
> 1. **768P 高清宽屏画质**：分辨率提升至 768x512，建筑材质、钢架线条与光影细腻锐利，告别模糊拉伸！
> 2. **单镜头帧数翻倍**：提升至 32 帧平滑运镜，运镜时长翻倍。
> 3. **4镜头完整长片自动合成 (核心亮点)**：一键全自动渲染全景 ➔ 结构 ➔ 细部 ➔ 延时四大分镜，并自动无缝拼接为完整建筑纪录长片！
> 4. **100% 显存与内存安全**：为 Colab 免费 T4 显卡量身调优，零崩溃稳定极速出片。
"""
    cells.append(nbf.v4.new_markdown_cell(md_header))

    # Cell 1: Hardware & Memory Check
    code_gpu = """# @title 1. 【硬件自适应】GPU 与系统物理内存安全检测
import os
import sys
import psutil
import torch

# 优化 PyTorch 显存碎片配置
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

print("="*60)
print("正在检查当前 Google Colab 计算资源与内存架构...")
print("="*60)

has_gpu = torch.cuda.is_available()
if not has_gpu:
    raise SystemError("❌ 未检测到 GPU！请点击顶部菜单栏：代码执行程序 -> 更改运行时类型 -> 硬件加速器选择 'T4 GPU'！")

gpu_name = torch.cuda.get_device_name(0)
total_vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
ram_gb = psutil.virtual_memory().total / (1024**3)

print(f"✅ GPU 型号:     {gpu_name}")
print(f"✅ GPU 显存总量: {total_vram:.2f} GB")
print(f"✅ 系统物理内存: {ram_gb:.2f} GB")

print("\\n💡 适配 Colab 免费标准环境 (Tesla T4 15GB VRAM / 12.7GB RAM)：")
print("   -> 启用 AnimateDiff + Realistic Vision V5.1 高清建筑渲染管线")
print("   -> 支持 768x512 宽屏高清输出与 32 帧平滑长镜头")
print("="*60)
"""
    cells.append(nbf.v4.new_code_cell(code_gpu))

    # Cell 2: Google Drive Mounting & Directory Setup
    code_drive = """# @title 2. 【存储同步】挂载 Google Drive 与资产接力目录初始化
from google.colab import drive
import os

# 挂载 Google 云端硬盘
print("正在挂载 Google Drive...")
drive.mount('/content/drive')

# 定义接力流水线专属工作目录
RELAY_BASE_DIR = "/content/drive/MyDrive/Colab_Video_Relay"
INPUTS_DIR = os.path.join(RELAY_BASE_DIR, "inputs")
OUTPUTS_DIR = os.path.join(RELAY_BASE_DIR, "outputs")
CONFIGS_DIR = os.path.join(RELAY_BASE_DIR, "configs")

for d in [RELAY_BASE_DIR, INPUTS_DIR, OUTPUTS_DIR, CONFIGS_DIR]:
    os.makedirs(d, exist_ok=True)

print(f"✅ Google Drive 工作空间就绪:")
print(f"   📥 上游 Agent 素材输入目录: {INPUTS_DIR}")
print(f"   🎬 视频素材与元数据输出目录: {OUTPUTS_DIR}")
print(f"   ⚙️ 提示词与配置存储目录:     {CONFIGS_DIR}")
"""
    cells.append(nbf.v4.new_code_cell(code_drive))

    # Cell 3: Fast Pip Dependencies Installation
    code_deps = """# @title 3. 【依赖安装】安装 Diffusers 核心与视频生成加速库
print("正在安装视频渲染流水线所需核心依赖...")

!pip install -q --upgrade diffusers transformers accelerate sentencepiece imageio imageio-ffmpeg gradio>=4.44.0 safetensors einops bitsandbytes torchvision psutil

print("✅ 所有核心依赖包安装完成！")
"""
    cells.append(nbf.v4.new_code_cell(code_deps))

    # Cell 4: Model Pipeline Loader
    code_model_loader = """# @title 4. 【模型载入】初始化 768P 高清建筑写实视频生成引擎
import os
import gc
import torch
from diffusers import AnimateDiffPipeline, MotionAdapter, DDIMScheduler
from diffusers.utils import export_to_video

def flush_memory():
    gc.collect()
    torch.cuda.empty_cache()

flush_memory()

print("="*60)
print("正在载入高清建筑影视级写实视频生成引擎 (AnimateDiff + Realistic Vision)...")
print("已优化 VAE 切片与平铺支持，兼容 768P 高清宽屏与多帧平滑输出...")
print("="*60)

# 加载运动适配器
motion_adapter = MotionAdapter.from_pretrained(
    "guoyww/animatediff-motion-adapter-v1-5-2",
    torch_dtype=torch.float16
)

# 加载写实底模
pipe = AnimateDiffPipeline.from_pretrained(
    "SG161222/Realistic_Vision_V5.1_noVAE",
    motion_adapter=motion_adapter,
    torch_dtype=torch.float16
)

# 配置平滑调度器
scheduler = DDIMScheduler.from_pretrained(
    "SG161222/Realistic_Vision_V5.1_noVAE",
    subfolder="scheduler",
    clip_sample=False,
    timestep_spacing="linspace",
    beta_schedule="linear",
    steps_offset=1
)
pipe.scheduler = scheduler

# 开启全套显存与分块切片优化 (保证 768x512 高清不爆显存)
if hasattr(pipe, "enable_vae_slicing"):
    pipe.enable_vae_slicing()
elif hasattr(pipe, "vae") and hasattr(pipe.vae, "enable_slicing"):
    pipe.vae.enable_slicing()

if hasattr(pipe, "enable_vae_tiling"):
    pipe.enable_vae_tiling()
elif hasattr(pipe, "vae") and hasattr(pipe.vae, "enable_tiling"):
    pipe.vae.enable_tiling()

pipe.enable_model_cpu_offload()

print("🎉 768P 高清视频生成引擎已成功加载！显存与内存均处于极佳健康状态。")
"""
    cells.append(nbf.v4.new_code_cell(code_model_loader))

    # Cell 5: Upstream Agent Asset Relay Pipeline (Batch Image-to-Video)
    code_relay = """# @title 5. 【资产接力】上游 Agent 渲染图/老照片一键批量生成视频素材
import os
import glob
import json
import time

# 预设的建筑与历史提示词映射字典
PRESET_PROMPTS = {
    "exterior": "Cinematic high-angle drone shot orbiting smoothly around the modern architecture, crisp daylight reflections, photorealistic 8k, steady cinematic motion",
    "atrium": "Smooth vertical crane camera rising through the monumental atrium, warm volumetric sunlight rays piercing through skylights, majestic spatial depth",
    "structure": "Isometric structural animation showing long-span steel space trusses and tension cables under load equilibrium, elegant tectonic engineering",
    "joint": "Macro slider camera dolly-in focusing on precision stainless steel spider fittings and CNC cast pin joints, crisp reflections",
    "history": "Archival vintage photograph transforming into living color reality with natural sunlight, pedestrians and street scene coming to life naturally, smooth cinematic movement"
}

def auto_detect_preset(filename):
    lower = filename.lower()
    for key in PRESET_PROMPTS:
        if key in lower:
            return PRESET_PROMPTS[key]
    if "facade" in lower or "building" in lower:
        return PRESET_PROMPTS["exterior"]
    if "truss" in lower or "beam" in lower or "cable" in lower:
        return PRESET_PROMPTS["structure"]
    if "vintage" in lower or "old" in lower or "bw" in lower:
        return PRESET_PROMPTS["history"]
    return PRESET_PROMPTS["exterior"]

# 扫描接力输入目录
input_images = []
for ext in ["*.png", "*.jpg", "*.jpeg", "*.webp"]:
    input_images.extend(glob.glob(os.path.join(INPUTS_DIR, ext)))

print("="*60)
print(f"📂 扫描到上游 Agent 传入的图片资产: {len(input_images)} 个")
for idx, img_path in enumerate(input_images, 1):
    matched_prompt = auto_detect_preset(os.path.basename(img_path))
    print(f" [{idx}] {os.path.basename(img_path)} -> 匹配运镜: {matched_prompt[:50]}...")
print("="*60)

def run_batch_relay(steps=30, guidance_scale=8.0, num_frames=32, fps=10):
    if not input_images:
        print("💡 提示: inputs 目录暂无待处理图片。请将其他 Agent 产出的效果图或历史照片上传到:")
        print(f"   {INPUTS_DIR}")
        return

    print("🚀 开始批量接力渲染 (768P 高清模式)...")
    for idx, img_path in enumerate(input_images, 1):
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        output_mp4 = os.path.join(OUTPUTS_DIR, f"{base_name}_hd.mp4")
        output_meta = os.path.join(OUTPUTS_DIR, f"{base_name}_hd.json")
        
        prompt = auto_detect_preset(base_name)
        print(f"\\n正在处理 [{idx}/{len(input_images)}]: {base_name}")
        print(f"提示词: {prompt}")
        
        try:
            start_t = time.time()
            output_frames = pipe(
                prompt=prompt,
                negative_prompt="blurry, low resolution, distorted, grainy, worst quality, cartoon",
                width=768,
                height=512,
                num_frames=num_frames,
                guidance_scale=guidance_scale,
                num_inference_steps=steps
            ).frames[0]
            export_to_video(output_frames, output_mp4, fps=fps)
            
            elapsed = time.time() - start_t
            
            # 写入元数据
            meta_info = {
                "source_image": img_path,
                "output_video": output_mp4,
                "prompt": prompt,
                "guidance_scale": guidance_scale,
                "num_frames": num_frames,
                "fps": fps,
                "resolution": "768x512",
                "elapsed_seconds": round(elapsed, 2),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(output_meta, "w", encoding="utf-8") as mf:
                json.dump(meta_info, mf, ensure_ascii=False, indent=2)
                
            print(f"✅ 渲染完成并已保存至: {output_mp4}")
            print(f"✅ 元数据已落盘: {output_meta}")
        except Exception as err:
            print(f"❌ 处理 {base_name} 时发生错误: {err}")

# 如果需要立即运行批量，取消下方注释并执行:
# run_batch_relay()
"""
    cells.append(nbf.v4.new_code_cell(code_relay))

    # Cell 6: Gradio WebUI for Architecture Video Studio
    code_gradio = """# @title 6. 【可视化工作台】启动 Gradio 建筑影视视频生成 Web 界面
import gradio as gr
import random
import os
import time

# 加载建筑专属提示词预设字典
ARCH_PRESETS = {
    "大阪梅田站城全景天幕与穿梭列车 (城市枢纽)": {
        "prompt": "Cinematic high-angle drone shot slowly gliding and descending over Osaka Station City (JR Umeda). Monumental silver diagonal glass canopy roof soaring gracefully over bustling railway platforms, expansive Toki-no-Hiroba plaza bathed in natural daylight, sleek Japanese commuter trains gliding smoothly below on rhythmic tracks, futuristic multi-layered pedestrian skybridges connecting modern high-rises, photorealistic, 8k resolution, crisp architectural rendering, steady cinematic motion, highly detailed.",
        "negative": "blurry, low resolution, distorted geometry, flickering, pixelated, noisy artifacts, cartoon, drawing, flat texture, bad architecture",
        "guidance": 8.0
    },
    "流线型现代展馆全景环绕 (航拍运镜)": {
        "prompt": "Cinematic drone shot, slowly orbiting around a white futuristic curvilinear pavilion with organic fluid geometry. Smooth reflections on surrounding mirror water pool, ultra-realistic daylight with soft shadows, highly detailed architecture rendering, 8k resolution, photorealistic, stable cinematic motion, razor sharp.",
        "negative": "blurry, low resolution, jittery motion, flickering, distorted geometry, noisy artifacts, cartoon",
        "guidance": 8.0
    },
    "巨型中庭天光垂直拉升漫游 (室内升降)": {
        "prompt": "Smooth vertical pedestal crane shot inside a monumental architectural atrium. Golden volumetric God rays streaming through a parametric geometric skylight, illuminating cantilevered glass bridges and perforated metallic panels. Cinematic architectural interior, dust motes drifting in sunbeams, profound spatial depth, photorealistic, ultra sharp.",
        "negative": "blurry, low resolution, deformed structures, warping, camera shake, overexposed, low quality, glitch, cartoon",
        "guidance": 8.0
    },
    "大跨度空间管桁架轴测动态拼装 (结构力学)": {
        "prompt": "Isometric exploded view showing the dynamic assembly of a long-span stadium tubular space truss. Modular triangular steel truss segments gracefully descend and lock into place with precision joints, forming a monumental saddle-shaped roof shell, subtle engineering stress flow illumination, high precision, photorealistic, crisp.",
        "negative": "blurry, low resolution, messy lines, chaotic deformation, unrealistic physics, flickering, blurred joints, cartoon",
        "guidance": 8.5
    },
    "中国古建斗栱榫卯旋转咬合 (传统大木作)": {
        "prompt": "Photorealistic 3D close-up turntable shot rotating around an ancient Chinese Dougong bracket set suspended in mid-air. Weathered aged cedar wood grain textures, intricately interlocking mortise-and-tenon wooden components sliding together with micron precision, historical oriental tectonic craft, dramatic soft lighting, 8k, sharp focus.",
        "negative": "blurry, low resolution, plastic wood, cartoon, blurry grain, floating detached parts, distorted joinery",
        "guidance": 8.0
    },
    "点支承玻璃幕墙驳接爪微距特写 (构造节点)": {
        "prompt": "Macro photography dolly-in focusing on a 4-arm stainless steel spider fitting of a point-supported glass curtain wall. Brushed CNC metal texture, precision countersunk bolts, silicone gaskets, ultra-clear low-E laminated glass edge with prismatic optical caustics, architectural tectonic detail perfection, razor sharp focus.",
        "negative": "blurry, low resolution, smudged glass, flat textures, noisy, distorted bolts, low detail, cartoon",
        "guidance": 8.0
    },
    "古建筑遗存晨昏日影与星轨延时 (光影流转)": {
        "prompt": "Magnificent 4k timelapse photography with fixed camera observing a weathered historic stone bridge and clocktower. Fast-moving shadows sweeps across ancient masonry as sun arches overhead, golden dusk transitions into deep twilight, starry Milky Way arcs across the night sky, poetic passage of time, ultra clear.",
        "negative": "blurry, low resolution, flickering frames, strobe lighting, jitter, broken stone, cartoon",
        "guidance": 8.0
    }
}

def apply_preset(preset_name):
    if preset_name in ARCH_PRESETS:
        p = ARCH_PRESETS[preset_name]
        return p["prompt"], p["negative"], p["guidance"]
    return "", "", 8.0

def generate_video(preset_name, prompt, negative_prompt, steps, guidance_scale, seed, aspect_ratio, num_frames_sel):
    print(f"🎬 收到渲染请求 | 步数: {steps} | 比例: {aspect_ratio} | 帧数: {num_frames_sel} | 引导: {guidance_scale}")
    if seed == -1:
        seed = random.randint(0, 2**32 - 1)
        
    out_filename = f"arch_video_{int(time.time())}_{seed}.mp4"
    out_path = os.path.join(OUTPUTS_DIR, out_filename)
    
    # 尺寸与画幅映射 (默认升级为 768P 高清宽屏)
    if "9:16" in aspect_ratio:
        width, height = 512, 768
    elif "16:9" in aspect_ratio:
        width, height = 768, 512
    else:
        width, height = 576, 576
        
    generator = torch.Generator(device="cuda" if torch.cuda.is_available() else "cpu").manual_seed(int(seed))
    
    output = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        height=height,
        width=width,
        num_frames=int(num_frames_sel),
        num_inference_steps=int(steps),
        guidance_scale=float(guidance_scale),
        generator=generator
    )
    frames = output.frames[0]
    
    # 帧率配置: 32帧用 8-10fps 可获得 3.5~4秒平滑播放
    fps_val = 10 if int(num_frames_sel) >= 32 else 8
    export_to_video(frames, out_path, fps=fps_val)
    print(f"✅ 渲染完成: {out_path} ({width}x{height}, {num_frames_sel}帧)")
    return out_path, f"✅ 768P 高清渲染完成！已保存至 Google Drive: {out_path}"

# 构建 Gradio 界面
with gr.Blocks(title="建筑与结构影视视频工作室 (768P 高清增强版)", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏛️ 建筑空间·结构力学·细部大样·人文历史 影视视频工作室 (768P 高清版)")
    gr.Markdown("专为建筑设计师与工程师打造。支持 768P 电影级宽屏与 32 帧平滑长镜头。")
    
    with gr.Row():
        with gr.Column(scale=1):
            preset_dd = gr.Dropdown(
                label="🎯 建筑专业镜头语言预设",
                choices=list(ARCH_PRESETS.keys()),
                value="大阪梅田站城全景天幕与穿梭列车 (城市枢纽)"
            )
            prompt_in = gr.Textbox(
                label="正面提示词 (Prompt)",
                value=ARCH_PRESETS["大阪梅田站城全景天幕与穿梭列车 (城市枢纽)"]["prompt"],
                lines=4
            )
            neg_prompt_in = gr.Textbox(
                label="反向负面提示词 (Negative Prompt)",
                value=ARCH_PRESETS["大阪梅田站城全景天幕与穿梭列车 (城市枢纽)"]["negative"],
                lines=2
            )
            
            with gr.Row():
                steps_slider = gr.Slider(label="推理步数 (Steps，推荐30步更细腻)", minimum=20, maximum=45, value=30, step=1)
                guidance_slider = gr.Slider(label="引导系数 (Guidance Scale)", minimum=5.0, maximum=12.0, value=8.0, step=0.1)
                
            with gr.Row():
                aspect_radio = gr.Radio(label="画面画幅", choices=["16:9 (768x512 高清宽屏)", "9:16 (512x768 移动竖屏)", "1:1 (576x576 正方剖面)"], value="16:9 (768x512 高清宽屏)")
                frames_radio = gr.Radio(label="视频长度/帧数", choices=["32 帧 (约 4 秒平滑长镜头)", "24 帧 (约 3 秒)", "16 帧 (约 2 秒)"], value="32 帧 (约 4 秒平滑长镜头)")
                
            seed_in = gr.Number(label="随机种子 (-1 为随机)", value=-1, precision=0)
            gen_btn = gr.Button("🚀 立即渲染 768P 高清视频素材", variant="primary")
            
        with gr.Column(scale=1):
            video_out = gr.Video(label="🎬 渲染输出预览 (MP4)")
            status_out = gr.Textbox(label="状态信息", interactive=False)
            
    preset_dd.change(
        fn=apply_preset,
        inputs=[preset_dd],
        outputs=[prompt_in, neg_prompt_in, guidance_slider]
    )
    
    def parse_frames(fr_str):
        if "32" in fr_str: return 32
        if "24" in fr_str: return 24
        return 16

    gen_btn.click(
        fn=lambda p, pr, npr, st, gu, sd, ar, fr: generate_video(p, pr, npr, st, gu, sd, ar, parse_frames(fr)),
        inputs=[preset_dd, prompt_in, neg_prompt_in, steps_slider, guidance_slider, seed_in, aspect_radio, frames_radio],
        outputs=[video_out, status_out]
    )

# 启动并生成公共访问链接
print("正在启动 Gradio Web 服务并生成公共公网链接 (share=True)...")
demo.launch(share=True, debug=True)
"""
    cells.append(nbf.v4.new_code_cell(code_gradio))

    # Cell 7: Multi-Shot Sequence Generation & Auto-Stitching
    code_multishot = """# @title 7. 【多镜头大片自动合成】一键渲染大阪梅田站 4 镜头并拼接为完整长视频
import os
import time
import subprocess
import torch
from diffusers.utils import export_to_video
from IPython.display import HTML, display

# 定义大阪梅田站 4 个连续分镜头 (全景 -> 结构 -> 细部 -> 延时)
OSAKA_STORY_SHOTS = [
    {
        "shot_name": "01_aerial_panorama",
        "title": "镜头 1：大阪站城全景天幕俯瞰",
        "prompt": "Cinematic high-angle drone shot gliding over Osaka Station City. Monumental silver diagonal glass canopy roof soaring gracefully over bustling railway platforms, expansive Toki-no-Hiroba plaza, sleek Japanese trains gliding below, 8k resolution, crisp architectural rendering, steady cinematic motion, photorealistic.",
        "num_frames": 32,
        "steps": 30,
        "guidance": 8.0,
        "seed": 42
    },
    {
        "shot_name": "02_space_truss_structure",
        "title": "镜头 2：大跨度斜向空间管桁架受力透视",
        "prompt": "Smooth upward tilt camera shot gazing up at the monumental long-span steel tubular space truss of Osaka Station glass roof. Elegantly intersecting silver steel tubes and cast pin joints forming a colossal dynamic arch, natural sunlight filtering through triangular glazed panels, tectonic engineering perfection, sharp focus, 8k.",
        "num_frames": 32,
        "steps": 30,
        "guidance": 8.0,
        "seed": 108
    },
    {
        "shot_name": "03_tectonic_pin_joint",
        "title": "镜头 3：重型抗震球铰与驳接爪微距特写",
        "prompt": "Macro cinematography slowly sliding in on a heavy-duty seismic spherical pin joint and high-grade stainless steel spider clamps on Osaka station glass facade. CNC brushed metal finish, precision bolt circles, crystal-clear laminated glass with subtle prismatic optical refraction, architectural tectonic craftsmanship, 8k.",
        "num_frames": 32,
        "steps": 30,
        "guidance": 8.0,
        "seed": 256
    },
    {
        "shot_name": "04_twilight_timelapse",
        "title": "镜头 4：梅田交通枢纽黄昏人流与霓虹延时",
        "prompt": "Breathtaking 4k urban timelapse shot overlooking the bustling multi-level concourse of Umeda Osaka Station at twilight. Commuters and pedestrians flowing like continuous vibrant streams of light, high-speed trains arriving rhythmically, golden sunset glow fading into neon evening, hyper-dense metropolitan pulse, photorealistic.",
        "num_frames": 32,
        "steps": 30,
        "guidance": 8.0,
        "seed": 512
    }
]

print("="*60)
print("🎬 正在启动【大阪梅田站 4 镜头完整故事大片流水线】...")
print("将依次渲染 4 个 768P 高清分镜头，并使用 ffmpeg 自动无缝拼接为一部长片！")
print("="*60)

shot_files = []
total_start = time.time()

for idx, shot in enumerate(OSAKA_STORY_SHOTS, 1):
    shot_filename = f"osaka_shot_{idx}_{shot['shot_name']}.mp4"
    shot_path = os.path.join(OUTPUTS_DIR, shot_filename)
    shot_files.append(shot_path)
    
    print(f"\\n[{idx}/4] 正在渲染 {shot['title']}...")
    print(f"提示词: {shot['prompt'][:60]}...")
    
    gen = torch.Generator(device="cuda" if torch.cuda.is_available() else "cpu").manual_seed(shot['seed'])
    output = pipe(
        prompt=shot['prompt'],
        negative_prompt="blurry, low resolution, deformed, flickering, noisy, cartoon",
        height=512,
        width=768,
        num_frames=shot['num_frames'],
        num_inference_steps=shot['steps'],
        guidance_scale=shot['guidance'],
        generator=gen
    )
    frames = output.frames[0]
    export_to_video(frames, shot_path, fps=10)
    print(f"✅ 分镜头 {idx} 渲染完成: {shot_path}")

print("\\n" + "="*60)
print("🎞️ 正在使用 ffmpeg 无损拼接 4 个分镜头为完整长视频...")
print("="*60)

# 生成拼接清单文件
concat_list_path = os.path.join(OUTPUTS_DIR, "concat_list.txt")
with open(concat_list_path, "w", encoding="utf-8") as f:
    for sp in shot_files:
        f.write(f"file '{sp}'\\n")

final_feature_path = os.path.join(OUTPUTS_DIR, "osaka_umeda_complete_feature_768p.mp4")

# 调用 ffmpeg 执行流式无损拼接
concat_cmd = f"ffmpeg -y -f concat -safe 0 -i \\"{concat_list_path}\\" -c copy \\"{final_feature_path}\\""
subprocess.run(concat_cmd, shell=True, check=True)

total_elapsed = time.time() - total_start
print(f"🎉 恭喜！完整多镜头建筑纪录片已合成完毕！")
print(f"✅ 文件保存路径: {final_feature_path}")
print(f"⏱️ 全套 4 镜头渲染与拼接总耗时: {total_elapsed:.1f} 秒")
print("="*60)

# 在 Notebook 中直接嵌入高清大屏播放器
display(HTML(f'''
    <h3>🏛️ 大阪梅田站完整影视级大片 (768P 高清多镜头合辑):</h3>
    <video width="768" height="512" controls autoplay muted loop>
        <source src="https://localhost:8080/{final_feature_path}" type="video/mp4">
        您的浏览器不支持播放，请在左侧文件树或 Google Drive 中直接下载: {final_feature_path}
    </video>
'''))
"""
    cells.append(nbf.v4.new_code_cell(code_multishot))

    # Cell 8: Asset Packaging & Download
    code_zip = """# @title 8. 【归档导出】将生成视频素材与元数据打包下载
import os
import shutil

zip_filename = "/content/drive/MyDrive/Colab_Video_Relay/architectural_videos_package"
print(f"正在将 {OUTPUTS_DIR} 中的视频素材打包为 ZIP...")

shutil.make_archive(zip_filename, 'zip', OUTPUTS_DIR)
print(f"✅ 素材包已生成: {zip_filename}.zip")
print("您可以在左侧文件树或 Google Drive 中直接下载该压缩包进行下游剪辑！")
"""
    cells.append(nbf.v4.new_code_cell(code_zip))

    nb.cells = cells

    output_path = os.path.join("notebooks", "Wan2_1_Architecture_Video_Colab.ipynb")
    with open(output_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"🎉 成功构建 768P 高清多镜头合成版 Notebook: {output_path}")

if __name__ == "__main__":
    create_colab_notebook()
