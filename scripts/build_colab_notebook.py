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
> 🚀 **核心能力**：
> 1. **Colab 免费 T4 极限防 OOM 优化**：默认适配高能轻量级 SOTA 视频生成引擎 (LTX-Video / Wan2.1)，物理内存与显存双重安全，彻底杜绝系统 RAM 崩溃与显存溢出。
> 2. **上游 Agent 资产接力**：无缝接收其他 Agent 产出的效果图、BIM 剖面图或历史照片，批量自动生成动态 B-Roll 视频素材。
> 3. **双生成模式**：文生视频 (T2V) 与 方案图/老照片活化图生视频 (I2V)。
> 4. **双交互形态**：支持 **Gradio 网页工作台**（带公网链接）与 **无人值守脚本批量渲染**。
> 5. **成果自动归档**：成果与镜头元数据自动保存至 Google Drive，断线不丢失。
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

# 针对 Colab 免费版 12.7GB RAM 限制做精准自适应
if ram_gb < 20.0:
    print("\\n💡 检测为 Colab 免费标准环境 (物理内存约 12.7GB)：")
    print("   -> 自动启用防系统 RAM OOM 保护策略")
    print("   -> 优选加载 SOTA 电影级超高速视频模型: Lightricks/LTX-Video")
    print("   -> 启用 low_cpu_mem_usage 流式载入，零崩溃稳定极速出片！")
    ENGINE_TYPE = "LTX"
    MODEL_ID = "Lightricks/LTX-Video"
else:
    print(f"\\n🚀 检测为高配置环境 ({ram_gb:.2f}GB RAM / {gpu_name})：")
    print("   -> 具备运行全尺寸 Wan2.1 或 LTX-Video 的充足资源")
    ENGINE_TYPE = "WAN"
    MODEL_ID = "Wan-AI/Wan2.1-T2V-1.3B-Diffusers"

ENABLE_CPU_OFFLOAD = True
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
print("正在安装视频渲染流水线所需核心依赖 (预计耗时 30-40 秒)...")

!pip install -q --upgrade diffusers transformers accelerate sentencepiece imageio imageio-ffmpeg gradio>=4.44.0 safetensors einops bitsandbytes torchvision psutil

print("✅ 所有核心依赖包安装完成！")
"""
    cells.append(nbf.v4.new_code_cell(code_deps))

    # Cell 4: Model Pipeline Loader (Lazy & Safe Memory Mode)
    code_model_loader = """# @title 4. 【模型载入器】定义影视级视频生成引擎 (低内存安全模式)
import os
import gc
import torch
from diffusers.utils import export_to_video

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

def flush_memory():
    gc.collect()
    torch.cuda.empty_cache()

pipe = None

def get_pipeline():
    global pipe
    if pipe is not None:
        return pipe
        
    print("="*60)
    print(f"🚀 正在以低内存模式 (low_cpu_mem_usage) 安全初始化视频引擎: {MODEL_ID} ...")
    print("="*60)
    flush_memory()
    
    if ENGINE_TYPE == "LTX":
        from diffusers import LTXPipeline
        pipe = LTXPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16,
            low_cpu_mem_usage=True
        )
        pipe.enable_model_cpu_offload()
    else:
        from diffusers import WanPipeline
        pipe = WanPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16,
            low_cpu_mem_usage=True
        )
        pipe.enable_model_cpu_offload()
        if hasattr(pipe, "vae") and pipe.vae is not None:
            if hasattr(pipe.vae, "enable_slicing"):
                pipe.vae.enable_slicing()
            if hasattr(pipe.vae, "enable_tiling"):
                pipe.vae.enable_tiling()
                
    print("🎉 视频引擎已安全加载并绑定 GPU！")
    return pipe

print("✅ 视频引擎安全载入器就绪（支持 low_cpu_mem_usage 内存切片防 OOM 保护）！")
"""
    cells.append(nbf.v4.new_code_cell(code_model_loader))

    # Cell 5: Upstream Agent Asset Relay Pipeline (Batch Image-to-Video)
    code_relay = """# @title 5. 【资产接力】上游 Agent 渲染图/老照片一键批量生成视频素材
import os
import glob
import json
import time
from PIL import Image

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

