#!/usr/bin/env python3
"""Re-encode eligible PDF image streams as JPEG while preserving page layout."""

from __future__ import annotations

import argparse
from io import BytesIO

from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, NumberObject


def walk_resources(resources, seen):
    for ref in resources.get("/XObject", {}).values():
        obj = ref.get_object()
        key = (ref.idnum, ref.generation)
        if key in seen:
            continue
        seen.add(key)
        subtype = obj.get("/Subtype")
        if subtype == "/Image":
            yield obj
        elif subtype == "/Form":
            yield from walk_resources(obj.get("/Resources", {}), seen)


def as_jpeg(image_obj, quality, scale):
    """Return JPEG data for images pypdf can safely decode as 8-bit RGB/gray."""
    if image_obj.get("/Mask"):
        return None
    if image_obj.get("/BitsPerComponent") != 8:
        return None

    width = image_obj.get("/Width")
    height = image_obj.get("/Height")
    colorspace = image_obj.get("/ColorSpace")
    if hasattr(colorspace, "get_object"):
        colorspace = colorspace.get_object()
    colors = None
    if isinstance(colorspace, str):
        colors = {"/DeviceGray": 1, "/DeviceRGB": 3}.get(colorspace)
    elif isinstance(colorspace, (list, tuple)) and colorspace:
        # ICCBased images in this source use 3-channel RGB profiles.
        if colorspace[0] == "/ICCBased":
            profile = colorspace[1].get_object()
            colors = profile.get("/N")
    if colors not in (1, 3):
        return None

    try:
        mode = "L" if colors == 1 else "RGB"
        pixels = image_obj.get_data()
        image = Image.frombytes(mode, (width, height), pixels)
        if scale < 1:
            resized = (max(1, round(width * scale)), max(1, round(height * scale)))
            image = image.resize(resized, Image.Resampling.LANCZOS)
        data = BytesIO()
        image.save(data, format="JPEG", quality=quality, optimize=True, progressive=True)
        return data.getvalue(), image.size
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_pdf")
    parser.add_argument("output_pdf")
    parser.add_argument("--quality", type=int, default=92)
    parser.add_argument("--scale", type=float, default=1.0)
    args = parser.parse_args()

    reader = PdfReader(args.input_pdf)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)

    seen = set()
    changed = 0
    before = 0
    after = 0
    for page in writer.pages:
        for image_obj in walk_resources(page.get("/Resources", {}), seen):
            before += len(image_obj._data)
            result = as_jpeg(image_obj, args.quality, args.scale)
            jpeg, dimensions = result if result is not None else (None, None)
            if jpeg is None or len(jpeg) >= len(image_obj._data):
                after += len(image_obj._data)
                continue
            image_obj._data = jpeg
            image_obj[NameObject("/Filter")] = NameObject("/DCTDecode")
            image_obj.pop(NameObject("/DecodeParms"), None)
            image_obj[NameObject("/Width")] = NumberObject(dimensions[0])
            image_obj[NameObject("/Height")] = NumberObject(dimensions[1])
            changed += 1
            after += len(jpeg)

    with open(args.output_pdf, "wb") as output:
        writer.write(output)
    print(f"re-encoded images: {changed}; image bytes: {before} -> {after}")


if __name__ == "__main__":
    main()
