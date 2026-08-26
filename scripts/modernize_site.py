from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent.parent

PRELOADER = re.compile(
    r"\s*<!-- Preloader Start -->.*?<!-- Preloader End -->\s*",
    re.IGNORECASE | re.DOTALL,
)

SERVICE_ROUTES = {
    "menage-et-entretien.html": "/menage-et-entretien",
    "aide-a-la-personne.html": "/aide-a-la-personne",
    "aide-au-demenagement.html": "/aide-au-demenagement",
    "services-numeriques.html": "/services-numeriques",
    "blanchisserie-et-couture.html": "/blanchisserie-et-couture",
    "services-soins-animaux.html": "/services-soins-animaux",
    "petits-travaux-maison.html": "/petits-travaux-maison",
    "nettoyage-apres-travaux-demenagement.html": "/nettoyage-apres-travaux-demenagement",
}

ROUTE_LABELS = {
    "/menage-et-entretien": "Découvrir le service Ménage et entretien",
    "/aide-a-la-personne": "Découvrir le service Aide aux personnes",
    "/aide-au-demenagement": "Découvrir le service Aide au déménagement",
    "/services-numeriques": "Découvrir les services numériques",
    "/blanchisserie-et-couture": "Découvrir le service Blanchisserie et couture",
    "/services-soins-animaux": "Découvrir le service Soins des animaux",
    "/petits-travaux-maison": "Découvrir le service Petits travaux",
    "/nettoyage-apres-travaux-demenagement": "Découvrir le nettoyage après travaux et déménagement",
    "/carte-visite-branding": "Voir le projet de cartes de visite",
    "/montage-cuisine-marseille": "Voir le projet de montage de meubles",
    "/nettoyage-jardin-vitrolles": "Voir le projet de nettoyage de jardin",
    "/local-technique-construction": "Voir le projet de construction du local technique",
    "/aide-demenagement-marseille-vitrolles": "Voir le projet de déménagement",
}

