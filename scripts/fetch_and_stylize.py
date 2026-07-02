#!/usr/bin/env python3
"""Download Chrysler Australia brochure images and create stylized timeline art."""

import json
import re
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "assets" / "source"
STYLIZED_DIR = ROOT / "assets" / "models"
ATTRIBUTIONS_FILE = ROOT / "assets" / "attributions.json"

ARCHIVE_BASE = "https://www.oldcarbrochures.org/Australia/Chrysler/Chrysler/"
ARCHIVE_INDEX = "https://www.oldcarbrochures.org/Australia/Chrysler/Chrysler/index.html"
USER_AGENT = "ValiantSite/1.0 (educational tribute; github.com/70vgval/valiant-site)"

OUTPUT_SIZE = (520, 293)  # 16:9
MAX_SOURCE_WIDTH = 1400

# crop_box: optional relative (left, top, right, bottom) fractions to isolate car art
MODELS = [
    {
        "id": "rv1",
        "brochure": "1962 Chrysler Valiant RV1",
        "image": "1962_Valiant_RV1-01.jpg",
        "crop_box": (0.0, 0.0, 1.0, 0.82),
    },
    {
        "id": "sv1",
        "brochure": "1962-Chrysler-SV1-Valiant-Brochure",
        "image": "1962_Chrysler_Valiant_SV1-01.jpg",
        "crop_box": (0.0, 0.0, 1.0, 0.82),
    },
    {
        "id": "ap5",
        "brochure": "1963 Valiant AP5 - Australia",
        "image": "1963 Valiant AP5 - Australia page_02.jpg",
        "crop_box": (0.0, 0.05, 0.62, 0.88),
    },
    {
        "id": "ap6",
        "brochure": "1965-Chrysler-AP6-Valiant-Brochure",
        "image": "%21965_Chrysler_AP6_Valiant-01.jpg",
        "raw_image": True,
        "crop_box": (0.0, 0.0, 1.0, 0.85),
    },
    {
        "id": "vc",
        "brochure": "1966 Valiant VC - Australia",
        "image": "1966 Valiant VC - Australia page_01.jpg",
        "crop_box": (0.0, 0.0, 1.0, 0.85),
    },
    {
        "id": "ve",
        "brochure": "1967 Valiant VE - Australia",
        "image": "1967 Valiant VE - Australia page_01_12.jpg",
        "crop_box": (0.0, 0.0, 1.0, 0.85),
    },
    {
        "id": "vf",
        "brochure": "1969 Valiant VF - Australia",
        "image": "1969 Valiant VF - Australia page_01.jpg",
        "crop_box": (0.0, 0.0, 1.0, 0.85),
    },
    {
        "id": "vg",
        "brochure": "1970 Chrysler VG Valiant - Australia",
        "image": "1970 Chrysler VG Valiant-01.jpg",
        "crop_box": (0.0, 0.0, 1.0, 0.85),
    },
    {
        "id": "vh",
        "brochure": "1971 Valiant VH Charger - Australia",
        "image": "1971 Valiant VH Charger - Australia page_01.jpg",
        "crop_box": (0.0, 0.08, 1.0, 0.92),
    },
    {
        "id": "vj",
        "brochure": "1973 Valiant VJ Charger - Australia",
        "image": "1973 Valiant VJ Charger - Australia page_01.jpg",
        "crop_box": (0.0, 0.0, 1.0, 0.88),
    },
    {
        "id": "vk",
        "brochure": "1975-Chrysler-VK-Charger-Brochure",
        "image": "1975_Chrysler_VK_Charger-01.jpg",
        "crop_box": (0.0, 0.0, 1.0, 0.85),
    },
    {
        "id": "cl",
        "brochure": "1976-Chrysler-CL-Valiant-Sedan-Brochure",
        "image": "1976_Chrysler_CL_Valiant_Sedan-01.jpg",
        "crop_box": (0.0, 0.0, 1.0, 0.85),
    },
    {
        "id": "cm",
        "brochure": "1978 Chrysler CM Valiant _ Regal (Aus)",
        "image": "1978 Chrysler CM Regal _ Valiant (Aus)-02.jpg",
        "crop_box": (0.0, 0.08, 0.68, 0.9),
    },
    {
        "id": "chrysler-by-chrysler",
        "brochure": "1971-Chrysler-CH-Brochure-Rev",
        "image": "1971_Chrysler_CH_Rev-01-02-03.jpg",
        "crop_box": (0.52, 0.05, 0.98, 0.88),
    },
]


