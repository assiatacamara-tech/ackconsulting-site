"""Retrouve le texte des réponses FAQ (affichées seulement au clic sur Sintra) dans les scripts JS de chaque page."""
import re, glob, json, html, sys, os
ROOT = sys.argv[1]  # snapshot/www.ackconsulting.fr
STR = re.compile(r'"((?:[^"\\]|\\.)*)"')

def js_strings(src):
    out = []
    for m in STR.finditer(src):
        try:
            out.append((m.start(), json.loads('"' + m.group(1).replace("\\x", "\\u00") + '"')))
        except Exception:
            pass
    return out

def norm(t):
    return re.sub(r"\s+", " ", t.replace("\u2019", "'")).strip()

res = {}
for page in sorted(glob.glob(f"{ROOT}/**/*.html", recursive=True)):
    rel = os.path.relpath(page, ROOT)[:-5]
    s = open(page, encoding="utf-8").read()
    m = re.search(r"<main\b.*?</main>", s, re.S)
    if not m:
        continue
    main = re.sub(r"<form\b.*?</form>", "", m.group(0), flags=re.S)
    qs = [html.unescape(re.sub(r"<[^>]+>", "", q)).strip()
          for q in re.findall(r"<button\b[^>]*>\s*<span[^>]*>(.*?)</span>", main, re.S)]
    if not qs:
        continue
    chunk = glob.glob(f"{ROOT}/_next/static/chunks/app/{rel}/page-*.js")
    strs = js_strings(open(chunk[0], encoding="utf-8").read()) if chunk else []
    # données intégrées dans la page (format Next.js) : on décode les blocs self.__next_f.push
    for blob in re.findall(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)', s):
        try:
            strs += js_strings(json.loads(blob))
        except Exception:
            pass
    found = {}
    for q in qs:
        for i, (_, v) in enumerate(strs):
            if norm(v) == norm(q) and i + 1 < len(strs) and strs[i + 1][1] in ("a", "answer", "r", "reponse", "text"):
                found[q] = strs[i + 2][1].strip() if i + 2 < len(strs) else ""
                break
            if norm(v) == norm(q) and q not in found:
                # réponse = chaîne(s) suivante(s) jusqu'à la prochaine question
                ans = []
                for _, w in strs[i + 1:i + 12]:
                    if norm(w) in map(norm, qs):
                        break
                    if len(w) > 25 or ans:
                        if re.fullmatch(r"[\w\-\s:/\[\]#.%()]+", w) and " " not in w.strip():
                            continue  # classes / noms techniques
                        ans.append(w)
                    if ans and len(" ".join(ans)) > 40 and w.rstrip().endswith((".", "!", "?", ")")):
                        break
                found[q] = " ".join(ans).strip()
                break
    res[rel] = {"questions": qs, "reponses": found}
json.dump(res, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
tot = sum(len(v["questions"]) for v in res.values()); ok = sum(len([a for a in v["reponses"].values() if a]) for v in res.values())
print(ok, "/", tot)
for k, v in res.items():
    miss = [q for q in v["questions"] if not v["reponses"].get(q)]
    if miss: print(k, miss)
