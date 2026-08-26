"""Add intrinsic dimensions to local images to prevent layout shifts."""

from pathlib import Path
import re
import xml.etree.ElementTree as ET

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent


def numeric_dimension(value):
    if not value:
        return None
    match = re.match(r"\s*([0-9]+(?:\.[0-9]+)?)", value)
    return round(float(match.group(1))) if match else None


def image_dimensions(path):
    if path.suffix.lower() == ".svg":
        root = ET.parse(path).getroot()
        width = numeric_dimension(root.get("width"))
        height = numeric_dimension(root.get("height"))
        if width and height:
            return width, height
        viewbox = root.get("viewBox", "").replace(",", " ").split()
        if len(viewbox) == 4:
            return round(float(viewbox[2])), round(float(viewbox[3]))
        return None

    with Image.open(path) as image:
        return image.size


def add_dimensions(match):
    tag = match.group(0)
    if re.search(r"\bwidth=", tag, re.IGNORECASE) and re.search(r"\bheight=", tag, re.IGNORECASE):
        return tag

    source_match = re.search(r'\bsrc=["\']([^"\']+)["\']', tag, re.IGNORECASE)
    if not source_match:
        return tag
    source = source_match.group(1).split("?", 1)[0]
    if source.startswith(("http:", "https:", "//", "data:")):
        return tag

    image_path = ROOT / source.lstrip("/")
    if not image_path.exists():
        return tag
    dimensions = image_dimensions(image_path)
    if not dimensions:
        return tag

    width, height = dimensions
    tag = re.sub(r'\s+width=["\'][^"\']*["\']', "", tag, flags=re.IGNORECASE)
    tag = re.sub(r'\s+height=["\'][^"\']*["\']', "", tag, flags=re.IGNORECASE)
    return tag.replace("<img", f'<img width="{width}" height="{height}"', 1)


for page in ROOT.glob("*.html"):
    source = page.read_text(encoding="utf-8")
    source = re.sub(r"<img\b[^>]*>", add_dimensions, source, flags=re.IGNORECASE)
    page.write_text(source, encoding="utf-8")
