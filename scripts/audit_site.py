"""Fail when a local page references a missing asset/page or has invalid basics."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import json
import re
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
        self.html_extension_refs = []
        self.unnamed_visual_links = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(attributes["id"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "img" and (not attributes.get("width") or not attributes.get("height")):
            self.images_without_dimensions += 1
        if tag == "a":
            href = attributes.get("href", "")
            if ".html" in urlparse(href).path:
                self.html_extension_refs.append(href)
            if attributes.get("data-cursor-text") == "Voir" and not attributes.get("aria-label"):
                self.unnamed_visual_links += 1
        for name in ("src", "href"):
            value = attributes.get(name, "")
            if value and not value.startswith(("http:", "https:", "tel:", "mailto:", "#", "//", "data:")):
                self.references.append(value.split("#")[0].split("?")[0])


for page in sorted(ROOT.glob("*.html")):
    source = page.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(source)
    for reference in parser.references:
        if reference and not resolve_local_reference(reference).exists():
            errors.append(f"{page.name}: missing {reference}")
    duplicates = [item for item, count in Counter(parser.ids).items() if count > 1]
    if duplicates:
        errors.append(f"{page.name}: duplicate ids {duplicates}")
    if parser.images_without_dimensions:
        errors.append(f"{page.name}: {parser.images_without_dimensions} images missing width/height")
    if parser.html_extension_refs:
        errors.append(f"{page.name}: .html links found {parser.html_extension_refs}")
    if parser.unnamed_visual_links:
        errors.append(f"{page.name}: {parser.unnamed_visual_links} visual links missing aria-label")
    for required_pwa_markup in (
        'name="theme-color"',
        'name="apple-mobile-web-app-capable" content="yes"',
        'rel="manifest" href="/manifest.webmanifest"',
        'rel="apple-touch-icon"',
    ):
        if required_pwa_markup not in source:
            errors.append(f"{page.name}: missing PWA markup {required_pwa_markup}")
    if page.name != "page-introuvable.html" and parser.h1_count != 1:
        errors.append(f"{page.name}: expected one H1, found {parser.h1_count}")

    if page.name == "services.html":
        if '<a href="/services-numeriques">Soins des animaux</a>' in source:
            errors.append("services.html: animal care title points to digital services")

    if page.name == "contact.html":
        for required_contact_markup in (
            'data-contact-method="whatsapp"',
            'data-contact-method="email"',
            'action="/api/contact"',
            'id="email"',
            'id="website"',
        ):
            if required_contact_markup not in source:
                errors.append(f"contact.html: missing contact option {required_contact_markup}")

    if page.name not in ("404.html", "page-introuvable.html"):
        title_match = re.search(r"<title>(.*?)</title>", source, re.DOTALL | re.IGNORECASE)
        description_match = re.search(
            r'<meta\s+name="description"\s+content="([^"]*)"', source, re.DOTALL | re.IGNORECASE
        )
        if not title_match or not 20 <= len(" ".join(title_match.group(1).split())) <= 60:
            errors.append(f"{page.name}: title should contain 20-60 characters")
        if not description_match or not 100 <= len(" ".join(description_match.group(1).split())) <= 160:
            errors.append(f"{page.name}: description should contain 100-160 characters")

    for raw_json in re.findall(
        r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.DOTALL | re.IGNORECASE
    ):
        try:
            json.loads(raw_json)
        except json.JSONDecodeError as error:
            errors.append(f"{page.name}: invalid structured data ({error})")

    if not re.search(r'class="[^"]*\bswiper\b', source, re.IGNORECASE) and "swiper-bundle" in source:
        errors.append(f"{page.name}: loads Swiper without a slider")
    if not re.search(r'class="[^"]*\bpopup-video\b', source, re.IGNORECASE) and "magnific-popup" in source:
        errors.append(f"{page.name}: loads Magnific Popup without a popup")

not_found = (ROOT / "404.html").read_text(encoding="utf-8")
if 'name="robots" content="noindex, follow"' not in not_found:
    errors.append("404.html: missing noindex directive")
if 'rel="canonical"' in not_found:
    errors.append("404.html: must not declare a canonical URL")

namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
for node in ET.parse(ROOT / "sitemap.xml").findall(".//s:loc", namespace):
    if not resolve_local_reference(node.text).exists():
        errors.append(f"sitemap.xml: missing {node.text}")

manifest_path = ROOT / "manifest.webmanifest"
try:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as error:
    errors.append(f"manifest.webmanifest: invalid or missing ({error})")
else:
    if manifest.get("display") != "standalone":
        errors.append("manifest.webmanifest: display must be standalone")
    if manifest.get("start_url") != "/" or manifest.get("scope") != "/":
        errors.append("manifest.webmanifest: invalid start_url or scope")
    for size in ("192x192", "512x512"):
        icon = next((item for item in manifest.get("icons", []) if item.get("sizes") == size), None)
        if not icon or not resolve_local_reference(icon.get("src", "")).exists():
            errors.append(f"manifest.webmanifest: missing {size} icon")

service_worker = ROOT / "sw.js"
if not service_worker.exists() or 'self.addEventListener("fetch"' not in service_worker.read_text(encoding="utf-8"):
    errors.append("sw.js: missing fetch handler")
if not (ROOT / "images/apple-touch-icon.png").exists():
    errors.append("images/apple-touch-icon.png: missing iOS home-screen icon")

contact_function = ROOT / "api/contact.mjs"
if not contact_function.exists():
    errors.append("api/contact.mjs: missing Resend contact function")
else:
    contact_function_source = contact_function.read_text(encoding="utf-8")
    for required_function_markup in (
        "process.env.RESEND_API_KEY",
        "https://api.resend.com/emails",
        'reply_to: form.email',
        '"configuration_required"',
    ):
        if required_function_markup not in contact_function_source:
            errors.append(f"api/contact.mjs: missing {required_function_markup}")

if errors:
    raise SystemExit("\n".join(errors))

print(f"Audit passed: {len(list(ROOT.glob('*.html')))} pages checked.")
