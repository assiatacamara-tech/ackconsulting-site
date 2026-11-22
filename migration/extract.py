"""Extraction unique : transforme la copie du site Sintra (snapshot/) en sources propres (src/ et assets/).

Règle : on RECOPIE les contenus, on ne les réécrit pas.
Usage : python3 migration/extract.py
"""
import html as H
import json
import os
import re
import shutil
import sys
import hashlib

sys.path.insert(0, os.path.dirname(__file__))
import rsc  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(ROOT, "snapshot")
SITE = os.path.join(SNAP, "www.ackconsulting.fr")
SRC = os.path.join(ROOT, "src", "pages")
ASSETS = os.path.join(ROOT, "assets")
FAQ = json.load(open(os.path.join(ROOT, "migration", "faq.json"), encoding="utf-8"))

# ---------- fichiers statiques ----------
IMG = os.path.join(ASSETS, "img")
os.makedirs(IMG, exist_ok=True)
os.makedirs(os.path.join(ASSETS, "fonts"), exist_ok=True)
os.makedirs(os.path.join(ASSETS, "docs"), exist_ok=True)

media_dirs = [os.path.join(SITE, "_next/static/media"),
              os.path.join(SNAP, "ackconsulting.sintra.site/_next/static/media")]
for d in media_dirs:
    for f in os.listdir(d) if os.path.isdir(d) else []:
        src = os.path.join(d, f)
        if f.endswith(".woff2"):
            shutil.copy(src, os.path.join(ASSETS, "fonts", f))
        else:
            shutil.copy(src, os.path.join(IMG, f.replace("sintra-", "img-")))
logo_hd = [os.path.join(dp, f) for dp, _, fs in os.walk(os.path.join(SNAP, "eu.chat-img.sintra.ai")) for f in fs]
if logo_hd:
    shutil.copy(logo_hd[0], os.path.join(IMG, "logo-hd.png"))
for dp, _, fs in os.walk(os.path.join(SNAP, "images.pexels.com")):
    for f in fs:
        shutil.copy(os.path.join(dp, f), os.path.join(IMG, f.split("?")[0]))
for f in ("livret-accueil.pdf", "reglement-interieur.pdf"):
    if os.path.exists(os.path.join(SITE, f)):
        shutil.copy(os.path.join(SITE, f), os.path.join(ASSETS, "docs", f))
for dp, _, fs in os.walk(os.path.join(SNAP, "eu.chat-img.sintra.ai")):
    for f in fs:
        if f.endswith(".xlsx"):
            shutil.copy(os.path.join(dp, f), os.path.join(ASSETS, "docs", f))

css_src = [os.path.join(SITE, "_next/static/css", f) for f in os.listdir(os.path.join(SITE, "_next/static/css"))][0]
css = open(css_src, encoding="utf-8").read()
css = re.sub(r"url\((?:\.\./)*(?:/_next/static/)?media/([^)]+\.woff2)\)", r"url(/assets/fonts/\1)", css)
open(os.path.join(ASSETS, "site.css"), "w", encoding="utf-8").write(css)


def cf_decode(hexs):
    k = int(hexs[:2], 16)
    return "".join(chr(int(hexs[i:i + 2], 16) ^ k) for i in range(2, len(hexs), 2))


def fix_emails(s):
    """Adresses e-mail masquées par Cloudflare sur Sintra : on remet l'adresse en clair."""
    s = re.sub(r'href="/cdn-cgi/l/email-protection#([0-9a-f]+)"', lambda m: f'href="mailto:{cf_decode(m.group(1))}"', s)
    s = re.sub(r'<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="([0-9a-f]+)">\[email&#160;protected\]</a>',
               lambda m: f'<a href="mailto:{cf_decode(m.group(1))}">{cf_decode(m.group(1))}</a>', s)
    s = re.sub(r'<span class="__cf_email__" data-cfemail="([0-9a-f]+)">\[email&#160;protected\]</span>', lambda m: cf_decode(m.group(1)), s)
    return s


def fix_urls(s):
    s = fix_emails(s)
    s = re.sub(r"https://eu\.chat-img\.sintra\.ai/[^\"'\s]+/(Modele_plan_action_commercial_ACK_Consulting\.xlsx)", r"/assets/docs/\1", s)
    s = re.sub(r"(?:https://ackconsulting\.sintra\.site)?/_next/static/media/sintra-([0-9a-f]+\.(?:png|jpe?g|webp|svg))(?:\?[^\"'#\s]*)?(?:#0+)?",
               r"/assets/img/img-\1", s)
    s = re.sub(r"https://eu\.chat-img\.sintra\.ai/[^\"'\s]+/LOGO-1HD\.png", "/assets/img/logo-hd.png", s)
    # photos Pexels : laissées sur Pexels (comme aujourd'hui), le site de Pexels refuse les téléchargements automatiques
    s = re.sub(r'(href|src)="/(livret-accueil|reglement-interieur)\.pdf"', r'\1="/assets/docs/\2.pdf"', s)
    return s


def abs_img(s):
    """Dans les balises meta / JSON-LD, les images doivent être des adresses complètes."""
    return s.replace('"/assets/img/', '"https://www.ackconsulting.fr/assets/img/')


