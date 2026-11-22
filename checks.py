"""Relecture automatique du site avant chaque mise en ligne.

Une seule vérification en échec => la mise en ligne est bloquée (code de sortie 1).
python3 checks.py            (après python3 build.py)
python3 checks.py --lock     (enregistre l'état actuel des blocs verrouillés, après validation par Assiata)
"""
import hashlib
import html as H
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
SNAP = os.path.join(ROOT, "snapshot", "www.ackconsulting.fr")
LOCKS = os.path.join(ROOT, "locks.json")
SITE = "https://www.ackconsulting.fr"

errors, count = [], 0


def check(ok, msg):
    global count
    count += 1
    if not ok:
        errors.append(msg)


def pages():
    for dp, _, fs in os.walk(DIST):
        if os.sep + "assets" in dp:
            continue
        for f in fs:
            if f.endswith(".html"):
                rel = os.path.relpath(os.path.join(dp, f), DIST)[:-5]
                yield ("/" if rel == "index" else "/" + rel), open(os.path.join(dp, f), encoding="utf-8").read()


def exists(url_path):
    p = url_path.split("#")[0].split("?")[0]
    if p in ("", "/"):
        return os.path.exists(os.path.join(DIST, "index.html"))
    p = p.lstrip("/")
    return any(os.path.isfile(os.path.join(DIST, c)) for c in (p, p + ".html", os.path.join(p, "index.html")))


def cf_decode(m):
    h = m.group(1)
    k = int(h[:2], 16)
    return "".join(chr(int(h[i:i + 2], 16) ^ k) for i in range(2, len(h), 2))


def text_of(fragment):
    fragment = re.sub(r"<!--.*?-->", "", fragment, flags=re.S)
    fragment = re.sub(r'<(?:span|a)\b[^>]*class="__cf_email__" data-cfemail="([0-9a-f]+)">.*?</(?:span|a)>', cf_decode, fragment)
    fragment = re.sub(r"<div id=\"crmWebToEntityForm\".*?</form>\s*</div>", " ", fragment, flags=re.S)
    fragment = re.sub(r"<(script|style)\b.*?</\1>", " ", fragment, flags=re.S)
    fragment = re.sub(r"<form\b.*?</form>", " ", fragment, flags=re.S)
    fragment = re.sub(r'<div class="faq-answer.*?</div>', " ", fragment, flags=re.S)
    fragment = re.sub(r'<div class="form-success.*?</div>|<p class="form-error.*?</p>', " ", fragment, flags=re.S)
    t = H.unescape(re.sub(r"<[^>]+>", " ", fragment))
    return re.sub(r"\s+", " ", t).strip()


all_pages = dict(pages())
check(len(all_pages) >= 48, f"Nombre de pages anormal : {len(all_pages)}")

