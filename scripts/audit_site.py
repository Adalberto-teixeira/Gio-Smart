"""Fail when a local page references a missing asset/page or has invalid basics."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
errors = []


def resolve_local_reference(reference):
    """Map a public clean route back to its source file for validation."""
    path = urlparse(reference).path.lstrip("/")
    if not path:
        return ROOT / "index.html"
    direct = ROOT / path
    if direct.exists():
        return direct
    return ROOT / f"{path}.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.ids = []
        self.h1_count = 0
        self.images_without_dimensions = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(attributes["id"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "img" and (not attributes.get("width") or not attributes.get("height")):
            self.images_without_dimensions += 1
        for name in ("src", "href"):
            value = attributes.get(name, "")
            if value and not value.startswith(("http:", "https:", "tel:", "mailto:", "#", "//", "data:")):
                self.references.append(value.split("#")[0].split("?")[0])


for page in sorted(ROOT.glob("*.html")):
    parser = PageParser()
    parser.feed(page.read_text(encoding="utf-8"))
    for reference in parser.references:
        if reference and not resolve_local_reference(reference).exists():
            errors.append(f"{page.name}: missing {reference}")
    duplicates = [item for item, count in Counter(parser.ids).items() if count > 1]
    if duplicates:
        errors.append(f"{page.name}: duplicate ids {duplicates}")
    if parser.images_without_dimensions:
        errors.append(f"{page.name}: {parser.images_without_dimensions} images missing width/height")
    if page.name != "page-introuvable.html" and parser.h1_count != 1:
        errors.append(f"{page.name}: expected one H1, found {parser.h1_count}")

    if page.name == "services.html":
        source = page.read_text(encoding="utf-8")
        if '<a href="/services-numeriques">Soins des animaux</a>' in source:
            errors.append("services.html: animal care title points to digital services")

namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
for node in ET.parse(ROOT / "sitemap.xml").findall(".//s:loc", namespace):
    if not resolve_local_reference(node.text).exists():
        errors.append(f"sitemap.xml: missing {node.text}")

if errors:
    raise SystemExit("\n".join(errors))

print(f"Audit passed: {len(list(ROOT.glob('*.html')))} pages checked.")