def brochure_url(folder: str, image: str, raw_image: bool = False) -> str:
    from urllib.parse import quote

    folder_part = quote(folder)
    image_part = image if raw_image else quote(image)
    return f"{ARCHIVE_BASE}{folder_part}/{image_part}"


def brochure_page_url(folder: str) -> str:
    from urllib.parse import quote

    return f"{ARCHIVE_BASE}{quote(folder)}/index.html"


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as resp:
        dest.write_bytes(resp.read())


def apply_relative_crop(img: Image.Image, crop_box: tuple[float, float, float, float]) -> Image.Image:
    w, h = img.size
    left, top, right, bottom = crop_box
    return img.crop((int(w * left), int(h * top), int(w * right), int(h * bottom)))


def trim_near_white_borders(img: Image.Image, threshold: int = 245) -> Image.Image:
    gray = img.convert("L")
    mask = gray.point(lambda p: 255 if p < threshold else 0)
    bbox = mask.getbbox()
    if not bbox:
        return img
    return img.crop(bbox)


def crop_center_16_9(img: Image.Image) -> Image.Image:
    w, h = img.size
    target_ratio = 16 / 9
    current_ratio = w / h
    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    new_h = int(w / target_ratio)
    top = (h - new_h) // 2
    return img.crop((0, top, w, top + new_h))


def build_brand_palette() -> Image.Image:
    colors = [
        (10, 10, 10),
        (255, 106, 0),
        (242, 194, 0),
        (245, 240, 230),
        (27, 79, 138),
        (45, 107, 58),
        (90, 90, 90),
        (200, 200, 200),
        (160, 90, 50),
        (120, 120, 120),
        (220, 180, 140),
        (60, 40, 30),
    ]
    palette = []
    for r, g, b in colors:
        palette.extend([r, g, b])
    palette.extend([0, 0, 0] * (256 - len(colors)))
    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette(palette)
    return pal_img


def stylize_brochure(img: Image.Image) -> Image.Image:
    """Lighter stylization that preserves period brochure character."""
    img = crop_center_16_9(img)
    img = img.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)

    img = img.filter(ImageFilter.MedianFilter(size=3))
    img = ImageOps.autocontrast(img, cutoff=1)
    img = ImageEnhance.Color(img).enhance(1.2)
    img = ImageEnhance.Contrast(img).enhance(1.25)
    img = ImageEnhance.Sharpness(img).enhance(1.1)

    # Gentle posterise — keeps brochure illustration quality
    img = img.quantize(colors=12, method=Image.Quantize.MEDIANCUT).convert("RGB")
    img = img.quantize(palette=build_brand_palette(), dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")

    tint = Image.new("RGB", OUTPUT_SIZE, (255, 106, 0))
    img = Image.blend(img, tint, alpha=0.04)

    return img


def prepare_source(img: Image.Image, crop_box: tuple[float, float, float, float] | None) -> Image.Image:
    if crop_box:
        img = apply_relative_crop(img, crop_box)
    img = trim_near_white_borders(img)
    if img.width > MAX_SOURCE_WIDTH:
        ratio = MAX_SOURCE_WIDTH / img.width
        img = img.resize((MAX_SOURCE_WIDTH, int(img.height * ratio)), Image.Resampling.LANCZOS)
    return img


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    STYLIZED_DIR.mkdir(parents=True, exist_ok=True)

    attributions = []

    for i, model in enumerate(MODELS):
        model_id = model["id"]
        source_path = SOURCE_DIR / f"{model_id}.jpg"
        output_path = STYLIZED_DIR / f"{model_id}.png"
        page_url = brochure_page_url(model["brochure"])
        image_url = brochure_url(model["brochure"], model["image"], model.get("raw_image", False))

        print(f"[{i + 1}/{len(MODELS)}] {model_id} ← {model['brochure']}")

        download(image_url, source_path)
        time.sleep(0.75)

        img = Image.open(source_path).convert("RGB")
        prepared = prepare_source(img, model.get("crop_box"))
        prepared.save(source_path, "JPEG", quality=88, optimize=True)

        styled = stylize_brochure(prepared)
        styled.save(output_path, "PNG", optimize=True)

        attributions.append({
            "id": model_id,
            "source_file": model["image"],
            "brochure": model["brochure"],
            "source_url": page_url,
            "image_url": image_url,
            "license": "Public domain / educational use (The Old Car Manual Project)",
            "artist": "Chrysler Australia / The Old Car Manual Project archive",
            "stylized": f"assets/models/{model_id}.png",
        })

    ATTRIBUTIONS_FILE.write_text(json.dumps(attributions, indent=2), encoding="utf-8")
    print(f"\nDone — {len(attributions)} brochure illustrations saved.")


if __name__ == "__main__":
    main()