# ---------- formulaires ----------
FORM_IDS = {
    ("how_heard",): "newsletter",
    ("name", "email", "phone", "message", "how_heard"): "contact",
    ("name", "email", "company", "website", "sector", "services", "target", "message", "how_heard"): "partenaire",
    ("prenom", "nom", "email", "tel", "entreprise", "enjeu", "how_heard"): "diagnostic",
    ("email-lm", "how_heard"): "diagnostic-pdf",
    ("name", "email", "phone", "profil", "taille", "objectif", "delai", "message", "how_heard"): "qualification-formation",
    ("prenom", "nom", "email", "tel", "entreprise", "commerciaux", "how_heard"): "sales-squad",
}
SUCCESS = {
    "newsletter": ["Inscription confirmée ! Bienvenue dans la communauté ACK."],
    "contact": ["Message envoyé !", "Je vous recontacte sous 24h."],
    "partenaire": ["Candidature reçue !", "Merci pour votre intérêt. Je prends connaissance de votre profil et vous recontacte sous 48h."],
    "diagnostic": ["Demande reçue !", "Je reviens vers vous sous 24h pour convenir d'un créneau. À très vite."],
    "diagnostic-pdf": ["Votre Diagnostic Express vous a été envoyé par email.", "Vérifiez votre boîte de réception (et vos spams)."],
    "qualification-formation": ["Demande reçue !", "Merci pour ces informations. Je prends connaissance de votre situation et vous recontacte sous 24h avec une recommandation adaptée."],
    "sales-squad": ["Demande reçue !", "Je reviens vers vous sous 24h pour convenir d'un créneau de 20 minutes. À très vite."],
}
forms_seen = {}


def netlify_form(m, page):
    attrs, body = m.group(1), m.group(2)
    names = tuple(re.findall(r'name="([^"]+)"', body))
    fid = FORM_IDS.get(names)
    if not fid:
        raise SystemExit(f"Formulaire inconnu sur {page}: {names}")
    # champs e-mail sans nom (newsletter)
    body = re.sub(r'<input type="email"(?![^>]*name=)', '<input type="email" name="email"', body)
    forms_seen.setdefault(fid, []).append(page)
    attrs = re.sub(r'\s*(name|method|action|data-netlify|data-form)="[^"]*"', "", attrs)
    hidden = (f'<input type="hidden" name="form-name" value="{fid}"/>'
              f'<input type="hidden" name="page" value="/{page}"/>'
              '<p class="hidden" aria-hidden="true"><label>Ne pas remplir <input name="bot-field" tabindex="-1" autocomplete="off"/></label></p>')
    ok = "".join(f"<p>{H.escape(t)}</p>" for t in SUCCESS[fid])
    return (f'<form{attrs} name="{fid}" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-form="{fid}">'
            f"{hidden}{body}</form>"
            f'<div class="form-success hidden" data-success="{fid}" role="status">{ok}</div>'
            f'<p class="form-error hidden text-red-600 text-sm mt-2" data-error="{fid}" role="alert">Une erreur est survenue. Veuillez réessayer.</p>')


# ---------- FAQ : on ajoute les réponses (masquées) sous chaque question ----------
def inject_faq(main, page):
    data = FAQ.get(page)
    if not data:
        return main
    answers = data["reponses"]

    def repl(m):
        q = H.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
        a = answers.get(q)
        if not a:
            return m.group(0)
        if "<" not in a:
            a = "<p>" + H.escape(a, quote=False).replace("\n", "<br>") + "</p>"
        btn = m.group(1)
        btn = btn.replace("<button", '<button data-faq aria-expanded="false"', 1) if "aria-expanded" not in btn else btn.replace("<button", "<button data-faq", 1)
        return (f"{btn}{m.group(2)}{m.group(3)}"
                f'<div class="faq-answer hidden px-6 pb-5 text-gray-600 text-sm leading-relaxed">{a}</div>')

    return re.sub(r"(<button\b[^>]*>\s*<span[^>]*>)(.*?)(</span>.*?</button>)", repl, main, flags=re.S)


# ---------- variantes de pied de page ----------
def footer_variant(s):
    f = re.search(r"<footer\b.*?</footer>", s, re.S)
    if not f:
        return "aucun"
    f = f.group(0)
    if "py-6 gradient-dark" in f:
        return "mini-squad" if "En savoir plus sur ACK Sales Squad" in f else "mini"
    return "complet" if "Prêt à ne plus perdre un seul lead" in f else "sans-appel"


def head_meta(s):
    head = s[: s.find("</head>")]
    meta = {}
    meta["title"] = H.unescape(re.search(r"<title>(.*?)</title>", head, re.S).group(1))
    tags = []
    for t in re.findall(r"<meta\b[^>]*>", head):
        if re.search(r'name="(description|robots|keywords|twitter:[^"]+)"|property="og:[^"]+"', t):
            tags.append(abs_img(fix_urls(t)))
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', head)
    meta["canonical"] = canon.group(1) if canon else ""
    meta["meta"] = tags
    meta["description"] = H.unescape((re.search(r'<meta name="description" content="([^"]*)"', head) or [None, ""])[1])
    return meta


