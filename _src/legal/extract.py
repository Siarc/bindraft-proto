#!/usr/bin/env python3
"""Turn the raw live-site HTML snapshots (fetched from bindraft.com) into clean JSON for build.py.
Text is copied as-is from the live pages; only markup is cleaned (classes dropped, Cloudflare-obfuscated
emails decoded, emoji bullets dropped, the site's own TOC removed because build.py renders one)."""
import json, os, re
from bs4 import BeautifulSoup, NavigableString
HERE = os.path.dirname(os.path.abspath(__file__))
KEEP = {"href", "id"}

def cf(hexs):
    k = int(hexs[:2], 16)
    return "".join(chr(int(hexs[i:i+2], 16) ^ k) for i in range(2, len(hexs), 2))

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("'", "")).strip("-")

def clean(p):
    s = BeautifulSoup(open(os.path.join(HERE, p + ".html")).read(), "html.parser")
    for t in s(["script", "style", "svg"]): t.decompose()
    m = s.find("main")
    for sp in m.select("[data-cfemail]"):
        a = sp.find_parent("a"); e = cf(sp["data-cfemail"])
        (a or sp).replace_with(BeautifulSoup(f'<a href="mailto:{e}">{e}</a>', "html.parser"))
    for t in m.find_all(True):
        t.attrs = {k: v for k, v in t.attrs.items() if k in KEEP}
    h1 = m.find("h1"); intro = h1.find_next("p")
    art = m.find("article")
    ps = art.find_all("p", recursive=False)
    updated = next(x.get_text(strip=True) for x in ps if x.get_text(strip=True).startswith("Last Updated"))
    out = dict(title=h1.get_text(strip=True), intro=intro.get_text(" ", strip=True),
               updated=updated.replace("Last Updated:", "").strip(), summary=None, sections=[])
    cur = None; mode = None
    for el in art.children:
        if isinstance(el, NavigableString):
            continue
        txt = el.get_text(" ", strip=True)
        if el.name == "p" and txt.startswith("Last Updated"):
            continue
        if el.name == "h2":
            if txt == "Quick Summary": mode = "summary"; continue
            if txt == "Table of Contents": mode = "toc"; continue
            mode = "sec"
            mt = re.match(r"(\d+)\.\s*(.*)", txt)
            num, title = (mt.group(1), mt.group(2)) if mt else (str(len(out["sections"]) + 1), txt)
            cur = dict(id=el.get("id") or slug(title), num=num, title=title, html="")
            out["sections"].append(cur); continue
        if mode == "summary":
            out["summary"] = (out["summary"] or "") + txt; continue
        if mode == "toc":
            continue
        if cur is not None:
            h = str(el)
            h = re.sub(r"[\U0001F300-\U0001FAFF]\s*", "", h)       # drop emoji bullets
            h = re.sub(r"\s*\n\s*", " ", h)
            h = re.sub(r"<div>\s*(<table>.*?</table>)\s*</div>", r'<div class="tbl">\1</div>', h, flags=re.S)
            cur["html"] += h + "\n"
    return out

if __name__ == "__main__":
    for p in ["privacy-policy", "terms-of-use", "cookie-policy"]:
        d = clean(p)
        json.dump(d, open(os.path.join(HERE, p + ".json"), "w"), indent=1, ensure_ascii=False)
        print(p, d["updated"], len(d["sections"]), "sections")
