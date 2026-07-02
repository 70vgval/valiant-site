#!/usr/bin/env python3
"""Download Wikipedia Commons images and create stylized 2D representations."""

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

USER_AGENT = "ValiantSite/1.0 (educational tribute; contact: github.com/70vgval/valiant-site)"

MODELS = [
    {
        "id": "rv1",
        "filename": "Chrysler Valiant R Series (16972724246).jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Chrysler_Valiant_R_Series_%2816972724246%29.jpg/960px-Chrysler_Valiant_R_Series_%2816972724246%29.jpg",
        "license": "CC BY 2.0",
        "artist": "Jeremy (Flickr)",
        "source_url": "https://commons.wikimedia.org/wiki/File:Chrysler_Valiant_R_Series_(16972724246).jpg",
    },
    {
        "id": "sv1",
        "filename": "Chrysler Valiant S-Series (16330566121).jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Chrysler_Valiant_S-Series_%2816330566121%29.jpg/960px-Chrysler_Valiant_S-Series_%2816330566121%29.jpg",
        "license": "CC BY 2.0",
        "artist": "Jeremy (Flickr)",
        "source_url": "https://commons.wikimedia.org/wiki/File:Chrysler_Valiant_S-Series_(16330566121).jpg",
    },
    {
        "id": "ap5",
        "filename": "AP5 Valiant AP565.JPG",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/AP5_Valiant_AP565.JPG/960px-AP5_Valiant_AP565.JPG",
        "license": "CC BY-SA 4.0",
        "artist": "OSX",
        "source_url": "https://commons.wikimedia.org/wiki/File:AP5_Valiant_AP565.JPG",
    },
    {
        "id": "ap6",
        "filename": "1965 Valiant AP6 Standard==.JPG",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/1965_Valiant_AP6_Standard%3D%3D.JPG/960px-1965_Valiant_AP6_Standard%3D%3D.JPG",
        "license": "CC BY-SA 4.0",
        "artist": "Sicnag",
        "source_url": "https://commons.wikimedia.org/wiki/File:1965_Valiant_AP6_Standard==.JPG",
    },
    {
        "id": "vc",
        "filename": "1966 Valiant VC Standard -.JPG",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/1966_Valiant_VC_Standard_-.JPG/960px-1966_Valiant_VC_Standard_-.JPG",
        "license": "CC BY-SA 4.0",
        "artist": "Sicnag",
        "source_url": "https://commons.wikimedia.org/wiki/File:1966_Valiant_VC_Standard_-.JPG",
    },
    {
        "id": "ve",
        "filename": "1968 Valiant VE Standard==.JPG",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/1968_Valiant_VE_Standard%3D%3D.JPG/960px-1968_Valiant_VE_Standard%3D%3D.JPG",
        "license": "CC BY-SA 4.0",
        "artist": "Sicnag",
        "source_url": "https://commons.wikimedia.org/wiki/File:1968_Valiant_VE_Standard==.JPG",
    },
    {
        "id": "vf",
        "filename": "1969-1970 Chrysler Valiant (VF) Pacer 225 sedan (2015-11-13) 01.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/1969-1970_Chrysler_Valiant_%28VF%29_Pacer_225_sedan_%282015-11-13%29_01.jpg/960px-1969-1970_Chrysler_Valiant_%28VF%29_Pacer_225_sedan_%282015-11-13%29_01.jpg",
        "license": "Public domain",
        "artist": "OSX",
        "source_url": "https://commons.wikimedia.org/wiki/File:1969-1970_Chrysler_Valiant_(VF)_Pacer_225_sedan_(2015-11-13)_01.jpg",
    },
    {
        "id": "vg",
        "filename": "1971 Chrysler VG Valiant sedan (6109313978) (cropped).jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/1971_Chrysler_VG_Valiant_sedan_%286109313978%29_%28cropped%29.jpg/960px-1971_Chrysler_VG_Valiant_sedan_%286109313978%29_%28cropped%29.jpg",
        "license": "CC BY 2.0",
        "artist": "Jeremy (Flickr)",
        "source_url": "https://commons.wikimedia.org/wiki/File:1971_Chrysler_VG_Valiant_sedan_(6109313978)_(cropped).jpg",
    },
    {
        "id": "vh",
        "filename": "1972 Chrysler Valiant VH Charger XL.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/1972_Chrysler_Valiant_VH_Charger_XL.jpg/960px-1972_Chrysler_Valiant_VH_Charger_XL.jpg",
        "license": "CC BY 2.0",
        "artist": "Sicnag (Flickr)",
        "source_url": "https://commons.wikimedia.org/wiki/File:1972_Chrysler_Valiant_VH_Charger_XL.jpg",
    },
    {
        "id": "vj",
        "filename": "Chrysler Valiant VJ Charger (16950622926).jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Chrysler_Valiant_VJ_Charger_%2816950622926%29.jpg/960px-Chrysler_Valiant_VJ_Charger_%2816950622926%29.jpg",
        "license": "CC BY 2.0",
        "artist": "Jeremy (Flickr)",
        "source_url": "https://commons.wikimedia.org/wiki/File:Chrysler_Valiant_VJ_Charger_(16950622926).jpg",
    },
    {
        "id": "vk",
        "filename": "Chrysler VK Valiant Regal Sedan 03.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Chrysler_VK_Valiant_Regal_Sedan_03.jpg/960px-Chrysler_VK_Valiant_Regal_Sedan_03.jpg",
        "license": "Public domain",
        "artist": "MartinHansV",
        "source_url": "https://commons.wikimedia.org/wiki/File:Chrysler_VK_Valiant_Regal_Sedan_03.jpg",
    },
    {
        "id": "cl",
        "filename": "Chrysler Valiant CL (16153035161).jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Chrysler_Valiant_CL_%2816153035161%29.jpg/960px-Chrysler_Valiant_CL_%2816153035161%29.jpg",
        "license": "CC BY 2.0",
        "artist": "Jeremy (Flickr)",
        "source_url": "https://commons.wikimedia.org/wiki/File:Chrysler_Valiant_CL_(16153035161).jpg",
    },
    {
        "id": "cm",
        "filename": "1980 Valiant CM Standard==.JPG",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/1980_Valiant_CM_Standard%3D%3D.JPG/960px-1980_Valiant_CM_Standard%3D%3D.JPG",
        "license": "CC BY-SA 4.0",
        "artist": "Sicnag",
        "source_url": "https://commons.wikimedia.org/wiki/File:1980_Valiant_CM_Standard==.JPG",
    },
    {
        "id": "chrysler-by-chrysler",
        "filename": "Chrysler_CH_Sedan_(white).JPG",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Chrysler_CH_Sedan_%28white%29.JPG/960px-Chrysler_CH_Sedan_%28white%29.JPG",
        "license": "CC BY-SA 3.0",
        "artist": "OSX",
        "source_url": "https://commons.wikimedia.org/wiki/File:Chrysler_CH_Sedan_(white).JPG",
    },
]