def jsonld(s):
    out = []
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        out.append(abs_img(fix_urls(j)))
    return out


if os.path.isdir(SRC):
    shutil.rmtree(SRC)
pages = []
for dp, _, fs in os.walk(SITE):
    if "/_next" in dp:
        continue
    for f in fs:
        if not f.endswith(".html"):
            continue
        path = os.path.relpath(os.path.join(dp, f), SITE)[:-5]
        s = open(os.path.join(dp, f), encoding="utf-8").read()
        m = re.search(r"<main\b[^>]*>(.*)</main>", s, re.S)
        main_tag = re.search(r"<main\b[^>]*>", s).group(0)
        main = m.group(1)
        main = re.sub(r"<script\b.*?</script>", "", main, flags=re.S)
        main = re.sub(r"<!-- -->|<!--\$-->|<!--/\$-->|<!--\$\?-->|<template[^>]*></template>", "", main)
        main = fix_urls(main)
        main = inject_faq(main, path)
        main = re.sub(r"<form\b([^>]*)>(.*?)</form>", lambda mm: netlify_form(mm, path), main, flags=re.S)
        meta = head_meta(s)
        meta["path"] = "/" if path == "index" else "/" + path
        meta["header"] = "<header" in s
        meta["footer"] = footer_variant(s)
        meta["main_class"] = H.unescape(re.search(r'class="([^"]*)"', main_tag).group(1)) if "class=" in main_tag else ""
        body_jsonld = jsonld(s)
        out = os.path.join(SRC, path + ".html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write("<!--page\n" + json.dumps({**meta, "jsonld": body_jsonld}, ensure_ascii=False, indent=1) + "\n-->\n")
            fh.write(main.strip() + "\n")
        pages.append(meta["path"])

# formulaire de contact court : modèle réutilisé dans la fenêtre « Nous contacter »
coach = open(os.path.join(SITE, "coaching.html"), encoding="utf-8").read()
cf = re.search(r'<form\b[^>]*>.*?</form>', coach, re.S).group(0)
cf = re.sub(r"<!-- -->", "", fix_urls(cf))
cf = re.sub(r"<form\b([^>]*)>(.*?)</form>", lambda mm: netlify_form(mm, "fenetre-contact"), cf, flags=re.S)
os.makedirs(os.path.join(ROOT, "src", "partials"), exist_ok=True)
open(os.path.join(ROOT, "src", "partials", "contact-form.html"), "w", encoding="utf-8").write(cf)

print(len(pages), "pages extraites")
print({k: len(v) for k, v in forms_seen.items()})

# ---------- pieds de page (recopiés tels quels, une version par variante) ----------
seen = {}
for dp, _, fs in os.walk(SITE):
    if "/_next" in dp:
        continue
    for f in fs:
        if f.endswith(".html"):
            s = open(os.path.join(dp, f), encoding="utf-8").read()
            v = footer_variant(s)
            if v != "aucun" and v not in seen:
                seen[v] = re.search(r"<footer\b.*?</footer>", s, re.S).group(0)
for v, foot in seen.items():
    foot = re.sub(r"<!-- -->", "", fix_urls(foot))
    foot = re.sub(r"<form\b([^>]*)>(.*?)</form>", lambda mm: netlify_form(mm, "pied-de-page"), foot, flags=re.S)
    foot = re.sub(r"©\s*\d{4}", "© {{ANNEE}}", foot)
    open(os.path.join(ROOT, "src", "partials", f"footer-{v}.html"), "w", encoding="utf-8").write(foot)
print("pieds de page :", sorted(seen))

# ---------- page contact : le formulaire Zoho était inséré par script, on l'écrit directement ----------
cjs = [os.path.join(SITE, "_next/static/chunks/app/contact", f) for f in os.listdir(os.path.join(SITE, "_next/static/chunks/app/contact"))][0]
cs = open(cjs, encoding="utf-8").read()


def js_literal(src, start_token, quote):
    i = src.find(start_token) + len(start_token)
    j = i
    while True:
        j = src.find(quote, j)
        if src[j - 1] != "\\":
            return src[i:j]
        j += 1


zform = json.loads('"' + js_literal(cs, "innerHTML='", "'").replace("\\x", "\\u00").replace('"', '\\"').replace("\\'", "'") + '"').strip()
zjs = json.loads('"' + js_literal(cs, 'n.textContent="', '"').replace("\\x", "\\u00") + '"').strip()
open(os.path.join(ASSETS, "zoho-contact.js"), "w", encoding="utf-8").write(zjs + "\n")
cp = os.path.join(SRC, "contact.html")
c = open(cp, encoding="utf-8").read()
marker = "Réponse garantie sous 24h.</p><div></div>"
assert c.count(marker) == 1, "repère introuvable sur /contact"
c = c.replace(marker, "Réponse garantie sous 24h.</p><div>" + zform + '</div><script src="/assets/zoho-contact.js"></script>')
open(cp, "w", encoding="utf-8").write(c)
print("formulaire Zoho remis sur /contact")
