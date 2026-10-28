# BindRaft marketing site (static)

Static HTML/CSS/JS. Generated from `_src/build.py` (shared chrome, content, JSON-LD, robots.txt, sitemap.xml).
Legal copy: `_src/legal/site_legal.py`. Share image / icons: `_src/assets.py`. CSS: `css/styles.css`. JS: `js/main.js` (deferred).

```bash
python3 _src/assets.py   # og.png, logo, favicons (only when the artwork changes)
python3 _src/build.py    # regenerate all pages
python3 -m http.server 8765   # links are root-absolute (/work/), so serve from the repo root
```

## Before going public
- `SITE` in build.py is the preview host; switch to `https://bindraft.com` (canonicals, og:url, sitemap).
- `ROBOTS` in build.py is `noindex,nofollow`; remove when the Founder approves indexing.
- Contact form and intro-call picker compose an email in the visitor's mail app (mailto). Swap for a real endpoint / scheduler when available and update the Privacy & Cookie pages if that adds processing or cookies.
- `vercel.json`: trailing-slash URLs plus 308s from `*/index.html` and old `/work/*.html` case URLs.

## Sources
- Contact, hours (Sat–Thu 9:00–18:00), address, socials, "since 2023": live bindraft.com.
- Client facts: worldpacintl.com, silkwaysgroup.com, wellpacpolymers.net (https; http returns 500). All three show a Laravel fingerprint; World Pac and Wellpac footers credit "Developed by BindRaft".
- Fonts: Geist / Geist Mono (OFL), self-hosted latin subset in `/fonts`.
