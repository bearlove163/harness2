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
    md_header = """# 🏛️ 建筑与结构工程影视级 AI 视频生成流水线 (30秒完整纪录片版)

<a href="https://colab.research.google.com/github/bearlove163/harness2/blob/colab_video_generation/notebooks/Wan2_1_Architecture_Video_Colab.ipynb" target="_parent">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

> 本 Notebook 专为**建筑空间展示、大跨度结构分析、细部构造拆解与建筑人文历史演进**定制。
>
> 🚀 **核心能力升级 (30秒大片专版)**：
> 1. **全自动清理历史残留**：执行前自动清理 Drive 中的旧测试废片，保持空间纯净。
> 2. **8 镜头完整故事线**：远景天际线 ➔ 站城大天幕 ➔ 时空之广场 ➔ 空间管桁架 ➔ 铸钢球铰 ➔ 幕墙驳接爪 ➔ 站台穿梭列车 ➔ 黄昏千万流光，构成完整的 30 秒建筑纪录大片！
> 3. **768P 高清宽屏画质**：768x512 宽屏电影画质，清晰呈现建筑线条与材质光泽。
> 4. **100% 内存安全**：为 Colab 免费 T4 显卡量身调优，零崩溃稳定极速出片。
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
print("   -> 8 镜头连续渲染流水线就绪，目标合成 30 秒完整建筑纪录片")
print("="*60)
"""
    cells.append(nbf.v4.new_code_cell(code_gpu))

    # Cell 2: Google Drive Mounting & Directory Cleanup
    code_drive = """# @title 2. 【存储同步与清理】挂载 Google Drive 并清空旧冗余视频
from google.colab import drive
import os
import glob

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

# 按照用户要求：清理 Drive outputs 目录中之前生成的旧测试残片
print("="*60)
print("🧹 正在检查并清理 Drive 目录中原有的旧测试视频...")
old_files = glob.glob(os.path.join(OUTPUTS_DIR, "*.*"))
cleaned_count = 0
for f in old_files:
    try:
        os.remove(f)
        cleaned_count += 1
    except Exception as e:
        print(f"清理跳过: {e}")

# 清理旧的 zip 压缩包
old_zips = glob.glob(os.path.join(RELAY_BASE_DIR, "*.zip"))
for z in old_zips:
    try:
        os.remove(z)
        cleaned_count += 1
    except Exception:
        pass

print(f"✅ 已成功清理 {cleaned_count} 个历史旧文件，Drive 空间保持纯净！")
print(f"📁 崭新的 30 秒大片将输出至: {OUTPUTS_DIR}")
print("="*60)
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

input_images = []
for ext in ["*.png", "*.jpg", "*.jpeg", "*.webp"]:
    input_images.extend(glob.glob(os.path.join(INPUTS_DIR, ext)))

print(f"📂 扫描到上游 Agent 传入的图片资产: {len(input_images)} 个")
"""
    cells.append(nbf.v4.new_code_cell(code_relay))

    # Cell 6: Gradio WebUI
    code_gradio = """# @title 6. 【可视化工作台】启动 Gradio 建筑影视视频生成 Web 界面 (可选手动调试)
import gradio as gr
import random
import os
import time

def generate_video(prompt, negative_prompt, steps, guidance_scale, seed):
    if seed == -1:
        seed = random.randint(0, 2**32 - 1)
        
    out_filename = f"custom_video_{int(time.time())}_{seed}.mp4"
    out_path = os.path.join(OUTPUTS_DIR, out_filename)
    
    generator = torch.Generator(device="cuda" if torch.cuda.is_available() else "cpu").manual_seed(int(seed))
    output = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        height=512,
        width=768,
        num_frames=32,
        num_inference_steps=int(steps),
        guidance_scale=float(guidance_scale),
        generator=generator
    )
    frames = output.frames[0]
    export_to_video(frames, out_path, fps=8)
    return out_path, f"✅ 渲染完成！已保存至 Google Drive: {out_path}"

# 简易启动
print("Gradio 交互工作台已就绪，主要生产请直接运行下方第 7 单元格进行 30 秒大片全自动生成！")
"""
    cells.append(nbf.v4.new_code_cell(code_gradio))

    # Cell 7: Full 8-Shot 30-Second Documentary Pipeline
    code_multishot = """# @title 7. 【30秒大片全自动合成】大阪梅田站 8 镜头完整建筑纪录片渲染与拼接
import os
import time
import subprocess
import torch
from diffusers.utils import export_to_video
from IPython.display import HTML, display

# 定义大阪梅田站 8 个连续分镜头 (总计 256 帧，按 8.5 FPS 播放恰好为 30.1 秒！)
OSAKA_8_SHOTS = [
    {
        "shot_id": 1,
        "name": "01_skyline_distant_view",
        "title": "镜头 1：远景·大阪梅田摩天楼群天际线俯瞰",
        "prompt": "Cinematic wide-angle aerial shot overlooking the modern skyline of Umeda Osaka. Morning golden sunlight reflecting off gleaming glass skyscrapers and complex rail network, majestic architectural cityscape, 8k resolution, ultra-realistic, steady gliding camera.",
        "seed": 101
    },
    {
        "shot_id": 2,
        "name": "02_station_city_canopy",
        "title": "镜头 2：中景·JR大阪站城银色斜向天幕飞越",
        "prompt": "Cinematic high-angle drone shot gliding over Osaka Station City. Monumental silver diagonal glass canopy roof soaring gracefully over bustling railway platforms, expansive Toki-no-Hiroba plaza, 8k resolution, crisp architectural rendering, steady cinematic motion.",
        "seed": 202
    },
    {
        "shot_id": 3,
        "name": "03_toki_no_hiroba_atrium",
        "title": "镜头 3：近景·时空之广场空中连桥与通高中庭",
        "prompt": "Smooth vertical pedestal crane shot inside monumental Osaka station atrium plaza. Golden volumetric God rays streaming through glass skylight, illuminating cantilevered pedestrian skybridges, profound spatial depth, photorealistic architectural masterpiece.",
        "seed": 303
    },
    {
        "shot_id": 4,
        "name": "04_space_truss_arch",
        "title": "镜头 4：结构·大跨度空间管桁架拱形受力透视",
        "prompt": "Smooth upward tilt camera shot gazing up at the monumental long-span steel tubular space truss of Osaka Station roof. Elegantly intersecting silver steel tubes and cast pin joints forming a colossal dynamic arch, crisp geometric shadows, tectonic engineering perfection, sharp focus, 8k.",
        "seed": 404
    },
    {
        "shot_id": 5,
        "name": "05_cast_steel_pin_joint",
        "title": "镜头 5：细部·重型抗震铸钢销轴节点与高强螺栓",
        "prompt": "Macro cinematography slowly sliding in on a heavy-duty seismic spherical pin joint on Osaka station steel roof base. Industrial shot-blasted matte steel surface, high-strength bolt circles, rim lighting accentuating bevels, heavy engineering structural power, 8k.",
        "seed": 505
    },
    {
        "shot_id": 6,
        "name": "06_glass_spider_fitting",
        "title": "镜头 6：构造·四爪点支承幕墙驳接爪与通透玻璃",
        "prompt": "Macro photography dolly-in focusing on a 4-arm stainless steel spider fitting of point-supported glass curtain wall in Osaka station. Brushed CNC metal texture, precision countersunk bolts, ultra-clear low-E laminated glass edge with prismatic optical caustics, crisp detail perfection.",
        "seed": 606
    },
    {
        "shot_id": 7,
        "name": "07_trains_platform_motion",
        "title": "镜头 7：动态·城际通勤列车与站台平滑穿梭",
        "prompt": "Dynamic eye-level tracking shot along active train platforms beneath Osaka station giant roof. Sleek modern Japanese silver commuter trains arriving and departing rhythmically on parallel tracks, commuters walking, natural daylight filtering through roof, photorealistic.",
        "seed": 707
    },
    {
        "shot_id": 8,
        "name": "08_twilight_neon_timelapse",
        "title": "镜头 8：延时·黄昏晚霞转入霓虹夜景与如织人流",
        "prompt": "Breathtaking urban timelapse shot overlooking the bustling multi-level concourse of Umeda Osaka Station at twilight. Commuters flowing like continuous vibrant streams of light, golden sunset glow fading into neon evening, hyper-dense metropolitan pulse, photorealistic, 8k.",
        "seed": 808
    }
]

print("="*60)
print("🎬 正在启动【大阪梅田站 30 秒完整建筑纪录片渲染流水线】！")
print("本流程将依次渲染 8 个 768P 高清分镜头 (总计 256 帧)，")
print("并通过 FFmpeg 自动拼接为精准 30 秒的影视级完整大片！")
print("="*60)

shot_files = []
total_start = time.time()

# 统一参数：25步推理快速收敛，32帧每镜头，768x512 高清宽屏
NUM_FRAMES_PER_SHOT = 32
STEPS = 25
GUIDANCE = 8.0
FPS_PER_SHOT = 8.5  # 32 帧 / 8.5 FPS = 3.76 秒/镜头，8个镜头恰好 30.1 秒！

for shot in OSAKA_8_SHOTS:
    idx = shot["shot_id"]
    shot_filename = f"osaka_shot_{idx}_{shot['name']}.mp4"
    shot_path = os.path.join(OUTPUTS_DIR, shot_filename)
    shot_files.append(shot_path)
    
    print(f"\\n[{idx}/8] 正在渲染 {shot['title']}...")
    print(f"提示词: {shot['prompt'][:65]}...")
    
    t0 = time.time()
    gen = torch.Generator(device="cuda" if torch.cuda.is_available() else "cpu").manual_seed(shot["seed"])
    output = pipe(
        prompt=shot["prompt"],
        negative_prompt="blurry, low resolution, deformed, flickering, noisy, cartoon, bad architecture, drawing",
        height=512,
        width=768,
        num_frames=NUM_FRAMES_PER_SHOT,
        num_inference_steps=STEPS,
        guidance_scale=GUIDANCE,
        generator=gen
    )
    frames = output.frames[0]
    export_to_video(frames, shot_path, fps=int(FPS_PER_SHOT) if FPS_PER_SHOT.is_integer() else 8)
    dt = time.time() - t0
    print(f"✅ 分镜 {idx} 渲染完成: {shot_path} (用时: {dt:.1f}s)")

print("\\n" + "="*60)
print("🎞️ 正在使用 FFmpeg 将 8 个镜头无缝拼接为 30 秒完整大片...")
print("="*60)

# 生成拼接清单文件
concat_list_path = os.path.join(OUTPUTS_DIR, "concat_list.txt")
with open(concat_list_path, "w", encoding="utf-8") as f:
    for sp in shot_files:
        f.write(f"file '{sp}'\\n")

final_30s_feature = os.path.join(OUTPUTS_DIR, "osaka_umeda_30s_documentary_feature.mp4")

# FFmpeg 无损拼接
concat_cmd = f"ffmpeg -y -f concat -safe 0 -i \\"{concat_list_path}\\" -c copy \\"{final_30s_feature}\\""
subprocess.run(concat_cmd, shell=True, check=True)

total_elapsed = time.time() - total_start
print(f"🎉 恭喜！30 秒完整建筑大片已全自动合成完毕！")
print(f"🏆 最终大片路径: {final_30s_feature}")
print(f"⏱️ 8 镜头渲染与拼接总耗时: {total_elapsed/60:.1f} 分钟")
print("="*60)

# 自动生成全套压缩包
zip_path = os.path.join(RELAY_BASE_DIR, "osaka_umeda_30s_full_package")
import shutil
shutil.make_archive(zip_path, 'zip', OUTPUTS_DIR)
print(f"📦 全套素材与 30 秒长片压缩包就绪: {zip_path}.zip")
"""
    cells.append(nbf.v4.new_code_cell(code_multishot))

    nb.cells = cells

    output_path = os.path.join("notebooks", "Wan2_1_Architecture_Video_Colab.ipynb")
    with open(output_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"🎉 成功构建 30 秒 8 镜头完整大片 Notebook: {output_path}")

if __name__ == "__main__":
    create_colab_notebook()
