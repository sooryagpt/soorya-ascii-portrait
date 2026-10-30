#!/usr/bin/env python3
"""
Turn a photo into terminal-style ASCII art.

Usage:
    python ascii_portrait.py your_photo.jpg

Optional:
    python ascii_portrait.py your_photo.jpg --width 100 --output portrait.txt
"""

import argparse
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance

RAMP = " .,:;irsXA253hMHGS#9B&@"


def make_ascii(image_path: Path, width: int, output_path: Path) -> None:
    image = Image.open(image_path).convert("RGB")
    image = ImageOps.grayscale(image)

    # Terminal characters are taller than they are wide, so use half-height.
    height = max(1, int(width * image.height / image.width * 0.5))
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    image = ImageEnhance.Contrast(image).enhance(1.35)

    pixels = image.load()
    lines = []
    for y in range(height):
        line = []
        for x in range(width):
            value = pixels[x, y]
            index = min(len(RAMP) - 1, value * len(RAMP) // 256)
            line.append(RAMP[index])
        lines.append("".join(line))

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"ASCII portrait saved to: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a photo into ASCII art.")
    parser.add_argument("image", type=Path, help="Path to the input photo")
    parser.add_argument("--width", type=int, default=100, help="Output character width")
    parser.add_argument("--output", type=Path, default=Path("portrait.txt"))
    args = parser.parse_args()

    if not args.image.is_file():
        parser.error(f"Image not found: {args.image}")
    if args.width < 20:
        parser.error("--width must be at least 20")

    make_ascii(args.image, args.width, args.output)


if __name__ == "__main__":
    main()
