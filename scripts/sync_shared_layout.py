"""Synchronize the shared header and footer across every static page."""

from argparse import ArgumentParser
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
PARTIALS = ROOT / "partials"
SOURCE = ROOT / "index.html"

COMPONENTS = {
    "header": re.compile(
        r"^[ \t]*(?:<!-- Header Start -->\s*)?<header class=\"main-header\">.*?<!-- Header End -->",
        re.DOTALL | re.MULTILINE,
    ),
    "footer": re.compile(
        r"^[ \t]*(?:<!-- Main Footer Start -->\s*)?<footer class=\"main-footer[^\"]*\">.*?<!-- Main Footer End -->",
        re.DOTALL | re.MULTILINE,
    ),
}


def extract_components():
    PARTIALS.mkdir(exist_ok=True)
    source = SOURCE.read_text(encoding="utf-8")
    for name, pattern in COMPONENTS.items():
        match = pattern.search(source)
        if not match:
            raise SystemExit(f"Missing {name} component in {SOURCE.name}")
        component = "\n".join(line.rstrip() for line in match.group(0).splitlines()).strip()
        (PARTIALS / f"{name}.html").write_text(component + "\n", encoding="utf-8")


def synchronize_pages():
    partials = {}
    for name in COMPONENTS:
        path = PARTIALS / f"{name}.html"
        if not path.exists():
            raise SystemExit(f"Missing shared component: {path}")
        partials[name] = path.read_text(encoding="utf-8").rstrip()

    for page in ROOT.glob("*.html"):
        source = page.read_text(encoding="utf-8")
        for name, pattern in COMPONENTS.items():
            if not pattern.search(source):
                raise SystemExit(f"{page.name}: missing {name} markers")
            source = pattern.sub(partials[name], source, count=1)
        page.write_text(source, encoding="utf-8")


parser = ArgumentParser()
parser.add_argument("--extract", action="store_true", help="Create partials from the current homepage")
args = parser.parse_args()

if args.extract:
    extract_components()
else:
    synchronize_pages()
