#!/usr/bin/env python3
"""
Generate the responsive image variants and the social-share image.

The photographs are 1600px wide JPEGs of 200-270KB each. The widest slot any
of them occupies is 552px on a desktop layout and 358px on a phone, so every
visitor was downloading roughly three times the pixels they could see, on the
render-blocking path for Largest Contentful Paint.

This writes, for each source photograph:

    <name>-480.webp   <name>-480.jpg
    <name>-960.webp   <name>-960.jpg
    <name>-1600.webp  <name>-1600.jpg

WebP is served first and the JPEG is the fallback, through <picture>. Both
carry the full srcset, so a browser without WebP still gets a correctly sized
image rather than the largest one.

It also composes assets/og-cover.jpg, the 1200x630 card that Facebook,
LinkedIn, Slack and X render when a page is shared. Without one, those
previews fall back to whatever the platform scrapes, which is usually
nothing.

Run after adding or replacing a photograph:

    python3 tools/build_images.py
"""

import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is needed: pip install Pillow")

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "site" / "assets"

# 480 covers phones at 1x and small slots; 960 covers phones at 2x and the
# desktop column; 1600 is the original, kept for large screens at 2x.
WIDTHS = (480, 960, 1600)

# Sources are the un-suffixed JPEGs. Generated variants carry a -<width>
# suffix, so they are skipped on a re-run rather than re-processed.
SOURCES = sorted(
    p for p in ASSETS.glob("*.jpg")
    if not any(p.stem.endswith(f"-{w}") for w in WIDTHS)
    and p.stem != "og-cover"
)

NAVY = (10, 35, 66)
GREEN = (53, 199, 122)
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def variants() -> None:
    for src in SOURCES:
        im = Image.open(src).convert("RGB")
        for w in WIDTHS:
            if im.width < w:
                continue
            h = round(im.height * w / im.width)
            resized = im.resize((w, h), Image.LANCZOS)
            # method=6 is the slowest, smallest WebP setting. This runs on a
            # handful of files by hand, so the time is irrelevant and the
            # bytes are not.
            resized.save(ASSETS / f"{src.stem}-{w}.webp", "WEBP",
                         quality=82, method=6)
            resized.save(ASSETS / f"{src.stem}-{w}.jpg", "JPEG",
                         quality=82, optimize=True, progressive=True)
        print(f"  {src.name}: {', '.join(str(w) for w in WIDTHS)}")


def og_cover() -> None:
    """The 1200x630 social card.

    Built from a site photograph so the preview looks like the site, with a
    navy scrim heavy enough to keep the text legible over any part of the
    image — a share card whose title is unreadable is worse than no card.
    """
    base = ASSETS / "ampoules-microscope.jpg"
    if not base.exists():
        print("  skipped og-cover: source photograph missing")
        return

    W, H = 1200, 630
    im = Image.open(base).convert("RGB")

    # Cover-fit: scale to fill, then centre-crop, so the photo is never
    # squashed to the card's aspect ratio.
    scale = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left, top = (im.width - W) // 2, (im.height - H) // 2
    im = im.crop((left, top, left + W, top + H))

    scrim = Image.new("RGB", (W, H), NAVY)
    im = Image.blend(im, scrim, 0.78)

    d = ImageDraw.Draw(im)
    title = ImageFont.truetype(FONT_BOLD, 66)
    sub = ImageFont.truetype(FONT_REG, 30)
    eyebrow = ImageFont.truetype(FONT_BOLD, 24)

    d.text((80, 150), "RESEARCH LAB USA", font=eyebrow, fill=GREEN)
    d.text((80, 205), "Research compound", font=title, fill="white")
    d.text((80, 285), "reference guides", font=title, fill="white")
    d.text((80, 400), "Chemical identity, handling and an honest account",
           font=sub, fill=(200, 214, 232))
    d.text((80, 442), "of what the literature actually shows.",
           font=sub, fill=(200, 214, 232))
    d.rectangle([80, 520, 140, 526], fill=GREEN)
    d.text((80, 550), "researchlabusa.com", font=sub, fill=(150, 172, 200))

    out = ASSETS / "og-cover.jpg"
    im.save(out, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"  og-cover.jpg: {W}x{H}, {out.stat().st_size // 1024}KB")


def main() -> None:
    if not SOURCES:
        sys.exit("No source photographs found in site/assets/")
    print(f"Generating variants for {len(SOURCES)} photographs:")
    variants()
    print("Composing the social-share card:")
    og_cover()


if __name__ == "__main__":
    main()