for path, s in all_pages.items():
    where = f"[{path}]"
    # 1. Titre, description, adresse canonique, un seul H1
    check(len(re.findall(r"<title>.+?</title>", s)) == 1, f"{where} titre manquant ou en double")
    check(re.search(r'<meta name="description" content="[^"]{30,}"', s) is not None, f"{where} description Google manquante")
    noindex = 'content="noindex' in s
    if not noindex:
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        check(canon is not None, f"{where} adresse canonique manquante")
        if canon:
            check(canon.group(1).rstrip("/") == (SITE + ("" if path == "/" else path)).rstrip("/"),
                  f"{where} adresse canonique incorrecte : {canon.group(1)}")
    main = re.search(r"<main\b.*?</main>", s, re.S)
    check(main is not None, f"{where} contenu principal introuvable")
    if main and not noindex:
        check(len(re.findall(r"<h1\b", main.group(0))) == 1, f"{where} il faut exactement un titre H1 dans la page")

    # 2. Chaque lien interne et chaque image mène à un fichier qui existe
    for attr, url in re.findall(r'\b(href|src)="(/[^"]*)"', s):
        if url.startswith("//"):
            continue
        check(exists(url), f"{where} lien cassé : {url}")
    for img in re.findall(r"<img\b[^>]*>", s):
        check(re.search(r'\balt="[^"]+"', img) is not None, f"{where} image sans texte alternatif : {img[:80]}")

    # 3. Plus aucune trace de l'ancien hébergeur ni note interne
    check("sintra" not in s.lower(), f"{where} référence à Sintra restante")
    check("railway.app" not in s, f"{where} formulaire encore relié à l'ancien hébergeur")
    check("<!--" not in s, f"{where} commentaire (note interne) dans le code publié")

    # 4. Formulaires : enregistrés par Netlify, avec un nom
    for form in re.findall(r"<form\b[^>]*>", s):
        if "WebToLeadForm" in form:
            continue
        check('data-netlify="true"' in form and re.search(r'name="[a-z-]+"', form), f"{where} formulaire non relié : {form[:100]}")

    # 4a. Formulaire Zoho : aucun titre interne Zoho visible par les visiteurs
    check("zcwf_title'" not in s and "Leads-ack" not in s, f"{where} titre interne du formulaire Zoho visible")

    # 4e. Textes ACK au « nous » (hors blog) et couleurs de la charte uniquement
    if not path.startswith("/blog"):
        for mot in ("Je vous réponds", "Je vous recontacte", "envoyez-moi", "Envoyez-moi", "Retrouvez-moi", "Je reviens vers vous", "Je prends en charge", "Ma méthode", "Mes services", "Pourquoi me ", "J&#x27;ai ", "j&#x27;ai ", "J&#x27;interviens", "j&#x27;interviens"):
            check(mot not in s, f"{where} texte à la première personne (« {mot} ») au lieu du « nous »")
    for vieux in ("1a6b5a", "2b8a76", "132833", "2364a1", "a06848", "c8a45e", "1fb6a6", "1477d6", "090a0a"):
        check(vieux not in s.lower(), f"{where} couleur hors charte : #{vieux}")

    # 4b. Fenêtre « Nous contacter » (fond blanc) : aucun titre ni champ écrit en blanc
    modal = re.search(r"data-contact-modal.*?</form>", s, re.S)
    if modal:
        for tag in re.findall(r"<(?:label|input|textarea|select)\b[^>]*>", modal.group(0)):
            check(not re.search(r'class="[^"]*\btext-white\b', tag), f"{where} texte blanc invisible dans la fenêtre Nous contacter : {tag[:90]}")

    # 4c. RGPD : chaque formulaire a une case de consentement obligatoire et un lien vers la politique de confidentialité
    for fm in re.finditer(r"<form\b(.*?)>(.*?)</form>", s, re.S):
        fbody = fm.group(2)
        if "WebToLeadForm" in fm.group(1):
            check('type="checkbox"' in fbody.replace("type = 'checkbox'", 'type="checkbox"') and "politique-de-confidentialite" in fbody,
                  f"{where} formulaire Zoho sans case de consentement")
            continue
        check(re.search(r'<input type="checkbox"[^>]*name="consentement"[^>]*required', fbody) is not None,
              f"{where} formulaire sans case de consentement RGPD obligatoire")
        check("/a-propos/politique-de-confidentialite" in fbody, f"{where} formulaire sans lien vers la politique de confidentialité")

    # 4d. Cookies : rien de Google avant consentement ; bandeau présent avec « Tout refuser » aussi visible que « Tout accepter »
    check("googletagmanager.com" not in s and "google-analytics.com" not in s, f"{where} outil Google chargé sans consentement")
    check("data-cookie-banner" in s and "data-cookie-refuse" in s and "data-cookie-accept" in s and "/assets/consent.js" in s,
          f"{where} bandeau cookies absent ou incomplet")

    # 5. Chaque question de FAQ a sa réponse
    for m in re.finditer(r"<button data-faq\b.*?</button>(.{0,40})", s, re.S):
        check('class="faq-answer' in m.group(1), f"{where} question de FAQ sans réponse")

    # 6. Les textes sont identiques à ceux du site Sintra (on recopie, on ne réécrit pas)
    modifiees = [l.strip() for l in open(os.path.join(ROOT, "migration", "pages-modifiees.txt"), encoding="utf-8") if l.startswith("/")]
    check(path not in modifiees or not path.startswith("/a-propos/") or "Dernière mise à jour :" in s, f"{where} page légale modifiée sans date de mise à jour")
    snap_file = os.path.join(SNAP, ("index" if path == "/" else path.lstrip("/")) + ".html")
    if os.path.exists(snap_file) and main and path not in modifiees:
        old = re.search(r"<main\b.*?</main>", open(snap_file, encoding="utf-8").read(), re.S)
        if old:
            # Accents affichés en code sur l'ancien site (« r\\u00e9ussi ») : corrigés au lot 1, comparés décodés
            a = re.sub(r"\\u([0-9a-fA-F]{4})", lambda u: chr(int(u.group(1), 16)), text_of(old.group(0)))
            b = text_of(main.group(0))
            if a != b:
                i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
                check(False, f"{where} texte différent du site actuel vers : « …{a[max(0, i - 40):i + 40]}… » / « …{b[max(0, i - 40):i + 40]}… »")
            else:
                check(True, "")

# 6b. Chaque classe de style utilisée existe dans la feuille de style (sinon l'élément s'affiche mal ou pas du tout)
CSS = open(os.path.join(ROOT, "assets", "site.css"), encoding="utf-8").read() + open(os.path.join(ROOT, "assets", "ack.css"), encoding="utf-8").read()
HOOKS = {"faq-answer", "form-success", "form-error"}
def css_has(c):
    return "." + re.sub(r"([:\[\]#/.%()&',>+~=])", r"\\\1", c) in CSS
missing = {}
for path, s in all_pages.items():
    s2 = re.sub(r"<div id=\"crmWebToEntityForm\".*?</form>\s*</div>", "", s, flags=re.S)
    for cl in re.findall(r'class="([^"]+)"', s2):
        for c in cl.split():
            if c not in HOOKS and not c.startswith("__") and not css_has(c):
                missing.setdefault(c, path)
