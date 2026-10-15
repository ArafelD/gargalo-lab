"""Lab 01 - O mito do "enhance".

Ideia Feynman: uma foto pequena é um resumo. Dá para fazer resumo a partir da
foto grande, mas não dá para recuperar a foto grande a partir do resumo,
porque muitas fotos grandes diferentes geram o MESMO resumo.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

BOX = Image.Resampling.BOX
BICUBIC = Image.Resampling.BICUBIC
NEAREST = Image.Resampling.NEAREST


def make_scene(width: int = 320, height: int = 160, seed: int = 7) -> Image.Image:
    """Gera uma cena sintética (placa fictícia + listras finas) com ruído leve."""
    rng = np.random.default_rng(seed)
    img = Image.new("L", (width, height), 200)
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default(size=40)
    except TypeError:  # Pillow antigo
        font = ImageFont.load_default()
    d.rectangle([20, 30, width - 20, height - 30], outline=0, width=3)
    d.text((40, 55), "7K3-9Q2", fill=0, font=font)
    for x in range(30, width - 30, 4):
        d.line([(x, height - 26), (x, height - 14)], fill=0 if (x // 4) % 2 else 255)
    arr = np.asarray(img, dtype=np.int16) + rng.integers(-3, 4, size=(height, width))
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def downscale(img: Image.Image, factor: int) -> Image.Image:
    return img.resize((img.width // factor, img.height // factor), BOX)


def upscale(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    return img.resize(size, BICUBIC)


def psnr(a: Image.Image, b: Image.Image) -> float:
    x = np.asarray(a, dtype=np.float64)
    y = np.asarray(b, dtype=np.float64)
    mse = float(np.mean((x - y) ** 2))
    return float("inf") if mse == 0 else 10 * np.log10(255.0**2 / mse)


def high_freq_energy(img: Image.Image) -> float:
    """Fração da energia em frequências altas (detalhe fino = mudança rápida)."""
    arr = np.asarray(img, dtype=np.float64)
    arr = arr - arr.mean()
    spec = np.abs(np.fft.fftshift(np.fft.fft2(arr))) ** 2
    h, w = spec.shape
    yy, xx = np.ogrid[:h, :w]
    r = np.hypot((yy - h / 2) / (h / 2), (xx - w / 2) / (w / 2))
    total = spec.sum()
    return float(spec[r > 0.5].sum() / total) if total else 0.0


def collision_demo() -> dict:
    """Duas 'realidades' diferentes que viram exatamente a mesma foto pequena."""
    a = np.tile(np.array([[0, 255], [255, 0]], dtype=np.uint8), (4, 4))
    b = np.tile(np.array([[255, 0], [0, 255]], dtype=np.uint8), (4, 4))
    ia, ib = Image.fromarray(a), Image.fromarray(b)
    sa, sb = downscale(ia, 2), downscale(ib, 2)
    return {
        "originals_differ": not np.array_equal(a, b),
        "downscaled_identical": np.array_equal(np.asarray(sa), np.asarray(sb)),
    }


def run(out_dir: Path, factor: int = 8) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    orig = make_scene()
    low = downscale(orig, factor)
    up = upscale(low, orig.size)
    montage = Image.new("L", (orig.width * 3 + 20, orig.height), 255)
    montage.paste(orig, (0, 0))
    montage.paste(low.resize(orig.size, NEAREST), (orig.width + 10, 0))
    montage.paste(up, (orig.width * 2 + 20, 0))
    montage_path = out_dir / "01_enhance_montage.png"
    montage.save(montage_path)
    return {
        "factor": factor,
        "pixels_original": orig.width * orig.height,
        "pixels_lowres": low.width * low.height,
        "info_kept_pct": round(100 * (low.width * low.height) / (orig.width * orig.height), 2),
        "psnr_db_bicubic": round(psnr(orig, up), 2),
        "hf_energy_original": round(high_freq_energy(orig), 5),
        "hf_energy_upscaled": round(high_freq_energy(up), 5),
        "collision_demo": collision_demo(),
        "montage": str(montage_path),
    }
