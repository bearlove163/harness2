import os
import nbformat as nbf


def create_render_notebook():
    """Build the Colab SDXL + Remotion Keyframe Generator notebook."""
    os.makedirs("notebooks", exist_ok=True)
    nb = nbf.v4.new_notebook()

    nb.metadata = {
        "accelerator": "GPU",
        "colab": {
            "gpuType": "T4",
            "provenance": [],
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
        },
    }

    cells = []

    md_header = """# 🏛️ Antigravity × Colab 建筑工程 1080P 关键帧渲染工作站 (SDXL RealVisXL)

<a href="https://colab.research.google.com/github/bearlove163/harness2/blob/colab_video_generation/notebooks/Architecture_SDXL_Rendering_Colab.ipynb" target="_parent">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

> 本 Notebook 负责云端 GPU **高精细 16:9 建筑关键帧 (1344×768)** 生成与质检，供本地 **Antigravity + Remotion** 合成 1080P/30fps 电影级纪录长片。
>
> 🛡️ **严格执行安全与画质准则**：
> 1. **显式挂载 VAE (`madebyollin/sdxl-vae-fp16-fix`)**，彻底杜绝无 VAE 引起的模糊与黄雾。
> 2. **前置单帧极速抽检 (Cell 5 Sanity Check)**：仅渲染 1 张图，自动检验锐度与色彩后再批量生成 4 场景。
> 3. **非阻塞下载桥 (Cell 7)**：生成完成后通过 Gradio 公网链接暴露原图与 ZIP，方便本地一键拉取。
"""
    cells.append(nbf.v4.new_markdown_cell(md_header))

    # Cell 1: Hardware Check
    code_gpu = """# @title 1. 【硬件检测】检查 Colab GPU / VRAM 与系统内存
import os
import sys
import psutil
import torch

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

print("=" * 60)
print("正在检查当前 Google Colab 计算资源与 GPU 架构...")
print("=" * 60)

if not torch.cuda.is_available():
    raise SystemError("❌ 未检测到 GPU！请点击顶部菜单：代码执行程序 -> 更改运行时类型 -> 选择 'T4 GPU'！")

gpu_name = torch.cuda.get_device_name(0)
total_vram = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
ram_gb = psutil.virtual_memory().total / (1024 ** 3)

print(f"✅ GPU 型号:     {gpu_name}")
print(f"✅ GPU 显存总量: {total_vram:.2f} GB")
print(f"✅ 系统物理内存: {ram_gb:.2f} GB")
print("💡 单张 1344x768 关键帧约耗时 12~18 秒，全流程约 1.5 分钟，远低于配额风险阈值。")
print("=" * 60)
"""
    cells.append(nbf.v4.new_code_cell(code_gpu))

    # Cell 2: Google Drive Mount & Directory Setup
    code_drive = """# @title 2. 【存储同步】挂载 Google Drive 并初始化关键帧输出目录
from google.colab import drive
import os

print("正在挂载 Google Drive...")
drive.mount('/content/drive')

RENDER_BASE_DIR = "/content/drive/MyDrive/AI_Architecture_Renders"
OUTPUTS_DIR = os.path.join(RENDER_BASE_DIR, "osaka_remotion_keyframes")
INPUTS_DIR = os.path.join(RENDER_BASE_DIR, "inputs_cad_sketches")

for d in [RENDER_BASE_DIR, OUTPUTS_DIR, INPUTS_DIR]:
    os.makedirs(d, exist_ok=True)

print("✅ Google Drive 工作目录就绪:")
print(f"   🖼️ 关键帧输出目录: {OUTPUTS_DIR}")
print(f"   📥 CAD/草图输入目录: {INPUTS_DIR}")
"""
    cells.append(nbf.v4.new_code_cell(code_drive))

    # Cell 3: Fast Dependencies Install (single line for clean AST)
    code_deps = """# @title 3. 【依赖安装】安装 SDXL 与图像处理核心库
print("正在安装 SDXL 与图像处理核心依赖...")

!pip install -q --upgrade diffusers>=0.30.0 transformers>=4.40.0 accelerate>=0.30.0 controlnet-aux gradio>=4.44.0 safetensors torchvision opencv-python-headless invisible-watermark

print("✅ 所有核心依赖包安装完成！")
"""
    cells.append(nbf.v4.new_code_cell(code_deps))

    # Cell 4: Model Pipeline Loader (RealVisXL_V4.0 + explicit fp16-fix VAE + fallback)
    code_model_loader = """# @title 4. 【模型载入】加载 RealVisXL V4.0 与显式 sdxl-vae-fp16-fix 解码器
import gc
import torch
from diffusers import (
    AutoencoderKL,
    DPMSolverMultistepScheduler,
    StableDiffusionXLPipeline,
)


def flush_memory():
    gc.collect()
    torch.cuda.empty_cache()


flush_memory()
print("=" * 60)
print("🔧 正在显式加载高保真 VAE: madebyollin/sdxl-vae-fp16-fix ...")
vae = AutoencoderKL.from_pretrained(
    "madebyollin/sdxl-vae-fp16-fix",
    torch_dtype=torch.float16,
)

MODEL_ID = "SG161222/RealVisXL_V4.0"
try:
    print(f"🚀 正在载入写实建筑底模: {MODEL_ID} ...")
    pipe = StableDiffusionXLPipeline.from_pretrained(
        MODEL_ID,
        vae=vae,
        torch_dtype=torch.float16,
        use_safetensors=True,
    )
except Exception as err:
    print(f"⚠️ {MODEL_ID} 加载回退 ({err}) -> 使用 stabilityai/stable-diffusion-xl-base-1.0")
    MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
    pipe = StableDiffusionXLPipeline.from_pretrained(
        MODEL_ID,
        vae=vae,
        torch_dtype=torch.float16,
        variant="fp16",
        use_safetensors=True,
    )

pipe.scheduler = DPMSolverMultistepScheduler.from_config(
    pipe.scheduler.config,
    use_karras_sigmas=True,
)
pipe.enable_vae_slicing()
pipe.enable_vae_tiling()
pipe.enable_model_cpu_offload()

print(f"🎉 管线就绪 ({MODEL_ID} + sdxl-vae-fp16-fix)")
print("=" * 60)
"""
    cells.append(nbf.v4.new_code_cell(code_model_loader))

    # Cell 5: Sanity Check (Single Frame Only)
    code_sanity = """# @title 5. 【首片极速抽检 (Sanity Check)】仅渲染 1 张 1344x768 测试帧并质检 (约 15 秒)
import os
import time
import cv2
import numpy as np
import torch
from IPython.display import display

print("=" * 60)
print("🔍 执行强制 Sanity Check：仅渲染 1 张测试帧，检查清晰度与色彩后再批量生成...")
print("=" * 60)

SANITY_PROMPT = (
    "RAW architectural photograph of Osaka Station City diagonal silver glass canopy roof "
    "and white tubular steel space truss over railway platforms, crisp clear sky, "
    "sharp geometric structural steel members, photorealistic, 8k uhd, sharp focus"
)
NEG_PROMPT = (
    "blurry, fuzzy, foggy, hazy, yellow tint, washed out, overexposed, "
    "low resolution, bad architecture, distorted lines, cartoon, drawing, anime, painting, watermark, text"
)

t0 = time.time()
gen = torch.Generator(device="cuda").manual_seed(42)
sanity_img = pipe(
    prompt=SANITY_PROMPT,
    negative_prompt=NEG_PROMPT,
    width=1344,
    height=768,
    num_inference_steps=22,
    guidance_scale=7.0,
    generator=gen,
).images[0]
gpu_sec = time.time() - t0

sanity_path = os.path.join(OUTPUTS_DIR, "00_sanity_check.png")
sanity_img.save(sanity_path)

# 客观清晰度与色彩指标校验
img_bgr = cv2.imread(sanity_path)
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
lap_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
mean_sat = float(hsv[:, :, 1].mean())
b_mean, g_mean, r_mean = [float(x) for x in img_bgr.mean(axis=(0, 1))]

print(f"⏱️ 【显卡计算渲染耗时】: {gpu_sec:.1f} 秒")
print(f"📐 输出尺寸: {sanity_img.size[0]}x{sanity_img.size[1]}")
print(f"🔬 拉普拉斯清晰度方差 (Laplacian Var): {lap_var:.1f} (阈值 > 50)")
print(f"🎨 平均饱和度: {mean_sat:.1f} | 通道均值 RGB=({r_mean:.1f}, {g_mean:.1f}, {b_mean:.1f})")

if lap_var > 50.0 and r_mean > 15.0:
    print("✅ SANITY_CHECK_PASS: 清晰度与色彩正常，请人工确认下方预览图后运行 Cell 6！")
else:
    print("❌ SANITY_CHECK_FAIL: 画面异常模糊或过暗，请勿运行 Cell 6！")

display(sanity_img)
"""
    cells.append(nbf.v4.new_code_cell(code_sanity))

    # Cell 6: 4-Scene Widescreen Keyframes Batch
    code_batch = """# @title 6. 【4 场景 16:9 关键帧批量渲染】生成 1344x768 建筑高清关键帧并打包 (约 75 秒)
import os
import shutil
import time
import cv2
import torch

SCENES_SPEC = [
    {
        "filename": "scene_01_aerial_canopy.png",
        "seed": 101,
        "title": "01 / 宏观体量 - 巨型斜向天幕",
        "prompt": (
            "High-angle daylight architectural photography of Osaka Station City's monumental "
            "diagonal silver-and-glass canopy roof spanning across modern railway tracks and flanked by high-rise towers, "
            "crystal clear blue sky, sharp structural detail, photorealistic, 8k uhd, RAW photo"
        ),
    },
    {
        "filename": "scene_02_space_truss.png",
        "seed": 202,
        "title": "02 / 结构力学 - 大跨度空间钢管桁架",
        "prompt": (
            "Dramatic upward architectural photography inside Osaka Station's Toki-no-Hiroba concourse "
            "looking at the huge white tubular steel triangular space truss roof and inclined skylight glazing, "
            "dramatic geometric shadows, pedestrians on skybridge below, crisp ultra-sharp structural lines, 8k uhd, RAW photo"
        ),
    },
    {
        "filename": "scene_03_tectonic_joint.png",
        "seed": 303,
        "title": "03 / 细部构造 - 抗震节点与点支承幕墙",
        "prompt": (
            "Crisp architectural detail macro photograph of a heavy cast-steel seismic pin joint "
            "and brushed stainless-steel 4-arm spider fitting anchoring thick clear laminated glass curtain wall panels, "
            "precision bolts, natural grazing sunlight, tack-sharp engineering craftsmanship, 8k uhd, RAW photo"
        ),
    },
    {
        "filename": "scene_04_twilight_hub.png",
        "seed": 404,
        "title": "04 / 城市脉动 - 梅田立体交通枢纽蓝调时刻",
        "prompt": (
            "Blue-hour twilight architectural photograph of Umeda Osaka Station's multi-level illuminated glass concourse "
            "and gleaming commuter train platforms below, glowing warm interior lights contrasting deep indigo sky, "
            "sharp reflections, ultra-clear 8k architectural photography, RAW photo"
        ),
    },
]

NEG_PROMPT = (
    "blurry, fuzzy, foggy, hazy, yellow tint, washed out, overexposed, "
    "low resolution, bad architecture, distorted lines, cartoon, drawing, anime, painting, watermark, text"
)

generated_paths = []
total_gpu_sec = 0.0

print("=" * 60)
print("🎬 开始批量生成 4 张 1344x768 (16:9) 建筑高清关键帧...")
print("=" * 60)

for i, spec in enumerate(SCENES_SPEC, 1):
    t0 = time.time()
    gen = torch.Generator(device="cuda").manual_seed(spec["seed"])
    img = pipe(
        prompt=spec["prompt"],
        negative_prompt=NEG_PROMPT,
        width=1344,
        height=768,
        num_inference_steps=28,
        guidance_scale=7.0,
        generator=gen,
    ).images[0]
    dt = time.time() - t0
    total_gpu_sec += dt

    out_path = os.path.join(OUTPUTS_DIR, spec["filename"])
    img.save(out_path)
    generated_paths.append(out_path)

    img_bgr = cv2.imread(out_path)
    lap_var = float(cv2.Laplacian(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var())
    size_kb = os.path.getsize(out_path) / 1024.0
    print(f"[{i}/4] ✅ {spec['title']} | 耗时: {dt:.1f}s | 体积: {size_kb:.0f} KB | 清晰度: {lap_var:.1f}")

zip_base = os.path.join(OUTPUTS_DIR, "osaka_keyframes_1344x768")
zip_dir_tmp = os.path.join(OUTPUTS_DIR, "_zip_stage")
os.makedirs(zip_dir_tmp, exist_ok=True)
for p in generated_paths:
    shutil.copy2(p, os.path.join(zip_dir_tmp, os.path.basename(p)))
zip_path = shutil.make_archive(zip_base, "zip", zip_dir_tmp)
shutil.rmtree(zip_dir_tmp, ignore_errors=True)

print("=" * 60)
print(f"🎉 4 张高清关键帧全部完成！⏱️ 【显卡计算总耗时】: {total_gpu_sec:.1f} 秒")
print(f"📦 ZIP 打包文件: {zip_path}")
print("=" * 60)
"""
    cells.append(nbf.v4.new_code_cell(code_batch))

    # Cell 7: Gradio Download Bridge
    code_bridge = """# @title 7. 【下载桥梁】启动轻量 Gradio 画廊并暴露 HTTP 下载链接
import os
import gradio as gr

export_files = [
    os.path.join(OUTPUTS_DIR, name)
    for name in [
        "scene_01_aerial_canopy.png",
        "scene_02_space_truss.png",
        "scene_03_tectonic_joint.png",
        "scene_04_twilight_hub.png",
        "osaka_keyframes_1344x768.zip",
    ]
    if os.path.exists(os.path.join(OUTPUTS_DIR, name))
]

gallery_items = [
    (p, os.path.basename(p))
    for p in export_files
    if p.endswith(".png")
]

with gr.Blocks(title="Osaka Keyframes Download Bridge") as bridge_demo:
    gr.Markdown("# 🏛️ 大阪梅田站 1344×768 极清关键帧资产下载桥")
    gr.Gallery(value=gallery_items, label="4 张高清关键帧预览", columns=2, height="auto")
    gr.Files(value=export_files, label="点击文件即可下载原图 & ZIP")

_, local_url, share_url = bridge_demo.launch(
    share=True,
    prevent_thread_lock=False,
    allowed_paths=[OUTPUTS_DIR],
)

print("=" * 60)
print(f"GRADIO_PUBLIC_URL: {share_url}")
for p in export_files:
    print(f"DOWNLOAD_URL: {share_url}/gradio_api/file={p}")
print("=" * 60)
"""
    cells.append(nbf.v4.new_code_cell(code_bridge))

    # Cell 8: Optional ControlNet Studio (Guarded so it never blocks batch flow)
    code_controlnet_studio = """# @title 8. 【可选扩展】ControlNet 草图/CAD 精准锁线交互工作室
RUN_INTERACTIVE_STUDIO = False  # 如需交互式上传 CAD/草图渲染，请改为 True 后单独运行本单元格

if RUN_INTERACTIVE_STUDIO:
    import random
    import time
    import cv2
    import numpy as np
    import gradio as gr
    from PIL import Image
    from diffusers import ControlNetModel, StableDiffusionXLControlNetPipeline

    controlnet = ControlNetModel.from_pretrained(
        "diffusers/controlnet-canny-sdxl-1.0",
        torch_dtype=torch.float16,
    )
    pipe_cn = StableDiffusionXLControlNetPipeline.from_pipe(pipe, controlnet=controlnet)
    pipe_cn.enable_model_cpu_offload()

    def render_from_sketch(input_img, prompt, low_t, high_t, strength, steps, seed):
        if input_img is None:
            return None, None, "请先上传草图或 CAD 线稿"
        if seed == -1:
            seed = random.randint(0, 2**32 - 1)
        arr = np.array(input_img.convert("RGB").resize((1024, 1024), Image.LANCZOS))
        edges = cv2.Canny(arr, int(low_t), int(high_t))
        edge_img = Image.fromarray(np.stack([edges] * 3, axis=-1))
        gen = torch.Generator(device="cuda").manual_seed(int(seed))
        res = pipe_cn(
            prompt=prompt,
            image=edge_img,
            controlnet_conditioning_scale=float(strength),
            num_inference_steps=int(steps),
            guidance_scale=7.0,
            generator=gen,
        ).images[0]
        out_p = os.path.join(OUTPUTS_DIR, f"cad_render_{int(time.time())}.png")
        res.save(out_p)
        return edge_img, res, f"✅ 已保存: {out_p}"

    with gr.Blocks(title="SDXL ControlNet 建筑线稿工作室") as cn_demo:
        gr.Markdown("# ✍️ CAD / 草图 / 白模 ControlNet 结构锁线渲染")
        with gr.Row():
            with gr.Column():
                in_img = gr.Image(label="上传草图/CAD", type="pil")
                in_prompt = gr.Textbox(
                    label="Prompt",
                    value="Modern steel truss and glass architecture, crisp daylight, 8k raw architectural photo",
                )
                low_s = gr.Slider(10, 200, value=100, step=10, label="Canny Low")
                high_s = gr.Slider(50, 300, value=200, step=10, label="Canny High")
                str_s = gr.Slider(0.2, 1.5, value=0.9, step=0.05, label="锁线强度")
                step_s = gr.Slider(15, 35, value=25, step=1, label="步数")
                seed_n = gr.Number(value=-1, precision=0, label="Seed")
                btn = gr.Button("渲染", variant="primary")
            with gr.Column():
                edge_out = gr.Image(label="提取线条")
                img_out = gr.Image(label="效果图")
                msg_out = gr.Textbox(label="状态")
        btn.click(
            render_from_sketch,
            [in_img, in_prompt, low_s, high_s, str_s, step_s, seed_n],
            [edge_out, img_out, msg_out],
        )
    cn_demo.launch(share=True, allowed_paths=[OUTPUTS_DIR])
else:
    print("ℹ️ 可选交互工作室已跳过 (RUN_INTERACTIVE_STUDIO = False)。如需使用请改为 True。")
"""
    cells.append(nbf.v4.new_code_cell(code_controlnet_studio))

    nb.cells = cells

    out_path = os.path.join("notebooks", "Architecture_SDXL_Rendering_Colab.ipynb")
    with open(out_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"🎉 成功构建 Antigravity × Colab 关键帧工作站 Notebook: {out_path}")


if __name__ == "__main__":
    create_render_notebook()
