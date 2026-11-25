"""Generate Mandarin neural narration MP3s and warm ambient pad WAV for Remotion."""

import asyncio
import math
import os
import wave
import numpy as np

AUDIO_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "public",
    "audio",
)

NARRATIONS = [
    (
        "scene_01.mp3",
        "横跨铁道上空约百米，银色斜向玻璃天幕重塑了关西门户的天际线。",
    ),
    (
        "scene_02.mp3",
        "在不停运的繁忙铁道上方，巨型立体管桁架实现了无柱大跨度跨越。",
    ),
    (
        "scene_03.mp3",
        "精密铸钢球铰与不锈钢四爪驳接件，兼顾了抗震变形与通透采光。",
    ),
    (
        "scene_04.mp3",
        "日均承接数百万客流，让硬核钢构骨架升华为充满温度的城市客厅。",
    ),
]


async def synthesize_narrations() -> None:
    import edge_tts

    os.makedirs(AUDIO_DIR, exist_ok=True)
    voices = ["zh-CN-YunjianNeural", "zh-CN-YunxiNeural"]

    for filename, text in NARRATIONS:
        out_path = os.path.join(AUDIO_DIR, filename)
        last_err = None
        for voice in voices:
            try:
                comm = edge_tts.Communicate(text=text, voice=voice, rate="+5%")
                await comm.save(out_path)
                size_kb = os.path.getsize(out_path) / 1024.0
                if size_kb < 5.0:
                    raise RuntimeError(f"TTS file too small: {size_kb:.1f} KB")
                print(f"[TTS] Generated {filename} ({voice}, {size_kb:.1f} KB)")
                last_err = None
                break
            except Exception as err:
                last_err = err
                print(f"[TTS] Warning {voice} failed for {filename}: {err}")
        if last_err is not None:
            raise RuntimeError(f"All TTS voices failed for {filename}: {last_err}")


def generate_ambient_pad(duration_sec: float = 30.5, sample_rate: int = 44100) -> None:
    """Create a warm stereo Cmaj9 ambient pad WAV without clipping."""
    os.makedirs(AUDIO_DIR, exist_ok=True)
    out_path = os.path.join(AUDIO_DIR, "ambient_pad.wav")

    n_samples = int(duration_sec * sample_rate)
    t = np.linspace(0.0, duration_sec, n_samples, endpoint=False, dtype=np.float64)

    # Cmaj9 voicing (Hz) with gentle weights (warm low-mid focus)
    notes = [
        (130.81, 0.30, 0.25),  # C3
        (196.00, 0.24, 0.35),  # G3
        (246.94, 0.16, 0.45),  # B3
        (293.66, 0.14, 0.55),  # D4
        (329.63, 0.12, 0.65),  # E4
    ]

    left = np.zeros(n_samples, dtype=np.float64)
    right = np.zeros(n_samples, dtype=np.float64)

    for freq, amp, lfo_rate in notes:
        # Subtle breathing LFO + slight stereo detune for width
        lfo_l = 0.72 + 0.28 * np.sin(2.0 * math.pi * lfo_rate * t)
        lfo_r = 0.72 + 0.28 * np.sin(2.0 * math.pi * lfo_rate * t + 1.1)

        sig_l = np.sin(2.0 * math.pi * (freq - 0.35) * t) + 0.15 * np.sin(
            2.0 * math.pi * (freq * 2.0 - 0.35) * t
        )
        sig_r = np.sin(2.0 * math.pi * (freq + 0.35) * t) + 0.15 * np.sin(
            2.0 * math.pi * (freq * 2.0 + 0.35) * t
        )

        left += amp * lfo_l * sig_l
        right += amp * lfo_r * sig_r

    # Gentle 2.0s fade-in and 2.5s fade-out
    fade_in_samples = int(2.0 * sample_rate)
    fade_out_samples = int(2.5 * sample_rate)
    env = np.ones(n_samples, dtype=np.float64)
    env[:fade_in_samples] = np.linspace(0.0, 1.0, fade_in_samples)
    env[-fade_out_samples:] = np.linspace(1.0, 0.0, fade_out_samples)

    left *= env
    right *= env

    peak = max(float(np.max(np.abs(left))), float(np.max(np.abs(right))), 1e-6)
    scale = 0.32 / peak  # Clean headroom
    left_i16 = np.clip(left * scale * 32767.0, -32767, 32767).astype(np.int16)
    right_i16 = np.clip(right * scale * 32767.0, -32767, 32767).astype(np.int16)

    stereo = np.column_stack((left_i16, right_i16)).tobytes()
    with wave.open(out_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(stereo)

    size_kb = os.path.getsize(out_path) / 1024.0
    print(f"[Audio] Generated ambient_pad.wav ({duration_sec}s stereo, {size_kb:.1f} KB)")


def main() -> None:
    asyncio.run(synthesize_narrations())
    generate_ambient_pad()
    print("[Audio] All audio assets generated successfully.")


if __name__ == "__main__":
    main()
