"""Create efficient WebP variants for larger raster assets and update references."""

from pathlib import Path
import re

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"
MINIMUM_SIZE = 30_000

html_files = list(ROOT.glob("*.html"))
css_files = list((ROOT / "css").glob("*.css"))
text_files = html_files + css_files
combined_source = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in text_files)

referenced = set(
    re.findall(
        r'(?:\.\./)?images/([^"\'\) ]+\.(?:jpg|jpeg|png))',
        combined_source,
        flags=re.IGNORECASE,
    )
)

replacements = {}
saved_bytes = 0

for filename in sorted(referenced):
    original = IMAGES / filename
    if not original.exists() or original.stat().st_size < MINIMUM_SIZE:
        continue

    optimized = original.with_suffix(".webp")
    with Image.open(original) as image:
        image.save(optimized, "WEBP", quality=82, method=6)

    if optimized.stat().st_size >= original.stat().st_size:
        optimized.unlink()
        continue

    replacements[filename] = optimized.name
    saved_bytes += original.stat().st_size - optimized.stat().st_size

for path in text_files:
    source = path.read_text(encoding="utf-8")
    updated = source
    for original, optimized in replacements.items():
        updated = updated.replace(f"images/{original}", f"images/{optimized}")
    if updated != source:
        path.write_text(updated, encoding="utf-8")

print(f"Optimized {len(replacements)} images; estimated transfer saving: {saved_bytes / 1024:.1f} KiB")
