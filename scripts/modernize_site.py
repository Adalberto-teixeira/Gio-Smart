from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent.parent

PRELOADER = re.compile(
    r"\s*<!-- Preloader Start -->.*?<!-- Preloader End -->\s*",
    re.IGNORECASE | re.DOTALL,
)

for path in ROOT.glob("*.html"):
    source = path.read_text(encoding="utf-8")

    # The full-screen loader hides useful content until every third-party asset
    # has finished. The page remains fully usable without it.
    source = PRELOADER.sub("\n", source)
    source = source.replace(
        "width=device-width, initial-scale=1.0, maximum-scale=1",
        "width=device-width, initial-scale=1.0",
    )
    source = re.sub(r'\s*<!-- SEO Keywords -->\s*<meta\s+name=["\']keywords["\'][^>]*>', '', source, flags=re.IGNORECASE)

    # Remove optional effects that add network/CPU cost without helping users.
    source = re.sub(r'\s*<link[^>]+href=["\']css/mousecursor\.css["\'][^>]*>', '', source)
    source = re.sub(r'\s*<script[^>]+src=["\']js/magiccursor\.js["\'][^>]*></script>', '', source)
    source = re.sub(r'\s*<script[^>]+src=["\']js/jquery\.mb\.YTPlayer\.min\.js["\'][^>]*></script>', '', source)

    # Keep script order while allowing HTML parsing to continue.
    source = re.sub(
        r'<script(?![^>]*\bdefer\b)([^>]+src=["\']js/[^"\']+["\'][^>]*)>',
        r'<script defer\1>',
        source,
    )

    # Lazy-load content images. Logos stay eager because they are visible first.
    def optimize_image(match):
        tag = match.group(0)
        if "loading=" in tag:
            return tag
        if any(name in tag for name in ("logo.svg", "favicon.png")):
            if "decoding=" in tag:
                return tag
            return tag.replace("<img", '<img decoding="async"', 1)
        return tag.replace("<img", '<img loading="lazy" decoding="async"', 1)

    source = re.sub(r'<img\b[^>]*>', optimize_image, source, flags=re.IGNORECASE)

    # Protect links that open a new tab.
    source = re.sub(
        r'<a(?![^>]*\brel=)([^>]*\btarget=["\']_blank["\'][^>]*)>',
        r'<a rel="noopener noreferrer"\1>',
        source,
        flags=re.IGNORECASE,
    )

    # Add consistent sharing previews using each page's existing title/summary.
    if 'property="og:title"' not in source:
        title_match = re.search(r'<title>(.*?)</title>', source, re.DOTALL | re.IGNORECASE)
        desc_match = re.search(
            r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']',
            source,
            re.IGNORECASE,
        )
        canonical_match = re.search(
            r'(<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']\s*/?>)',
            source,
            re.IGNORECASE,
        )
        if title_match and desc_match and canonical_match:
            title = html.escape(re.sub(r'\s+', ' ', title_match.group(1)).strip(), quote=True)
            description = html.escape(desc_match.group(1).strip(), quote=True)
            url = html.escape(canonical_match.group(2), quote=True)
            social = f'''{canonical_match.group(1)}
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="fr_FR" />
  <meta property="og:site_name" content="Gio Smart" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="https://giosmart-services.fr/images/hero-bg.jpg" />
  <meta name="twitter:card" content="summary_large_image" />'''
            source = source.replace(canonical_match.group(1), social, 1)

    # Common copy fixes.
    replacements = {
        "Nos Réalisation": "Nos réalisations",
        "No Réalisation": "Nos réalisations",
        "Nos réalisationss": "Nos réalisations",
        "Nettoyage apres travaux demenagement": "Nettoyage après travaux et déménagement",
        "contacter sur whatsapp": "Contacter sur WhatsApp",
        "Contacter Sur Whatsapp": "Contacter sur WhatsApp",
        ">adalbertofurtado.com<": ">adalberto.fr<",
    }
    for old, new in replacements.items():
        source = source.replace(old, new)

    source = source.replace('decoding="async" decoding="async"', 'decoding="async"')

    path.write_text(source, encoding="utf-8")

sitemap = ROOT / "sitemap.xml"
if sitemap.exists():
    sitemap_source = sitemap.read_text(encoding="utf-8")
    sitemap_source = re.sub(r"<lastmod>[^<]+</lastmod>", "<lastmod>2026-08-25</lastmod>", sitemap_source)
    sitemap.write_text(sitemap_source, encoding="utf-8")
