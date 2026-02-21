#!/usr/bin/env python3
"""
Process original photos into three web-optimized tiers:
  thumbs  - 400px wide, quality 70
  medium  - 1200px wide, quality 80
  full    - 2000px wide, quality 85
"""

import os
import re
import sys
import time
from pathlib import Path
from PIL import Image

# -- Configuration --

BASE = Path("/home/jeffjanovitch/claude-projects/jokesshots/src/assets/photos")
ORIGINALS = BASE / "originals" / "Homepage Shortlist"

FOLDER_MAP = {
    "Boondawg": "boondawg",
    "Burna Boy": "burna-boy",
    "Ice Cube": "ice-cube",
    "KAYTRANADA": "kaytranada",
    "Larry June": "larry-june",
    "Luciano": "luciano",
    "Misc Shortlist": "misc",
    "OG KEEMO": "og-keemo",
    "RIN": "rin",
    "Roddy Rich": "roddy-ricch",
    "Soulside Shortlist": "soulside",
    "Westside Boogie": "westside-boogie",
}

TIERS = [
    {"name": "thumbs",  "max_width": 400,  "quality": 70},
    {"name": "medium",  "max_width": 1200, "quality": 80},
    {"name": "full",    "max_width": 2000, "quality": 85},
]

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}

# -- Helpers --

def sanitize_filename(name):
    """Lowercase, replace spaces/parens/underscores with hyphens, collapse duplicates, strip."""
    stem = Path(name).stem
    s = stem.lower()
    # replace spaces, underscores, parentheses, brackets with hyphens
    s = re.sub(r"[\s_\(\)\[\]]+", "-", s)
    # remove " copy" artifacts (e.g. "--copy", "-copy-2")
    s = re.sub(r"-*copy-*\d*", "", s)
    # strip any non-alphanumeric except hyphens
    s = re.sub(r"[^a-z0-9\-]", "", s)
    # collapse multiple hyphens
    s = re.sub(r"-{2,}", "-", s)
    # strip leading/trailing hyphens
    s = s.strip("-")
    if not s:
        s = "image"
    return s + ".jpg"


def process_image(src_path, dst_path, max_width, quality):
    """Open image, resize if needed, strip EXIF, save as progressive JPEG."""
    img = Image.open(src_path)

    # Handle transparency (RGBA/P) by compositing onto white background
    if img.mode in ("RGBA", "LA", "P"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        background.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
        img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")

    # Only downscale, never upscale
    w, h = img.size
    if w > max_width:
        ratio = max_width / w
        new_w = max_width
        new_h = int(h * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)

    # Save as progressive JPEG, no EXIF
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst_path, "JPEG", quality=quality, progressive=True, optimize=True)


# -- Main --

def main():
    start = time.time()
    stats = {tier["name"]: {"count": 0, "bytes": 0} for tier in TIERS}
    errors = []
    skipped = 0
    total_processed = 0

    # Gather all source images first for progress tracking
    source_files = []
    for orig_folder, dest_slug in sorted(FOLDER_MAP.items()):
        src_dir = ORIGINALS / orig_folder
        if not src_dir.is_dir():
            print(f"  WARNING: source folder not found: {src_dir}")
            continue
        for f in sorted(src_dir.iterdir()):
            if f.suffix.lower() in IMAGE_EXTENSIONS and f.is_file():
                source_files.append((f, dest_slug))

    total = len(source_files)
    print(f"Found {total} images across {len(FOLDER_MAP)} folders")
    print(f"Processing into {len(TIERS)} tiers: {', '.join(t['name'] for t in TIERS)}")
    print("=" * 70)

    for idx, (src_path, dest_slug) in enumerate(source_files, 1):
        clean_name = sanitize_filename(src_path.name)

        print(f"  [{idx:3d}/{total}] {dest_slug}/{clean_name} ", end="", flush=True)

        tier_ok = 0
        for tier in TIERS:
            dst_dir = BASE / tier["name"] / dest_slug
            dst_path = dst_dir / clean_name
            try:
                process_image(src_path, dst_path, tier["max_width"], tier["quality"])
                size = dst_path.stat().st_size
                stats[tier["name"]]["count"] += 1
                stats[tier["name"]]["bytes"] += size
                tier_ok += 1
            except Exception as e:
                errors.append((str(src_path), tier["name"], str(e)))

        if tier_ok == len(TIERS):
            print("OK")
            total_processed += 1
        elif tier_ok > 0:
            print(f"PARTIAL ({tier_ok}/{len(TIERS)} tiers)")
            total_processed += 1
        else:
            print("FAILED")
            skipped += 1

    # -- Summary --
    elapsed = time.time() - start
    print()
    print("=" * 70)
    print(f"DONE in {elapsed:.1f}s")
    print(f"  Processed: {total_processed} images")
    if skipped:
        print(f"  Skipped:   {skipped} images")
    print()

    for tier in TIERS:
        name = tier["name"]
        count = stats[name]["count"]
        total_mb = stats[name]["bytes"] / (1024 * 1024)
        print(f"  {name:8s}  {count:4d} files  {total_mb:8.2f} MB  (max {tier['max_width']}px, q{tier['quality']})")

    grand_total = sum(s["bytes"] for s in stats.values())
    grand_count = sum(s["count"] for s in stats.values())
    print(f"  {'TOTAL':8s}  {grand_count:4d} files  {grand_total / (1024*1024):8.2f} MB")

    if errors:
        print(f"\n  Errors ({len(errors)}):")
        for path, tier, msg in errors:
            print(f"    [{tier}] {path}: {msg}")

    print()


if __name__ == "__main__":
    main()
