"""Construit le site dans dist/ à partir de src/ et assets/.

python3 build.py
"""
import datetime
import html as H
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
DIST = os.path.join(ROOT, "dist")
SITE_URL = "https://www.ackconsulting.fr"

# Menus (repris du site Sintra)
PRESTATIONS = [
    ("Direction commerciale externalisée", "/directrice-commerciale-externalisee", "Direction, management et pilotage, à temps partagé", "📋"),
    ("Manager de transition commercial", "/manager-de-transition-commercial", "En urgence", "⚡"),
    ("Structuration commerciale – Zéro Lead Perdu", "/zero-lead-perdu", "Process, pipeline et KPI", "🎯"),
    ("Coaching commercial & manager", "/coaching", "Commercial & managérial", "🏋️"),
    ("Offre spéciale organismes de formation", "/prestation-of", "Pour les organismes de formation", "🎓"),
    ("ACK Sales Squad", "/ack-sales-squad", "Force commerciale externalisée", "🚀"),
    ("Traitement de leads", "/traitement-leads", "Partiel ou total", "📥"),
    ("ACK Sales Match", "https://www.acksalesmatch.fr", "Trouver un commercial freelance", "🤝"),
]
APROPOS = [
    ("Nos modalités d'intervention", "/nos-modalites", "⚙️"),
    ("Accompagnement stratégique", "/accompagnement", "📈"),
]


def ext(href):
    return ' target="_blank" rel="noopener noreferrer"' if href.startswith("http") else ""


def menus():
    e = H.escape
    return {
        "PRESTATIONS_DESKTOP": "".join(
            f'<a href="{h}"{ext(h)} class="flex items-start gap-3 px-5 py-4 hover:bg-[#f6f6f8] transition-colors group">'
            f'<span class="text-xl shrink-0 mt-0.5">{i}</span><div><p class="font-semibold text-sm text-[#1a1a1a] group-hover:text-[#1e8482] transition-colors">{e(l)}</p>'
            f'<p class="text-xs text-gray-500 mt-0.5">{e(d)}</p></div></a>' for l, h, d, i in PRESTATIONS),
        "PRESTATIONS_MOBILE": "".join(
            f'<a href="{h}"{ext(h)} class="flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm text-gray-700 hover:bg-[#f6f6f8] transition-colors"><span>{i}</span><span>{e(l)}</span></a>'
            for l, h, d, i in PRESTATIONS),
        "APROPOS_DESKTOP": "".join(
            f'<a href="{h}" class="flex items-center gap-3 px-5 py-4 hover:bg-[#f6f6f8] transition-colors group"><span class="text-xl shrink-0">{i}</span>'
            f'<p class="font-semibold text-sm text-[#1a1a1a] group-hover:text-[#1e8482] transition-colors">{e(l)}</p></a>' for l, h, i in APROPOS),
        "APROPOS_MOBILE": "".join(
            f'<a href="{h}" class="flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm text-gray-700 hover:bg-[#f6f6f8] transition-colors"><span>{i}</span><span>{e(l)}</span></a>'
            for l, h, i in APROPOS),
    }


def light_form(form):
    """Le formulaire de contact est conçu pour un fond sombre ; dans la fenêtre « Nous contacter » (fond blanc), on le passe en version claire."""
    return (form.replace("text-white/80", "text-gray-700")
                .replace("bg-white/10 border border-white/20", "bg-white border-2 border-gray-200")
                .replace("rounded-xl text-white ", "rounded-xl text-gray-900 "))


def read(p):
    return open(p, encoding="utf-8").read()


def partial(name):
    return read(os.path.join(SRC, "partials", name))


def strip_comments(s):
    """Aucune note interne dans le code publié."""
    return re.sub(r"<!--.*?-->", "", s, flags=re.S)


CERTIFICAT = "/assets/docs/certificat-qualiopi-ack-consulting.pdf"
LOGO_QUALIOPI = "img-e2c0ea0a6fac53b9f0effcc14d1eed81.png"
BLOC_CERTIFICAT = (
    '<section class="py-12 bg-[#f6f6f8]"><div class="max-w-4xl mx-auto px-6">'
    '<div class="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 flex flex-col md:flex-row items-center gap-6">'
    f'<img src="/assets/img/{LOGO_QUALIOPI}" alt="Qualiopi — Processus certifié — République Française" class="h-12 w-auto" loading="lazy" width="200" height="40"/>'
    '<div class="flex-1"><p class="font-bold text-[#1a1a1a] mb-1">ACK Consulting est certifié Qualiopi</p>'
    '<p class="text-gray-600 text-sm leading-relaxed">Certificat n° CERT_S1225_1438 délivré par CEVA Solution le 09/02/2026, valable jusqu&#x27;au 08/02/2029. '
    'La certification qualité a été délivrée au titre de la catégorie d&#x27;actions suivante : actions de formation.</p></div>'
    f'<a href="{CERTIFICAT}" target="_blank" rel="noopener" class="inline-flex items-center gap-2 bg-[#055388] text-white px-5 py-3 rounded-full text-sm font-bold hover:bg-[#1e8482] transition-colors">Voir le certificat (PDF)</a>'
    '</div></div></section>'
)


