# BindRaft redesign prototype (preview only)

Static HTML/CSS/JS clickable prototype. **Prototype, not production.** It does not touch bindraft.com, its DNS, or the Laravel app.

## Open locally
```bash
# from the repository root
python3 -m http.server 8765
# open http://localhost:8765/
```
Opening `index.html` directly from disk (file://) also works. All links are relative.

Pages are generated from `_src/build.py` (shared nav, footer and content). Edit there, then run `python3 _src/build.py`. CSS lives in `css/styles.css`, JS in `js/main.js`.

## Pages
index.html · work/index.html · work/world-pac.html · work/silkways-group.html · work/wellpac-polymers.html · services/index.html · about/index.html · contact/index.html · 404.html

## Real (from public sources)
- Contact: contact@bindraft.com · +880 1558 934599 · Road-10, House-31, Sector-9, Uttara, Dhaka 1230 · Sat–Thu 9–18
- Clients and live URLs: worldpacintl.com, silkwaysgroup.com, wellpacpolymers.net (this one may return HTTP 500)
- Client facts (World Pac est. 2004 / rebranded 2024, Gulshan-2, service lines; Silkways since 1995, 9 sister concerns; Wellpac export markets, polymers, and plant claims) come from the clients' own sites and are labelled as theirs.
- Laravel fingerprint observed for World Pac and Silkways (copper chips). Wellpac's stack is marked unconfirmed.
- Services are based on the current bindraft.com offer, trimmed to 5.

## Stubbed / placeholder
- **Calendar booking**: client-side slots (next 3 Mon–Fri weeks, sample "taken" slots). Clicking a slot opens a "Prototype stub — not a real booking" modal. Nothing is booked.
- **Contact form**: validates on the client side, then shows "Prototype stub — message not sent". Nothing is sent.
- **Case visuals**: typographic colour plates, not real screenshots of the client sites.
- **Years** in the Work index: "—" until the Founder confirms them.
- **Team**: "details on request" stub. No names, headcount or bios.
- **Copy**: process, values and service outcome lines are draft copy for Founder review. Case "constraints" are inferred from public positioning, not from client interviews.
- **404**: uses relative links, so it is correct when served at the site root. A production server would need absolute paths.
- Pages carry `noindex`.