OUTPUT_SIZE = (520, 293)  # 16:9


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as resp:
        dest.write_bytes(resp.read())


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
    """Build an 8-colour palette image for quantisation."""
    colors = [
        (10, 10, 10),
        (255, 106, 0),
        (242, 194, 0),
        (245, 240, 230),
        (27, 79, 138),
        (45, 107, 58),
        (90, 90, 90),
        (200, 200, 200),
    ]
    palette = []
    for r, g, b in colors:
        palette.extend([r, g, b])
    palette.extend([0, 0, 0] * (256 - len(colors)))
    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette(palette)
    return pal_img


def stylize(img: Image.Image) -> Image.Image:
    """Convert a photo into a flat, posterised 2D illustration."""
    img = crop_center_16_9(img)
    img = img.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)

    # Smooth surfaces before quantising for a flatter illustrated look
    img = img.filter(ImageFilter.MedianFilter(size=3))
    img = ImageOps.autocontrast(img, cutoff=1)
    img = ImageEnhance.Color(img).enhance(1.35)
    img = ImageEnhance.Contrast(img).enhance(1.5)
    img = ImageEnhance.Sharpness(img).enhance(0.8)

    # Posterise to flat colour bands
    img = img.quantize(colors=8, method=Image.Quantize.MEDIANCUT).convert("RGB")
    img = img.quantize(palette=build_brand_palette(), dither=Image.Dither.NONE).convert("RGB")

    # Reinforce outlines for 2D graphic feel
    gray = img.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edges = ImageEnhance.Contrast(edges).enhance(4.0)
    edges = edges.point(lambda p: 255 if p > 60 else 0)
    edge_rgb = Image.merge("RGB", (edges, edges, edges))

    # Darken edge pixels on the posterised image
    img = ImageChops.multiply(img, ImageChops.invert(edge_rgb).point(lambda p: min(255, p + 40)))

    # Subtle warm tint for period ad warmth
    tint = Image.new("RGB", OUTPUT_SIZE, (255, 106, 0))
    img = Image.blend(img, tint, alpha=0.06)

    return img


def clean_artist(raw: str) -> str:
    text = re.sub(r"<[^>]+>", "", raw)
    return text.strip()[:120] or "Wikimedia Commons contributor"


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    STYLIZED_DIR.mkdir(parents=True, exist_ok=True)

    attributions = []

    for i, model in enumerate(MODELS):
        model_id = model["id"]
        source_path = SOURCE_DIR / f"{model_id}.jpg"
        output_path = STYLIZED_DIR / f"{model_id}.png"

        print(f"[{i + 1}/{len(MODELS)}] {model_id}…")
        if not source_path.exists():
            download(model["url"], source_path)
            time.sleep(0.5)

        img = Image.open(source_path).convert("RGB")
        styled = stylize(img)
        styled.save(output_path, "PNG", optimize=True)

        attributions.append({
            "id": model_id,
            "source_file": model["filename"],
            "source_url": model["source_url"],
            "license": model["license"],
            "artist": clean_artist(model["artist"]),
            "stylized": f"assets/models/{model_id}.png",
        })

    ATTRIBUTIONS_FILE.write_text(json.dumps(attributions, indent=2), encoding="utf-8")
    print(f"\nDone — {len(attributions)} stylized images saved to {STYLIZED_DIR}")


if __name__ == "__main__":
    main()