def lier_logos_qualiopi(html):
    """Chaque logo Qualiopi ouvre le certificat (exigence Qualiopi)."""
    def lier(m):
        avant = html[max(0, m.start() - 200):m.start()]
        if avant.rfind("<a ") > avant.rfind("</a>"):
            return m.group(0)
        return f'<a href="{CERTIFICAT}" target="_blank" rel="noopener" title="Voir notre certificat Qualiopi (PDF)">{m.group(0)}</a>'
    return re.sub(r'<img[^>]*' + re.escape(LOGO_QUALIOPI) + r'[^>]*>', lier, html)


def page_html(meta, body, blocks):
    head = [
        '<meta charset="utf-8"/>',
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>',
        f"<title>{H.escape(meta['title'])}</title>",
        *meta["meta"],
    ]
    if meta.get("canonical"):
        head.append(f'<link rel="canonical" href="{meta["canonical"]}"/>')
    head += [
        '<link rel="icon" type="image/png" href="/assets/img/img-74454af550a3fb61ba227ab610003b56.png"/>',
        '<link rel="apple-touch-icon" href="/assets/img/img-74454af550a3fb61ba227ab610003b56.png"/>',
        '<link rel="stylesheet" href="/assets/site.css"/>',
        '<link rel="stylesheet" href="/assets/ack.css"/>',
        '<link rel="stylesheet" href="/assets/complements.css"/>',
    ]
    head += [f'<script type="application/ld+json">{j}</script>' for j in meta.get("jsonld", [])]
    header = blocks["header"] if meta["header"] else ""
    footer = blocks.get("footer-" + meta["footer"], "")
    return (
        '<!DOCTYPE html>\n<html lang="fr" class="__variable_d8ebd1 __variable_fab2aa">\n<head>\n' + "\n".join(head) + "\n</head>\n"
        '<body class="__className_d8ebd1 text-[#1a1a1a] bg-white antialiased">\n'
        + header
        + f'\n<main class="{H.escape(meta["main_class"])}">\n{body}\n</main>\n'
        + footer
        + "\n" + blocks["cookie-banner"]
        + '\n<script src="/assets/site.js" defer></script>\n<script src="/assets/consent.js" defer></script>\n<script src="/assets/suivi.js" defer></script>'
        + ('\n<script src="/assets/video.js" defer></script>' if "data-video=" in body else "")
        + '\n</body>\n</html>\n'
    )


def build():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"))

    year = str(datetime.date.today().year)
    header = partial("header.html")
    for k, v in menus().items():
        header = header.replace("{{" + k + "}}", v)
    header = header.replace("{{CONTACT_FORM}}", light_form(partial("contact-form.html")))
    blocks = {"header": header, "cookie-banner": partial("cookie-banner.html")}
    for f in os.listdir(os.path.join(SRC, "partials")):
        if f.startswith("footer-"):
            blocks[f[:-5]] = partial(f).replace("{{ANNEE}}", year)

    pages = []
    for dp, _, fs in os.walk(os.path.join(SRC, "pages")):
        for f in sorted(fs):
            if not f.endswith(".html"):
                continue
            raw = read(os.path.join(dp, f))
            m = re.match(r"<!--page\n(.*?)\n-->\n", raw, re.S)
            meta = json.loads(m.group(1))
            body = raw[m.end():]
            rel_page = os.path.relpath(os.path.join(dp, f), os.path.join(SRC, "pages"))
            if rel_page.startswith("formations"):
                body = body + "\n" + BLOC_CERTIFICAT
            out = lier_logos_qualiopi(page_html(meta, body, blocks))
            out = strip_comments(out)
            rel = os.path.relpath(os.path.join(dp, f), os.path.join(SRC, "pages"))
            target = os.path.join(DIST, rel)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            open(target, "w", encoding="utf-8").write(out)
            pages.append(meta)

    # sitemap : mêmes adresses qu'aujourd'hui (pages en noindex et /liens exclues)
    sitemap_paths = [l.strip() for l in read(os.path.join(ROOT, "src", "sitemap.txt")).splitlines() if l.strip()]
    today = datetime.date.today().isoformat()
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml += [f"<url><loc>{SITE_URL}{'' if p == '/' else p}</loc><lastmod>{today}</lastmod></url>" for p in sitemap_paths]
    xml.append("</urlset>")
    open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml) + "\n")
    shutil.copy(os.path.join(SRC, "robots.txt"), os.path.join(DIST, "robots.txt"))
    print(f"{len(pages)} pages construites dans dist/")


if __name__ == "__main__":
    build()