SEO_METADATA = {
    "index.html": (
        "Services à domicile à Martigues | Gio Smart",
        "Ménage, petits travaux, déménagement et aide quotidienne à Martigues et alentours. Contactez Gio Smart pour un devis gratuit et une réponse rapide.",
    ),
    "services.html": (
        "Services à domicile à Martigues | Nos prestations",
        "Découvrez les services Gio Smart à Martigues : ménage, déménagement, petits travaux, aide quotidienne, numérique, couture et soins des animaux.",
    ),
    "a-propos.html": (
        "Gio Smart, entreprise locale de services à Martigues",
        "Découvrez Gio Smart, une entreprise locale à taille humaine qui accompagne les particuliers à Martigues avec des services pratiques et accessibles.",
    ),
    "contact.html": (
        "Contact et devis gratuit à Martigues | Gio Smart",
        "Contactez Gio Smart pour votre besoin à Martigues et alentours. Demandez un devis gratuit par formulaire, WhatsApp, téléphone ou e-mail.",
    ),
    "faq.html": (
        "Questions fréquentes sur nos services | Gio Smart",
        "Réponses aux questions sur les tarifs, réservations, délais et zones d'intervention des services Gio Smart à Martigues et alentours.",
    ),
    "tarifs.html": (
        "Tarifs des services à domicile à Martigues | Gio Smart",
        "Consultez les tarifs indicatifs Gio Smart pour le ménage, les petits travaux, le déménagement, la couture et les autres services à Martigues.",
    ),
    "menage-et-entretien.html": (
        "Ménage à domicile à Martigues | Gio Smart",
        "Service de ménage ponctuel ou régulier à Martigues et alentours. Entretien du logement adapté à vos besoins et devis gratuit avec Gio Smart.",
    ),
    "aide-a-la-personne.html": (
        "Aide quotidienne à domicile à Martigues | Gio Smart",
        "Accompagnement quotidien, courses et aide administrative à Martigues. Une présence de proximité adaptée aux besoins de chaque personne.",
    ),
    "aide-au-demenagement.html": (
        "Aide au déménagement à Martigues | Gio Smart",
        "Aide au chargement, transport, démontage et remontage de meubles à Martigues et alentours. Demandez votre devis gratuit à Gio Smart.",
    ),
    "services-numeriques.html": (
        "Assistance numérique à Martigues | Gio Smart",
        "Aide informatique, configuration d'appareils, création de documents et services web à Martigues. Un accompagnement numérique simple et humain.",
    ),
    "blanchisserie-et-couture.html": (
        "Blanchisserie et couture à Martigues | Gio Smart",
        "Lavage, repassage, ourlets et petites retouches à Martigues. Gio Smart prend soin de votre linge avec un service pratique et personnalisé.",
    ),
    "services-soins-animaux.html": (
        "Soins des animaux à domicile à Martigues | Gio Smart",
        "Promenade, alimentation et surveillance de vos animaux à Martigues et alentours. Contactez Gio Smart pour organiser une prestation adaptée.",
    ),
    "petits-travaux-maison.html": (
        "Petits travaux à domicile à Martigues | Gio Smart",
        "Montage de meubles, fixations, petites réparations et peinture à Martigues. Expliquez votre besoin et recevez un devis gratuit Gio Smart.",
    ),
    "nettoyage-apres-travaux-demenagement.html": (
        "Nettoyage après travaux à Martigues | Gio Smart",
        "Remise en état après travaux ou déménagement à Martigues : dépoussiérage, sols et nettoyage complet. Demandez un devis gratuit.",
    ),
    "nos-realisations.html": (
        "Réalisations et services à Martigues | Gio Smart",
        "Découvrez des réalisations Gio Smart en petits travaux, déménagement, entretien, jardinage et services numériques à Martigues et alentours.",
    ),
    "carte-visite-branding.html": (
        "Création de cartes de visite | Réalisation Gio Smart",
        "Découvrez une création de cartes de visite personnalisées réalisée par Gio Smart : conception graphique, identité visuelle et impression.",
    ),
    "montage-cuisine-marseille.html": (
        "Montage de meubles à Marseille | Réalisation Gio Smart",
        "Montage de meubles et installation murale réalisés à Marseille par Gio Smart. Découvrez les étapes et le résultat de cette intervention.",
    ),
    "nettoyage-jardin-vitrolles.html": (
        "Nettoyage de jardin à Vitrolles | Gio Smart",
        "Nettoyage de jardin réalisé à Vitrolles : feuilles, branches et évacuation des déchets verts. Découvrez cette réalisation Gio Smart.",
    ),
    "local-technique-construction.html": (
        "Construction d'un local technique à Marseille | Gio Smart",
        "Découvrez la construction d'un local technique à Marseille : traçage, élévation en parpaings et toiture, réalisée par Gio Smart.",
    ),
    "aide-demenagement-marseille-vitrolles.html": (
        "Déménagement Marseille–Vitrolles | Gio Smart",
        "Aide au déménagement entre Marseille et Vitrolles : manutention, transport et montage de meubles. Découvrez cette intervention Gio Smart.",
    ),
    "mentions-legales.html": (
        "Mentions légales | Gio Smart",
        "Consultez les informations légales, l'éditeur, l'hébergement et les conditions d'utilisation du site Gio Smart Services.",
    ),
    "politique-confidentialite.html": (
        "Politique de confidentialité | Gio Smart",
        "Découvrez comment Gio Smart collecte, utilise et protège les informations transmises via son site et ses moyens de contact.",
    ),
}

# Vercel automatically serves a root 404.html for unknown static routes. Keep
# the designed error page as the single source so both versions stay aligned.
not_found_source = ROOT / "page-introuvable.html"
not_found_target = ROOT / "404.html"
if not_found_source.exists():
    not_found_target.write_text(not_found_source.read_text(encoding="utf-8"), encoding="utf-8")


def clean_internal_url(url):
    """Return the public, extensionless route for a local HTML URL."""
    if url.startswith("https://giosmart-services.fr/"):
        return re.sub(r"\.html(?=([?#]|$))", "", url)
    if url.startswith(("http:", "https:", "//", "mailto:", "tel:", "data:", "#")):
        return url

    match = re.fullmatch(r"(?:\./)?([^?#]*?)\.html([?#].*)?", url)
    if not match:
        return url
    route, suffix = match.group(1), match.group(2) or ""
    return ("/" if route == "index" else f"/{route.lstrip('/')}") + suffix

