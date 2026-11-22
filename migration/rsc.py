"""Lecture des données intégrées par Next.js (Sintra) dans chaque page : self.__next_f.push([1,"..."])."""
import re, json, html as H

def payload(page_html):
    parts = []
    for blob in re.findall(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)', page_html):
        try:
            parts.append(json.loads(blob))
        except Exception:
            pass
    rows = {}
    for line in "".join(parts).split("\n"):
        m = re.match(r"^([0-9a-f]+):(.*)$", line)
        if not m:
            continue
        body = m.group(2)
        if body[:1] in "[{\"":
            try:
                rows[m.group(1)] = json.loads(body)
            except Exception:
                pass
    return rows

def walk(node):
    yield node
    if isinstance(node, list):
        for x in node:
            yield from walk(x)
    elif isinstance(node, dict):
        for x in node.values():
            yield from walk(x)

def render(node):
    """Transforme un nœud React sérialisé en HTML simple (texte, liens, gras)."""
    if node is None or node is False or node is True:
        return ""
    if isinstance(node, str):
        return "" if node.startswith("$") and len(node) < 6 else H.escape(node, quote=False)
    if isinstance(node, (int, float)):
        return str(node)
    if isinstance(node, list):
        if len(node) == 4 and node[0] == "$" and isinstance(node[1], str):
            tag, props = node[1], node[3] or {}
            inner = render(props.get("children"))
            if tag.startswith("$"):
                tag = "a" if "href" in props else "span"
            attrs = ""
            for k, a in (("href", "href"), ("className", "class"), ("target", "target"), ("rel", "rel")):
                if k in props and isinstance(props[k], str):
                    attrs += f' {a}="{H.escape(props[k])}"'
            if tag in ("br", "img"):
                return f"<{tag}{attrs}>"
            return f"<{tag}{attrs}>{inner}</{tag}>"
        return "".join(render(x) for x in node)
    return ""

def qa_pairs(page_html):
    out = {}
    for row in payload(page_html).values():
        for n in walk(row):
            if isinstance(n, dict) and "q" in n and "a" in n and isinstance(n["q"], str):
                out.setdefault(n["q"].strip(), render(n["a"]).strip())
    return out