snap_missing = set()
if os.path.isdir(SNAP):
    for c in list(missing):
        if any(f'"{c}"' in l or f" {c} " in l or f'"{c} ' in l or f' {c}"' in l for l in [open(os.path.join(dp, f), encoding="utf-8").read() for dp, _, fs in os.walk(SNAP) if "_next" not in dp for f in fs if f.endswith(".html")][:60]):
            snap_missing.add(c)
for c, p in missing.items():
    if c not in snap_missing:
        check(False, f"[{p}] classe de style inexistante : {c}")

# 7. Plan du site : chaque adresse existe, aucune page masquée de Google
sm = open(os.path.join(DIST, "sitemap.xml"), encoding="utf-8").read()
for loc in re.findall(r"<loc>([^<]+)</loc>", sm):
    p = loc.replace(SITE, "") or "/"
    check(p in all_pages, f"[plan du site] adresse sans page : {p}")
    if p in all_pages:
        check('content="noindex' not in all_pages[p], f"[plan du site] page masquée de Google listée : {p}")

# 8. Mêmes champs pour un même formulaire (exigence Netlify)
fields = {}
for path, s in all_pages.items():
    for m in re.finditer(r'<form\b[^>]*data-netlify="true"[^>]*name="([^"]+)"[^>]*>(.*?)</form>|<form\b[^>]*name="([^"]+)"[^>]*data-netlify="true"[^>]*>(.*?)</form>', s, re.S):
        name = m.group(1) or m.group(3)
        body = m.group(2) or m.group(4)
        fs = tuple(sorted(set(re.findall(r'\bname="([^"]+)"', body)) - {"form-name", "page", "bot-field"}))
        fields.setdefault(name, set()).add(fs)
zoho_js = open(os.path.join(ROOT, "netlify", "functions", "zoho.mjs"), encoding="utf-8").read()
for name in fields:
    check(f'"{name}"' in zoho_js or f"\n  {name}:" in zoho_js, f"[formulaire {name}] non prévu dans l'envoi vers Zoho (netlify/functions/zoho.mjs)")
for name, variants in fields.items():
    check(len(variants) == 1, f"[formulaire {name}] champs différents selon les pages : {variants}")

# 10. Lot 1 (22/11/2026) : accents affichés en code, images lourdes, titres et descriptions trop longs,
#     données structurées lisibles, articles balisés, concurrence avec acksalesmatch.fr
for path, page in pages():
    visible = re.sub(r"<(script|style)\b.*?</\1>", " ", page, flags=re.S)
    check(not re.search(r"\\u[0-9a-fA-F]{4}", visible), f"[{path}] accent affiché en code (\\u00e9…)")
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
        try:
            json.loads(j)
            ok_json = True
        except ValueError:
            ok_json = False
        check(ok_json, f"[{path}] données structurées illisibles")
    if 'content="noindex' in page:
        continue
    t = re.search(r"<title>(.*?)</title>", page, re.S)
    check(t and len(H.unescape(t.group(1))) <= 65, f"[{path}] titre Google de plus de 65 caractères")
    d = re.search(r'<meta name="description" content="([^"]*)"', page)
    check(d and len(H.unescape(d.group(1))) <= 175, f"[{path}] description Google de plus de 175 caractères")
    check(not (t and re.search(r"commercial freelance", t.group(1), re.I)), f"[{path}] titre visant « commercial freelance » (réservé à acksalesmatch.fr)")
    if path.startswith("/blog/"):
        check('"@type": "Article"' in page or '"@type":"Article"' in page, f"[{path}] article sans données structurées Article")
for dp, _, fs in os.walk(os.path.join(DIST, "assets", "img")):
    for f in fs:
        size = os.path.getsize(os.path.join(dp, f))
        check(size <= 400 * 1024, f"[assets/img/{f}] image de plus de 400 Ko ({size // 1024} Ko) : la convertir en WebP")

# 9. Blocs verrouillés : toute modification d'un bloc validé bloque la mise en ligne
locked = sorted(os.path.join("src", "partials", f) for f in os.listdir(os.path.join(ROOT, "src", "partials")))
locked += ["assets/site.css", "assets/site.js", "assets/consent.js", "assets/ack.css", "assets/video.js"]
state = {f: hashlib.sha256(open(os.path.join(ROOT, f), "rb").read()).hexdigest() for f in locked}
if "--lock" in sys.argv:
    json.dump(state, open(LOCKS, "w"), indent=1, sort_keys=True)
    print("Blocs verrouillés enregistrés :", len(state))
    sys.exit(0)
if os.path.exists(LOCKS):
    saved = json.load(open(LOCKS))
    for f, h in state.items():
        if f not in saved:
            print(f"(info) nouveau bloc en attente de validation par Assiata : {f}")
            continue
        check(saved.get(f) == h, f"[bloc verrouillé] {f} a été modifié sans validation (relancer « python3 checks.py --lock » après accord)")

if errors:
    print(f"ÉCHEC : {len(errors)} vérification(s) en échec sur {count}. Mise en ligne bloquée.\n")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"OK : {count} vérifications réussies.")