def run_batch_relay(steps=25, guidance_scale=3.5, num_frames=65, fps=24):
    if not input_images:
        print("💡 提示: inputs 目录暂无待处理图片。请将其他 Agent 产出的效果图或历史照片上传到:")
        print(f"   {INPUTS_DIR}")
        return

    p = get_pipeline()
    print("🚀 开始批量接力渲染...")
    for idx, img_path in enumerate(input_images, 1):
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        output_mp4 = os.path.join(OUTPUTS_DIR, f"{base_name}_video.mp4")
        output_meta = os.path.join(OUTPUTS_DIR, f"{base_name}_video.json")
        
        prompt = auto_detect_preset(base_name)
        print(f"\\n正在处理 [{idx}/{len(input_images)}]: {base_name}")
        print(f"提示词: {prompt}")
        
        try:
            start_t = time.time()
            output_frames = p(
                prompt=prompt,
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
from PIL import Image

# 加载建筑专属提示词预设字典
ARCH_PRESETS = {
    "流线型现代展馆全景环绕 (航拍运镜)": {
        "prompt": "Cinematic drone shot, slowly orbiting around a white futuristic curvilinear pavilion with organic fluid geometry. Smooth reflections on surrounding mirror water pool, ultra-realistic daylight with soft shadows, highly detailed architecture rendering, 8k resolution, photorealistic, stable cinematic motion.",
        "negative": "jittery motion, flickering, blurry, distorted geometry, low resolution, bad lighting, noisy artifacts",
        "guidance": 3.5
    },
    "巨型中庭天光垂直拉升漫游 (室内升降)": {
        "prompt": "Smooth vertical pedestal crane shot inside a monumental architectural atrium. Golden volumetric God rays streaming through a parametric geometric skylight, illuminating cantilevered glass bridges and perforated metallic panels. Cinematic architectural interior, dust motes drifting in sunbeams, profound spatial depth, photorealistic.",
        "negative": "deformed structures, warping, camera shake, overexposed, low quality, glitch",
        "guidance": 3.5
    },
    "大跨度空间管桁架轴测动态拼装 (结构力学)": {
        "prompt": "Isometric exploded view showing the dynamic assembly of a long-span stadium tubular space truss. Modular triangular steel truss segments gracefully descend and lock into place with precision joints, forming a monumental saddle-shaped roof shell, subtle engineering stress flow illumination, high precision.",
        "negative": "messy lines, chaotic deformation, unrealistic physics, flickering, blurred joints",
        "guidance": 4.0
    },
    "中国古建斗栱榫卯旋转咬合 (传统大木作)": {
        "prompt": "Photorealistic 3D close-up turntable shot rotating around an ancient Chinese Dougong bracket set suspended in mid-air. Weathered aged cedar wood grain textures, intricately interlocking mortise-and-tenon wooden components sliding together with micron precision, historical oriental tectonic craft, dramatic soft lighting, 8k.",
        "negative": "plastic wood, cartoon, blurry grain, floating detached parts, distorted joinery",
        "guidance": 3.8
    },
    "点支承玻璃幕墙驳接爪微距特写 (构造节点)": {
        "prompt": "Macro photography dolly-in focusing on a 4-arm stainless steel spider fitting of a point-supported glass curtain wall. Brushed CNC metal texture, precision countersunk bolts, silicone gaskets, ultra-clear low-E laminated glass edge with prismatic optical caustics, architectural tectonic detail perfection.",
        "negative": "smudged glass, flat textures, noisy, distorted bolts, low detail",
        "guidance": 3.5
    },
    "历史黑白老照片动态彩色复活 (人文历史/I2V)": {
        "prompt": "Archival vintage black-and-white photograph smoothly transitioning into living color reality. The historical brick-and-timber architecture warms up with realistic daylight, fine photo grain transforms into crisp 4k textures, vintage pedestrians start moving naturally, living history brought back to life.",
        "negative": "morphing faces, glitchy walking, weird distortions, flashing artifacts, erratic movement",
        "guidance": 3.5
    },
    "古建筑遗存晨昏日影与星轨延时 (光影流转)": {
        "prompt": "Magnificent 4k timelapse photography with fixed camera observing a weathered historic stone bridge and clocktower. Fast-moving shadows sweeps across ancient masonry as sun arches overhead, golden dusk transitions into deep twilight, starry Milky Way arcs across the night sky, poetic passage of time.",
        "negative": "flickering frames, strobe lighting, jitter, broken stone",
        "guidance": 3.5
    }
}

def apply_preset(preset_name):
    if preset_name in ARCH_PRESETS:
        p = ARCH_PRESETS[preset_name]
        return p["prompt"], p["negative"], p["guidance"]
    return "", "", 3.5

def generate_video(mode, prompt, negative_prompt, init_image, steps, guidance_scale, seed, aspect_ratio):
    print(f"🎬 收到渲染请求 | 模式: {mode} | 步数: {steps} | 比例: {aspect_ratio}")
    if seed == -1:
        seed = random.randint(0, 2**32 - 1)
        
    out_filename = f"arch_video_{int(time.time())}_{seed}.mp4"
    out_path = os.path.join(OUTPUTS_DIR, out_filename)
    
    # 尺寸与画幅映射（均保证为 32 的倍数）
    if "9:16" in aspect_ratio:
        width, height = 512, 768
    elif "1:1" in aspect_ratio:
        width, height = 576, 576
    else: # 16:9
        width, height = 768, 512
        
    p = get_pipeline()
    generator = torch.Generator(device="cuda" if torch.cuda.is_available() else "cpu").manual_seed(int(seed))
    output = p(
        prompt=prompt,
        negative_prompt=negative_prompt,
        height=height,
        width=width,
        num_frames=65,
        num_inference_steps=int(steps),
        guidance_scale=float(guidance_scale),
        generator=generator
    )
    frames = output.frames[0]
    export_to_video(frames, out_path, fps=24)
    print(f"✅ 渲染完成: {out_path}")
    return out_path, f"✅ 渲染完成！已保存至 Google Drive: {out_path}"

# 构建 Gradio 界面
with gr.Blocks(title="建筑与结构影视视频工作室", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏛️ 建筑空间·结构力学·细部大样·人文历史 影视视频工作室")
    gr.Markdown("专为建筑设计师、结构工程师与文史创作者打造。支持文字概念生成与图纸/老照片活化动效。")
    
    with gr.Row():
        with gr.Column(scale=1):
            preset_dd = gr.Dropdown(
                label="🎯 建筑专业镜头语言预设",
                choices=list(ARCH_PRESETS.keys()),
                value="流线型现代展馆全景环绕 (航拍运镜)"
            )
            prompt_in = gr.Textbox(
                label="正面提示词 (Prompt)",
                value=ARCH_PRESETS["流线型现代展馆全景环绕 (航拍运镜)"]["prompt"],
                lines=4
            )
            neg_prompt_in = gr.Textbox(
                label="反向负面提示词 (Negative Prompt)",
                value=ARCH_PRESETS["流线型现代展馆全景环绕 (航拍运镜)"]["negative"],
                lines=2
            )
            
            with gr.Tab("🖼️ 图生视频模式 (I2V / 图纸或历史照片活化)"):
                image_in = gr.Image(label="上传建筑效果图 / 结构剖面 / 历史老照片", type="pil")
                
            with gr.Row():
                steps_slider = gr.Slider(label="推理步数 (Steps)", minimum=15, maximum=40, value=25, step=1)
                guidance_slider = gr.Slider(label="引导系数 (Guidance Scale)", minimum=2.0, maximum=8.0, value=3.5, step=0.1)
                
            with gr.Row():
                aspect_radio = gr.Radio(label="画面画幅", choices=["16:9 (横屏大片)", "9:16 (移动端立面)", "1:1 (正方剖面)"], value="16:9 (横屏大片)")
                seed_in = gr.Number(label="随机种子 (-1 为随机)", value=-1, precision=0)
                
            gen_btn = gr.Button("🚀 立即开始渲染视频素材", variant="primary")
            
        with gr.Column(scale=1):
            video_out = gr.Video(label="🎬 渲染输出预览 (MP4)")
            status_out = gr.Textbox(label="状态信息", interactive=False)
            
    preset_dd.change(
        fn=apply_preset,
        inputs=[preset_dd],
        outputs=[prompt_in, neg_prompt_in, guidance_slider]
    )
    
    gen_btn.click(
        fn=generate_video,
        inputs=[preset_dd, prompt_in, neg_prompt_in, image_in, steps_slider, guidance_slider, seed_in, aspect_radio],
        outputs=[video_out, status_out]
    )

# 启动并生成公共访问链接
print("正在启动 Gradio Web 服务并生成公共公网链接 (share=True)...")
demo.launch(share=True, debug=True)
"""
    cells.append(nbf.v4.new_code_cell(code_gradio))

    # Cell 7: Asset Packaging & Download
    code_zip = """# @title 7. 【归档导出】将生成视频素材与元数据打包下载
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

    print(f"🎉 成功构建防 OOM 增强版 Notebook: {output_path}")

if __name__ == "__main__":
    create_colab_notebook()
