#!/usr/bin/env python3
"""Build a fixed-size PDF from rendered JPEG pages."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("images_dir")
    parser.add_argument("output_pdf")
    parser.add_argument("--dpi", type=int, default=180)
    args = parser.parse_args()

    paths = sorted(Path(args.images_dir).glob("page-*.jpg"))
    if not paths:
        raise ValueError("No rendered JPEG pages found")
    images = [Image.open(path).convert("RGB") for path in paths]
    try:
        images[0].save(
            args.output_pdf,
            "PDF",
            save_all=True,
            append_images=images[1:],
            resolution=args.dpi,
        )
    finally:
        for image in images:
            image.close()


if __name__ == "__main__":
    main()