for path in ROOT.glob("*.html"):
    source = path.read_text(encoding="utf-8")

    metadata = SEO_METADATA.get(path.name)
    if metadata:
        title, description = metadata
        source = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', source, count=1, flags=re.DOTALL | re.IGNORECASE)
        source = re.sub(
            r'(<meta\s+name="description"\s+content=")[^"]*("\s*/?>)',
            lambda match: match.group(1) + html.escape(description, quote=True) + match.group(2),
            source,
            count=1,
            flags=re.DOTALL | re.IGNORECASE,
        )

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

    has_swiper = bool(re.search(r'class="[^"]*\bswiper\b', source, re.IGNORECASE))
    has_counter = bool(re.search(r'class="[^"]*\bcounter\b', source, re.IGNORECASE))
    has_skills = bool(re.search(r'class="[^"]*\bskills-progress', source, re.IGNORECASE))
    has_popup = bool(re.search(r'class="[^"]*\bpopup-video\b', source, re.IGNORECASE))

    if not has_swiper:
        source = re.sub(r'\s*<link[^>]+href=["\']css/swiper-bundle\.min\.css["\'][^>]*>', '', source)
        source = re.sub(r'\s*<script[^>]+src=["\']js/swiper-bundle\.min\.js["\'][^>]*></script>', '', source)
    if not has_counter:
        source = re.sub(r'\s*<script[^>]+src=["\']js/jquery\.counterup\.min\.js["\'][^>]*></script>', '', source)
    if not has_counter and not has_skills:
        source = re.sub(r'\s*<script[^>]+src=["\']js/jquery\.waypoints\.min\.js["\'][^>]*></script>', '', source)
    if not has_popup:
        source = re.sub(r'\s*<link[^>]+href=["\']css/magnific-popup\.css["\'][^>]*>', '', source)
        source = re.sub(r'\s*<script[^>]+src=["\']js/jquery\.magnific-popup\.min\.js["\'][^>]*></script>', '', source)

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

    # Refresh existing sharing metadata from the page title and description.
    # Attribute values use double quotes, so French apostrophes remain intact.
    title_match = re.search(r'<title>(.*?)</title>', source, re.DOTALL | re.IGNORECASE)
    desc_match = re.search(
        r'<meta\s+name="description"\s+content="([^"]*)"',
        source,
        re.DOTALL | re.IGNORECASE,
    )
    if title_match:
        social_title = html.escape(re.sub(r'\s+', ' ', title_match.group(1)).strip(), quote=True)
        source = re.sub(
            r'(<meta\s+property="og:title"\s+content=")[^"]*("\s*/?>)',
            lambda match: match.group(1) + social_title + match.group(2),
            source,
            count=1,
            flags=re.IGNORECASE,
        )
    if desc_match:
        social_description = html.escape(re.sub(r'\s+', ' ', desc_match.group(1)).strip(), quote=True)
        source = re.sub(
            r'(<meta\s+property="og:description"\s+content=")[^"]*("\s*/?>)',
            lambda match: match.group(1) + social_description + match.group(2),
            source,
            count=1,
            flags=re.IGNORECASE,
        )

    # Common copy fixes.
    replacements = {
        "Nos Réalisation": "Nos réalisations",
        "No Réalisation": "Nos réalisations",
        "Nos réalisationss": "Nos réalisations",
        "Nettoyage apres travaux demenagement": "Nettoyage après travaux et déménagement",
        "contacter sur whatsapp": "Contacter sur WhatsApp",
        "Contacter Sur Whatsapp": "Contacter sur WhatsApp",
        "Luni à Vendredi": "Lundi à vendredi",
        "Dimarche": "Dimanche",
        "urgennce": "urgence",
        "Tous nos Services": "Tous nos services",
        "Aide Déménagement": "Aide au déménagement",
        "Soin des Animaux": "Soins des animaux",
        '<a href="/services-numeriques">Soins des animaux</a>': '<a href="/services-soins-animaux">Soins des animaux</a>',
        ">adalbertofurtado.com<": ">adalberto.fr<",
        "<h3>Adresse</h3>": "<h3>Zone d’intervention</h3>",
        "<p>12 Avenue Charles Moulet, 13500 Martigues</p>": "<p>Martigues et alentours</p>",
    }
    for old, new in replacements.items():
        source = source.replace(old, new)

    if path.name == "index.html":
        # Keep the homepage focused: these legacy blocks repeat services or use
        # weak vanity metrics without helping visitors request a quote.
        for start, end in (
            ("Client Slider Section Start", "Client Slider Section End"),
            ("Chiffres Clés Start", "Chiffres Clés End"),
            ("Meilleurs Services Start", "Meilleurs Services End"),
        ):
            source = re.sub(
                rf'\s*<!-- {re.escape(start)} -->.*?<!-- {re.escape(end)} -->\s*',
                "\n",
                source,
                count=1,
                flags=re.DOTALL,
            )

    # Public navigation uses canonical, extensionless routes. Physical files keep
    # their .html suffix because Vercel maps them through cleanUrls.
    source = re.sub(
        r'(?P<prefix>\bhref=["\'])(?P<url>[^"\']+)(?P<suffix>["\'])',
        lambda match: (
            match.group("prefix")
            + clean_internal_url(match.group("url"))
            + match.group("suffix")
        ),
        source,
        flags=re.IGNORECASE,
    )

    # Version the site-owned assets globally. Vendor libraries are immutable,
    # while these two files change with normal site releases.
    source = re.sub(
        r'href="css/custom\.css(?:\?v=[^"]+)?"',
        'href="css/custom.css?v=20260826-3"',
        source,
        count=1,
    )
    source = re.sub(
        r'src="js/function\.js(?:\?v=[^"]+)?"',
        'src="js/function.js?v=20260826-3"',
        source,
        count=1,
    )

    # Image-only service/project links need an accessible name for screen readers.
    def label_visual_link(match):
        route = match.group("route")
        label = ROUTE_LABELS.get(route)
        if not label:
            return match.group(0)
        return f'<a aria-label="{label}"{match.group("before")}href="{route}"{match.group("after")}>'

    source = re.sub(
        r'<a(?![^>]*\baria-label=)(?P<before>[^>]*?)href="(?P<route>/[^"]+)"(?P<after>[^>]*?\bdata-cursor-text="Voir"[^>]*)>',
        label_visual_link,
        source,
        flags=re.IGNORECASE,
    )
    source = re.sub(
        r'(?P<prefix>\bcontent=["\'])(?P<url>https://giosmart-services\.fr/[^"\']+)(?P<suffix>["\'])',
        lambda match: (
            match.group("prefix")
            + clean_internal_url(match.group("url"))
            + match.group("suffix")
        ),
        source,
        flags=re.IGNORECASE,
    )

    # Mark the current service in the shared sidebar for visual and assistive
    # navigation. Limit the change to this component so header links stay clean.
    current_route = SERVICE_ROUTES.get(path.name)
    if current_route:
        def mark_current_service(match):
            sidebar = match.group(0)
            sidebar = sidebar.replace(' class="is-active"', '')
            sidebar = sidebar.replace(' aria-current="page"', '')
            return sidebar.replace(
                f'<a href="{current_route}"',
                f'<a class="is-active" href="{current_route}" aria-current="page"',
                1,
            )

        source = re.sub(
            r'<div class="service-catagery-list\b.*?</div>',
            mark_current_service,
            source,
            count=1,
            flags=re.DOTALL,
        )

    if path.name == "404.html":
        if 'name="robots"' not in source:
            source = source.replace(
                '<meta name="author"',
                '<meta name="robots" content="noindex, follow" />\n    <meta name="author"',
                1,
            )
        source = re.sub(r'\s*<link\s+rel="canonical"[^>]*>', '', source, count=1)
        source = re.sub(r'\s*<meta\s+property="og:url"[^>]*>', '', source, count=1)

    source = source.replace('decoding="async" decoding="async"', 'decoding="async"')

    path.write_text(source, encoding="utf-8")

sitemap = ROOT / "sitemap.xml"
if sitemap.exists():
    sitemap_source = sitemap.read_text(encoding="utf-8")
    sitemap_source = re.sub(
        r"https://giosmart-services\.fr/([^<]+?)\.html(?=</loc>)",
        r"https://giosmart-services.fr/\1",
        sitemap_source,
    )
    sitemap_source = re.sub(r"<lastmod>[^<]+</lastmod>", "<lastmod>2026-08-26</lastmod>", sitemap_source)
    sitemap.write_text(sitemap_source, encoding="utf-8")
