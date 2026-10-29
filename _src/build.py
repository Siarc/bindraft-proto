#!/usr/bin/env python3
"""Generates the static site pages from shared chrome. Run: python3 _src/build.py"""
import os, json, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_src", "legal"))
# Absolute host for canonical / og:url / sitemap. Switch to https://bindraft.com at launch.
SITE = "https://bindraft-proto-preview.vercel.app"
ROBOTS = "noindex,nofollow"   # preview: leave as-is until the Founder approves going public
SAME_AS = ["https://www.linkedin.com/company/bindraft", "https://www.facebook.com/BindRaft/", "https://github.com/bindraft"]
SITEMAP = []

EMAIL = "contact@bindraft.com"; PHONE = "+880 1558 934599"; TEL = "+8801558934599"
ADDR = "Road-10, House-31, Sector-9, Uttara, Dhaka 1230"

CASES = {
 "world-pac": dict(name="World Pac International", short="World Pac", sector="Courier & logistics", platform="Web · Laravel",
   url="https://worldpacintl.com/", urltext="worldpacintl.com", bg="#1D1B19", fg="#F2F0EB", cls="plate-wp"),
 "silkways-group": dict(name="Silkways Group", short="Silkways", sector="Diversified group · 10 concerns", platform="Web · Laravel",
   url="https://silkwaysgroup.com/", urltext="silkwaysgroup.com", bg="#D9D3C7", fg="#0E0D0C", cls="plate-sw"),
 "wellpac-polymers": dict(name="Wellpac Polymers", short="Wellpac", sector="Export packaging manufacturing", platform="Web · Laravel",
   url="https://wellpacpolymers.net/", urltext="wellpacpolymers.net", bg="#C9BBA9", fg="#0E0D0C", cls="plate-wl"),
}
ORDER = ["world-pac", "silkways-group", "wellpac-polymers"]

def plate(slug, big=False):
    c = CASES[slug]
    if slug == "world-pac":
        body = f'''<div class="top"><span>worldpacintl.com</span><span>Gulshan-2 · Dhaka</span></div>
<div><div class="big">World<br>Pac</div><div class="bar"></div>
<div class="win"><div class="row"><span>Track shipment</span><span>→</span></div><div class="fill"></div><div class="fill c"></div></div></div>'''
    elif slug == "silkways-group":
        tiles = ["Aviation","Cargo","Tours","Trade","Smart cards","IT","Wellpac","Alamsons","Farisha","Silk Spoon"]
        t = "".join(f'<div class="{"on" if i==6 else ""}">{x}</div>' for i,x in enumerate(tiles))
        body = f'''<div class="top"><span>silkwaysgroup.com</span><span>Since 1995</span></div>
<div><div class="big">Silk<br>ways</div><div class="bar"></div><div class="dots">{t}</div></div>'''
    else:
        body = f'''<div class="top"><span>wellpacpolymers.net</span><span>100% export</span></div>
<div><div class="big">Well<br>pac</div><div class="bar"></div><div class="stripes"><i></i><i></i><i></i><i></i><i></i></div></div>'''
    return f'<div class="inner {c["cls"]}" aria-hidden="true">{body}</div>'

def url_of(path):
    return "/" + (path[:-len("index.html")] if path.endswith("index.html") else path)

def org():
    return {"@type": "ProfessionalService", "@id": SITE + "/#org", "name": "BindRaft", "url": SITE + "/",
        "logo": SITE + "/assets/logo.png", "image": SITE + "/assets/og.png",
        "description": "Software studio in Uttara, Dhaka: custom software, mobile apps, AI agents, digital consultancy, QA & security.",
        "email": EMAIL, "telephone": TEL, "foundingDate": "2023", "slogan": "Bind together to stay afloat",
        "address": {"@type": "PostalAddress", "streetAddress": "Road-10, House-31, Sector-9, Uttara", "addressLocality": "Dhaka",
                    "postalCode": "1230", "addressCountry": "BD"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"], "opens": "09:00", "closes": "18:00"}],
        "sameAs": SAME_AS}

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

def page(path, title, desc, body, current=None, schema=(), crumb=None, og_type="website"):
    r = "/"
    url = url_of(path)
    from html import escape
    title, desc = escape(title, quote=True), escape(desc, quote=True)
    is404 = path == "404.html"
    def nav_a(href, label, key, n):
        cur = ' aria-current="page"' if current == key else ""
        return f'<li><a href="/{href}"{cur}><sup>{n}</sup>{label}</a></li>'
    graph = [{"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "BindRaft", "publisher": {"@id": SITE + "/#org"}}, org()] + list(schema)
    if crumb: graph.append(crumbs([("Home", "/")] + crumb))
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    head_url = "" if is404 else f'<link rel="canonical" href="{SITE}{url}">\n'
    html = f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{ROBOTS}">
{head_url}<link rel="preload" href="/fonts/geist-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/geist-mono-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/styles.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#F2F0EB">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="BindRaft">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{url}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="BindRaft. We build the software businesses run on.">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/assets/og.png">
<script type="application/ld+json">{ld}</script>
<script src="/js/main.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav">
 <div class="wrap">
  <a class="logo" href="/" aria-label="BindRaft home">BindRaft<i></i></a>
  <nav aria-label="Primary"><ul id="primary-nav">
   {nav_a("work/","Work","work","01")}
   {nav_a("services/","Services","services","02")}
   {nav_a("about/","About","about","03")}
   {nav_a("contact/","Contact","contact","04")}
  </ul></nav>
  <div class="nav-right">
   <a class="btn sm" href="/contact/#book">Start a project <span class="arr">→</span></a>
   <button class="menu-btn" type="button" aria-expanded="false" aria-controls="primary-nav">Menu</button>
  </div>
 </div>
</header>
<main id="main">
{body.replace("{r}", r)}
</main>
<footer class="foot">
 <div class="wrap">
  <div class="foot-grid">
   <div><a href="/" class="big" aria-label="BindRaft home">BindRaft<i></i></a>
    <p class="muted" style="margin-top:16px;max-width:36ch">Product-engineering studio in Uttara, Dhaka. Web, mobile, AI agents.</p></div>
   <div><p class="fh">Index</p><ul>
    <li><a href="/work/">Work</a></li><li><a href="/services/">Services</a></li>
    <li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li></ul></div>
   <div><p class="fh">Talk</p><ul>
    <li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="tel:{TEL}">{PHONE}</a></li>
    <li><a href="/contact/#book">Book a call</a></li></ul></div>
   <div><p class="fh">Studio</p><address>{ADDR}</address><p class="muted" style="margin-top:8px">Sat–Thu · 9:00–18:00 (Dhaka)</p></div>
   <div><p class="fh">Legal</p><ul>
    <li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms-of-use/">Terms of Use</a></li>
    <li><a href="/cookie-policy/">Cookie Policy</a></li></ul></div>
  </div>
  <div class="foot-base"><span>© 2026 BindRaft</span><span><a href="{SAME_AS[0]}" rel="noopener">LinkedIn</a> · <a href="{SAME_AS[1]}" rel="noopener">Facebook</a> · <a href="{SAME_AS[2]}" rel="noopener">GitHub</a></span></div>
 </div>
</footer>
</body>
</html>
'''
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(html)
    if not is404: SITEMAP.append(url)
    print("wrote", path)

SERVICES = [
 ("Custom software", "Web apps and SaaS products that hold up after launch, not just on demo day.",
  "Admin panels, customer portals, booking and tracking flows, multi-tenant SaaS. We build in the Laravel + React class of stack because it's boring in the good way: easy to hire for, easy to host in Bangladesh or abroad.",
  ["Laravel","React","Node.js","PostgreSQL","Livewire"], "A running staging URL from week two, plus a repo you own."),
 ("Mobile apps", "One codebase for iOS and Android, without the second-class-citizen feel.",
  "Flutter or React Native, chosen per project, wired to the same API as your web product. Store submission and release pipeline included.",
  ["Flutter","React Native","iOS","Android","Firebase"], "TestFlight / internal-track builds your team can tap through."),
 ("AI agents", "Agents that do one job well inside your existing workflow.",
  "Retrieval over your own documents, support triage, internal ops copilots. Scoped narrowly, evaluated against real examples, and given a human hand-off. We won't build a chatbot for its own sake.",
  ["OpenAI","LangChain","Python","RAG","Evals"], "An eval sheet that shows where the agent is right, wrong, and unsure."),
 ("Digital consultancy", "A plan you can actually staff, budget, and ship.",
  "Architecture reviews, build-vs-buy calls, cloud and DevOps setup, rescue plans for stalled projects. Useful before you hire a team, ours or anyone's.",
  ["Architecture","Cloud","DevOps","Roadmaps"], "A written roadmap with sequence, risks, and rough cost bands."),
 ("QA & security", "Fewer surprises in production.",
  "Automated test suites, CI gates, and practical security reviews of web and API surfaces. Can be added to an existing codebase, including one we didn't write.",
  ["Pest","Playwright","CI/CD","OWASP review"], "A findings report ranked by severity, with fixes or PRs attached."),
]

def chips(xs, v=()):
    return '<div class="chips">' + "".join(f'<span class="chip{" v" if x in v else ""}">{x}</span>' for x in xs) + "</div>"

# ---------------- HOME ----------------
cases_html = "".join(f'''
<a class="case-card rv" href="{{r}}work/{s}/">
 <div class="plate">{plate(s)}</div>
 <div class="meta"><span class="label">0{i+1} · {CASES[s]["sector"]}</span><span class="go">Case →</span></div>
 <h3>{CASES[s]["name"]}</h3>
</a>''' for i, s in enumerate(ORDER))

svc_rows = "".join(f'''
<a class="row-i" href="{{r}}services/#p{i+1}"><span class="n">0{i+1}</span><h3>{t}</h3><p>{o}</p><span class="arr">→</span></a>''' for i,(t,o,*_ ) in enumerate(SERVICES))

home = f'''
<section class="hero">
 <div class="wrap">
  <div class="hero-meta label"><span>Software studio · Uttara, Dhaka</span><span>Web · Mobile · AI agents</span></div>
  <h1>We build the software <em>businesses run on.</em></h1>
  <div class="hero-foot">
   <div>
    <p>BindRaft is a product-engineering studio for founders and operators: custom web platforms, mobile apps and practical AI agents, designed and built in-house.</p>
    <p class="proof">Live client sites: <a href="{{r}}work/world-pac/">World Pac</a> · <a href="{{r}}work/silkways-group/">Silkways</a> · <a href="{{r}}work/wellpac-polymers/">Wellpac</a></p>
   </div>
   <div class="hero-ctas">
    <a class="btn" href="{{r}}contact/#book">Start a project <span class="arr">→</span></a>
    <a class="btn ghost" href="{{r}}work/">See work <span class="arr">→</span></a>
   </div>
  </div>
 </div>
</section>

<section class="sec" aria-labelledby="h-work">
 <div class="wrap">
  <div class="sec-head"><div class="num"><b>01</b> / Selected work</div>
   <div><h2 id="h-work">Live sites for companies that ship real things.</h2>
   <p>Logistics, a ten-company group, an export manufacturer. Each one is public and online. Click through to the cases.</p></div></div>
  <div class="cases">{cases_html}</div>
  <p class="note"><a class="link-u" href="{{r}}work/">All work →</a></p>
 </div>
</section>

<section class="sec" aria-labelledby="h-svc">
 <div class="wrap">
  <div class="sec-head"><div class="num"><b>02</b> / Services</div>
   <div><h2 id="h-svc">Five things we do. Nothing padded.</h2></div></div>
  <div class="rows">{svc_rows}</div>
 </div>
</section>

<section class="sec" aria-labelledby="h-proc">
 <div class="wrap">
  <div class="sec-head"><div class="num"><b>03</b> / Process</div>
   <div><h2 id="h-proc">Four steps. Something you can click in every one.</h2></div></div>
  <div class="process">
   <div class="step rv"><span class="n">01</span><h3>Discover</h3><p>We sit with the people who'll use it and agree what "done" means before anyone writes code.</p><div class="out">Out: scope + plan</div></div>
   <div class="step rv"><span class="n">02</span><h3>Design</h3><p>Flows and screens you can click through and test with real users before the build starts.</p><div class="out">Out: clickable designs</div></div>
   <div class="step rv"><span class="n">03</span><h3>Build</h3><p>Short cycles, a staging URL from early on, weekly demos instead of status emails.</p><div class="out">Out: staging + repo</div></div>
   <div class="step rv"><span class="n">04</span><h3>Launch</h3><p>Release, monitoring, hand-over docs. Then we either stay on as support or leave it with your team.</p><div class="out">Out: production + docs</div></div>
  </div>
 </div>
</section>

<section class="sec" aria-labelledby="h-cl" style="padding-bottom:clamp(56px,7vw,96px)">
 <div class="wrap">
  <div class="sec-head"><div class="num"><b>04</b> / Clients</div><div><h2 id="h-cl" style="font-size:clamp(28px,3vw,40px)">Clients online today</h2><p>Open any of them. World Pac and Wellpac carry a “Developed by BindRaft” credit in their footers.</p></div></div>
  <div class="clients">''' + "".join(f'<a href="{{r}}work/{s}/"><strong>{CASES[s]["name"]}</strong><span class="label">{CASES[s]["urltext"]}</span></a>' for s in ORDER) + '''</div>
 </div>
</section>

<section class="closing">
 <div class="wrap">
  <span class="label">05 / Next step</span>
  <h2>Got a build in mind? <span>Book 30 minutes.</span></h2>
  <div class="row">
   <a class="btn" href="{r}contact/#book">Pick a time <span class="arr">→</span></a>
   <a class="btn ghost" href="mailto:contact@bindraft.com">contact@bindraft.com</a>
  </div>
 </div>
</section>
'''
page("index.html", "BindRaft · Software studio in Dhaka. Web, mobile, AI agents", "BindRaft is a product-engineering studio in Uttara, Dhaka building custom web platforms, mobile apps and practical AI agents for founders and operators.", home)

# ---------------- WORK INDEX ----------------
rows = "".join(f'''
<a href="{{r}}work/{s}/" data-bg="{CASES[s]["bg"]}" data-fg="{CASES[s]["fg"]}" data-name="{CASES[s]["short"]}" data-sector="{CASES[s]["urltext"]}">
 <strong>{CASES[s]["name"]}</strong><span>{CASES[s]["sector"]}</span><span>{CASES[s]["platform"]}</span><span class="yr"><i class="live-dot" aria-hidden="true"></i>Live</span><span class="arr">→</span>
</a>''' for s in ORDER)
work = f'''
<section class="phero"><div class="wrap">
 <nav class="crumb label" aria-label="Breadcrumb"><a href="{{r}}">Home</a> / Work</nav>
 <h1>Work</h1>
 <p class="lede">Public sites we've delivered. Each case sticks to what you can check online: no made-up metrics, no ghost-written quotes.</p>
</div></section>
<section style="padding-bottom:clamp(72px,10vw,140px)"><div class="wrap">
 <div class="wlist" role="list">
  <div class="head label" aria-hidden="true"><span>Client</span><span>Sector</span><span>Platform</span><span>Status</span><span></span></div>
  {rows}
 </div>
 <p class="note">Every site listed is public and online. More cases are added as clients approve them.</p>
</div></section>
<div class="hover-preview" aria-hidden="true"><span class="t"></span><span class="b"></span></div>
<section class="closing"><div class="wrap"><span class="label">Next step</span>
 <h2>Want yours on this list? <span>Talk to us.</span></h2>
 <div class="row"><a class="btn" href="{{r}}contact/#book">Book a call <span class="arr">→</span></a></div></div></section>
'''
page("work/index.html", "Work · Client websites built by BindRaft", "Live client sites built by BindRaft in Dhaka: World Pac International (courier and logistics), Silkways Group (10 concerns) and Wellpac Polymers (export packaging).", work, "work",
     schema=[{"@type": "CollectionPage", "@id": SITE + "/work/#page", "url": SITE + "/work/", "name": "Work",
              "hasPart": [{"@id": SITE + f"/work/{s}/#case"} for s in ORDER]}], crumb=[("Work", "/work/")])


# ---------------- CASES ----------------
CASE_BODY = {
 "world-pac": dict(
  intro="Corporate website and shipment-tracking front door for World Pac International Ltd., a Dhaka-based international air express courier and logistics company.",
  hq="Landmark Building, Gulshan-2, Dhaka", est="Est. 2004 · rebranded 2024",
  credit="“Developed by BindRaft” in the site footer",
  problem=("A logistics brand is judged on its website before anyone ships a parcel.",
   "World Pac sells international express courier, warehousing and fulfilment, customs clearance and corporate B2B2C logistics out of Dhaka. After its 2024 rebrand, the website had two jobs: present the new brand credibly to corporate shippers, and get existing customers to tracking with as few clicks as possible."),
  constraints=["Four service lines (express courier, warehousing & fulfilment, customs, corporate B2B2C) without burying any of them","Tracking has to be the first thing a returning customer finds","Shipments handled by associate partners need their own route to the partner tracking portal","Has to load quickly on Bangladeshi mobile networks"],
  built=("Marketing site with tracking as the main entry point.",
   "A corporate site organised around the four service lines, with shipment tracking in the main path rather than tucked away in the footer, a separate partner-tracking hand-off for associate-network shipments, and “Get a quote” and contact routes for new business. The public stack fingerprint is Laravel."),
  stack=["Laravel","PHP","Responsive web","Shipment tracking","Partner portal hand-off"], verified=["Laravel"],
  result="Live as World Pac's public corporate site and tracking front door, credited “Developed by BindRaft” in its footer.",
  note="Operational figures shown on worldpacintl.com (daily shipments, destinations, delivery accuracy) are World Pac's own business stats, not BindRaft results, so they aren't repeated here."),
 "silkways-group": dict(
  intro="One group website for Silkways Group, a diversified Bangladeshi business group established in 1995, and its ten sister concerns.",
  hq="Gulshan Avenue, Dhaka", est="Group established 1995",
  credit=None,
  problem=("Ten businesses under one name, with very little in common.",
   "Silkways spans airline GSA and operational support, air cargo, IATA-accredited travel, international trade, smart-card manufacturing, IT services, Wellpac Polymers, overseas recruitment (Alamsons), Farisha Hotel & Resort and Silk Spoon. The group site has to explain how the companies relate and then send each visitor to the right one quickly."),
  constraints=["Ten sister concerns that each need a fair entry, with none dominating","Audiences ranging from airline partners and exporters to hotel and restaurant guests","A group identity that sits above the concerns without flattening them","Room to add or remove concerns later without a redesign"],
  built=("A group website with a directory of the sister concerns.",
   "A multi-entity site: a featured-concern carousel and the group story at the top, then a structured directory where each concern gets its core expertise, its founding year where known (Cargo 1995, Card & Printing 2005, Tours & Travels 2008, Solutions 2013) and a link out to its own site. Board of directors, vision and mission, news, gallery and contact sit alongside. The public stack fingerprint is Laravel."),
  stack=["Laravel","PHP","Multi-entity IA","Concern directory","News & gallery"], verified=["Laravel"],
  result="Live as the Silkways Group corporate site and directory of its ten sister concerns.",
  note="Group facts (founded 1995, the concern list and founding years) come from Silkways' own public site."),
 "wellpac-polymers": dict(
  intro="Website for Wellpac Polymers Limited, a 100% export-oriented flexible-packaging manufacturer in Bangladesh and a sister concern of Silkways Group.",
  hq="Office: Gulshan Avenue-1, Dhaka<br>Factory: Gojaria, Munshiganj", est="Silkways Group concern",
  credit="“Developed by BindRaft” in the site footer",
  problem=("Overseas buyers check a supplier's website before they ask for a quote.",
   "Wellpac makes HDPE, LDPE and LLDPE bags (T-shirt bags on roll, carrier bags, draw-tape garbage and draw-tape bags) for export to the United Kingdom, the United States, Japan and Europe. Its site needs to show a procurement manager what the plant can make and how to ask for a quotation."),
  constraints=["The audience is international B2B buyers, not local consumers","The product range has to be easy to scan, so it's built around products and a gallery","Plant capability (their stated 60,000 sq ft floor, 8-colour printing, 1.064 MW gas generator) shown without overselling","Needs to sit inside the wider Silkways group presence"],
  built=("An export-manufacturer site built around products and enquiries.",
   "A focused manufacturer site with product pages for each bag type, manufacturing, export markets, gallery and certifications sections, a downloadable company profile, and a quotation request that asks buyers for product, dimensions, printing needs and quantity. The public stack fingerprint is Laravel."),
  stack=["Laravel","PHP","Product catalogue","Quotation request","Company profile"], verified=["Laravel"],
  result="Live as Wellpac's public site for overseas buyers, credited “Developed by BindRaft” in its footer.",
  note="Plant and market figures are Wellpac's own published claims, not BindRaft results."),
}
for i, s in enumerate(ORDER):
    c, b = CASES[s], CASE_BODY[s]
    nxt = ORDER[(i+1) % 3]
    cons = "".join(f"<li><span>{j+1:02d}</span>{x}</li>" for j, x in enumerate(b["constraints"]))
    legend = '<p class="chip-legend">Copper chip = confirmed from the live site’s public fingerprint. Others = what was delivered.</p>'
    credit = f'<div><dt>Credit</dt><dd>{b["credit"]}</dd></div>' if b["credit"] else '<div><dt>Status</dt><dd><i class="live-dot" aria-hidden="true"></i>Live, public</dd></div>'
    body = f'''
<section class="case-hero"><div class="wrap">
 <nav class="crumb label muted" aria-label="Breadcrumb" style="margin-bottom:20px"><a href="{{r}}work/">Work</a> / 0{i+1}</nav>
 <h1>{c["name"]}</h1>
 <p class="lede" style="font-size:clamp(18px,1.6vw,22px);max-width:52ch;color:var(--ink-2);margin-top:28px">{b["intro"]}</p>
 <dl class="case-facts">
  <div><dt>Sector</dt><dd>{c["sector"]}</dd></div>
  <div><dt>Client</dt><dd>{b["hq"]}<br><span class="muted">{b["est"]}</span></dd></div>
  <div><dt>Deliverable</dt><dd>{c["platform"]}</dd></div>
  {credit}
  <div><dt>Live</dt><dd><a href="{c["url"]}" target="_blank" rel="noopener">{c["urltext"]} ↗</a></dd></div>
 </dl>
 <div class="case-plate plate">{plate(s, True)}</div>
</div></section>
<section><div class="wrap">
 <div class="cs-block"><div class="num"><b>01</b> / Problem</div><div><h2>{b["problem"][0]}</h2><p>{b["problem"][1]}</p></div></div>
 <div class="cs-block"><div class="num"><b>02</b> / Constraints</div><div><ul class="list">{cons}</ul></div></div>
 <div class="cs-block"><div class="num"><b>03</b> / What we built</div><div><h2>{b["built"][0]}</h2><p>{b["built"][1]}</p>{chips(b["stack"], b["verified"])}{legend}</div></div>
 <div class="cs-block"><div class="num"><b>04</b> / Result</div><div>
  <div class="result"><div><a class="url" href="{c["url"]}" target="_blank" rel="noopener">{c["urltext"]} ↗</a><p>{b["result"]}</p></div>
  <a class="btn ghost sm" href="{c["url"]}" target="_blank" rel="noopener">Visit live site <span class="arr">↗</span></a></div>
  <p class="note">{b["note"]}</p>
 </div></div>
</div></section>
<a class="next" href="{{r}}work/{nxt}/"><div class="wrap"><span class="label">Next project →</span><strong>{CASES[nxt]["name"]}</strong></div></a>
<section class="closing"><div class="wrap"><span class="label">Next step</span>
 <h2>Have a similar brief? <span>Book a call.</span></h2>
 <div class="row"><a class="btn" href="{{r}}contact/#book">Pick a time <span class="arr">→</span></a><a class="btn ghost" href="{{r}}work/">All work</a></div></div></section>
'''
    cw = {"@type": "CreativeWork", "@id": SITE + f"/work/{s}/#case", "name": f"{c['name']} website",
          "description": b["intro"], "url": c["url"], "mainEntityOfPage": SITE + f"/work/{s}/",
          "creator": {"@id": SITE + "/#org"}, "genre": "Website", "inLanguage": "en",
          "about": {"@type": "Organization", "name": c["name"], "url": c["url"]},
          "keywords": ", ".join(b["stack"])}
    page(f"work/{s}/index.html", f"{c['name']} · Case study · BindRaft", b["intro"], body, "work",
         schema=[cw], crumb=[("Work", "/work/"), (c["name"], f"/work/{s}/")], og_type="article")

# ---------------- SERVICES (manifesto + sticky-split panels) ----------------
ON = ' class="on"'
N = len(SERVICES)
VERBS = ["Build", "Ship", "Automate", "Plan", "Harden"]

S3 = [
 dict(when="You have a workflow that lives in spreadsheets, email and phone calls, and it's starting to break.",
      do=["Map the flow with the people who run it","Ship a staging URL early, then demo weekly","Hand over a repo, docs and hosting in your name"],
      mock=f'''<div class="m-bar"><i></i><i></i><i></i><span>staging.your-product.app</span></div>
<div class="m-tree"><span>repo/</span><span>├ app/</span><span>├ resources/</span><span>├ tests/</span><span>└ README.md</span></div>
<div class="m-tags"><span>Week 02 · staging live</span><span>Repo owner · you</span></div>'''),
 dict(when="Your customers or field team need it in their pocket, not on a laptop.",
      do=["Choose Flutter or React Native per project","Wire it to the same API as your web product","Run store submission and the release pipeline"],
      mock='''<div class="m-phones"><div class="m-ph"><span>iOS</span><i></i><i></i><i class="c"></i><b>TestFlight build</b></div><div class="m-ph"><span>Android</span><i></i><i class="c"></i><i></i><b>Internal track</b></div></div>'''),
 dict(when="A team spends hours a day answering the same questions from the same documents.",
      do=["Scope one job the agent owns, and what it never touches","Collect real examples and score the agent against them","Route anything unsure to a person"],
      mock='''<div class="m-tbl"><div class="h"><span>Example</span><span>Expected</span><span>Agent</span><span>Verdict</span></div>
<div><span>#001</span><i></i><i></i><b class="ok">Right</b></div><div><span>#002</span><i></i><i></i><b class="no">Wrong</b></div><div><span>#003</span><i></i><i></i><b class="mb">Unsure → human</b></div><div><span>#004</span><i></i><i></i><b class="ok">Right</b></div></div>'''),
 dict(when="You're about to hire, buy, or rebuild, and want a second opinion before the money moves.",
      do=["Review architecture, cloud and DevOps as they are","Make the build-vs-buy call in writing","Sequence the work with risks and rough cost bands"],
      mock='''<div class="m-road"><div><span>Phase 1</span><i style="width:34%"></i><em>Risk · low</em></div><div><span>Phase 2</span><i style="width:58%;margin-left:22%"></i><em>Risk · med</em></div><div><span>Phase 3</span><i class="c" style="width:40%;margin-left:56%"></i><em>Risk · high</em></div><div class="bands"><span>Cost band A</span><span>Cost band B</span><span>Cost band C</span></div></div>'''),
 dict(when="Releases feel risky, or nobody can say how exposed the API really is.",
      do=["Add automated tests and CI gates to the codebase you have","Review web and API surfaces against OWASP-class issues","Rank findings by severity, then fix or open PRs"],
      mock='''<div class="m-find"><div><b class="s1">Critical</b><i></i><span>PR attached</span></div><div><b class="s2">High</b><i></i><span>PR attached</span></div><div><b class="s3">Medium</b><i></i><span>Fix noted</span></div><div><b class="s4">Low</b><i></i><span>Backlog</span></div></div>'''),
]
panels = "".join(f'''
<section class="p3{" dark" if i%2 else ""}" id="p{i+1}" aria-labelledby="p{i+1}-h"><div class="wrap p3-split">
 <div class="p3-stick">
  <div class="label p3-k"><b>0{i+1}</b> / 0{N} · {VERBS[i]}</div>
  <h2 id="p{i+1}-h">{t}</h2>
  <p class="p3-o">{o}</p>
  <a class="btn sm" href="{{r}}contact/#book">Talk about {t.lower()} <span class="arr">→</span></a>
 </div>
 <div class="p3-flow">
  <div class="p3-card"><span class="label">When you need it</span><p class="p3-big">{x["when"]}</p></div>
  <div class="p3-card"><span class="label">What we do</span><ol class="p3-do">{"".join(f"<li><span>{j+1:02d}</span>{y}</li>" for j,y in enumerate(x["do"]))}</ol>{chips(st)}</div>
  <figure class="p3-card p3-art"><figcaption class="label"><span>You get</span><span>Illustrative layout · not client data</span></figcaption>
   <div class="mock m{i+1}" aria-hidden="true">{x["mock"]}</div>
   <p>{a}</p></figure>
 </div>
</div></section>''' for i,((t,o,d,st,a),x) in enumerate(zip(SERVICES,S3)))
toc3 = "".join(f'<a href="#p{i+1}"><span>0{i+1}</span>{t}</a>' for i,(t,*_) in enumerate(SERVICES))
services = f'''
<section class="m3-hero"><div class="wrap">
 <nav class="crumb label" aria-label="Breadcrumb"><a href="{{r}}">Home</a> / Services</nav>
 <p class="label muted m3-k">A short manifesto</p>
 <h1 class="m3-h1">We'd rather ship <span>one thing that works</span> than five that demo well.</h1>
 <ol class="m3-tenets">
  <li><span>i.</span>Every engagement ends in something you can open, run, or forward. Not a slide deck.</li>
  <li><span>ii.</span>We scope narrow on purpose, and say out loud what we won't build.</li>
  <li><span>iii.</span>The code, accounts and credentials are yours from day one.</li>
 </ol>
 <nav class="m3-toc label" aria-label="Offers">{toc3}</nav>
</div></section>
{panels}
<section class="closing"><div class="wrap"><span class="label">Next step</span>
 <h2>One offer, one call. <span>Start there.</span></h2>
 <div class="row"><a class="btn" href="{{r}}contact/#book">Book 30 minutes <span class="arr">→</span></a><a class="btn ghost" href="{{r}}contact/#write">Write instead</a></div></div></section>
'''
svc_ld = [{"@type": "Service", "@id": SITE + f"/services/#p{i+1}", "name": t, "description": o + " " + d,
           "serviceType": t, "provider": {"@id": SITE + "/#org"}, "areaServed": "Worldwide",
           "url": SITE + f"/services/#p{i+1}"} for i, (t, o, d, *_ ) in enumerate(SERVICES)]
page("services/index.html", "Services · Custom software, mobile apps, AI agents · BindRaft",
     "Five services from BindRaft in Dhaka: custom software, mobile apps, AI agents, digital consultancy, and QA & security. What each one is for, what we do, and what you get.",
     services, "services", schema=svc_ld, crumb=[("Services", "/services/")])

# ---------------- ABOUT ----------------
values = [("Show, don't tell","Clickable designs and staging links over slide decks and status reports."),
 ("Boring where it counts","Proven stacks, readable code, docs you can hand to the next developer."),
 ("Honest scope","We say what we won't build, and why, before we quote."),
 ("You own it","Repos, accounts and credentials are in your name from day one."),
 ("Close to the work","Direct contact with the people building it, not a chain of account managers.")]
vals = "".join(f"<li><span>{i+1:02d}</span><strong>{a}</strong><p>{b}</p></li>" for i,(a,b) in enumerate(values))
about = f'''
<section class="phero"><div class="wrap">
 <nav class="crumb label" aria-label="Breadcrumb"><a href="{{r}}">Home</a> / About</nav>
 <h1>Bind together to stay afloat.</h1>
 <p class="lede">It's an old line of ours and still how we work: small team, close to the client, hands on the code.</p>
</div></section>
<section class="sec"><div class="wrap about-grid">
 <div class="label muted"><b class="copper" style="font-weight:400">01</b> / Origin</div>
 <div class="prose">
  <p>BindRaft is a software studio in Uttara, Dhaka, working since 2023. We work as a product-engineering partner: we design and build the software, then stay on to run it with you if you want that.</p>
  <p>Our clients range from courier brands to multi-company groups to export manufacturers. They hire us when the website or the tool has to work in daily use, not just look good in a pitch.</p>
 </div>
</div></section>
<section class="sec"><div class="wrap">
 <div class="sec-head"><div class="num"><b>02</b> / How we work</div><div><h2>Five working rules</h2></div></div>
 <ul class="values">{vals}</ul>
</div></section>
<section class="sec"><div class="wrap">
 <div class="sec-head"><div class="num"><b>03</b> / Studio</div><div><h2>Where to find us</h2></div></div>
 <div class="facts-strip">
  <div><span class="label">Address</span>{ADDR}</div>
  <div><span class="label">Hours</span>Sat–Thu · 9:00–18:00 (Dhaka, UTC+6)</div>
  <div><span class="label">Reach</span><a class="link-u" href="mailto:{EMAIL}">{EMAIL}</a><br><a href="tel:{TEL}">{PHONE}</a></div>
 </div>
 <div class="callout" style="margin-top:40px"><span>Want to meet the people who'd build it? We'll set up a call with the team that would work on your project.</span><a class="btn ghost sm" href="{{r}}contact/#write">Ask about the team <span class="arr">→</span></a></div>
</div></section>
<section class="closing"><div class="wrap"><span class="label">Next step</span>
 <h2>Come say hello. <span>Uttara or online.</span></h2>
 <div class="row"><a class="btn" href="{{r}}contact/#book">Book a call <span class="arr">→</span></a><a class="btn ghost" href="{{r}}work/">See work</a></div></div></section>
'''
page("about/index.html", "About BindRaft · Product-engineering studio in Uttara, Dhaka",
     "BindRaft is a product-engineering studio in Uttara, Dhaka, working since 2023. Small team, close to the client, hands on the code. How we work and where to find us.",
     about, "about", schema=[{"@type": "AboutPage", "@id": SITE + "/about/#page", "url": SITE + "/about/", "name": "About BindRaft", "about": {"@id": SITE + "/#org"}}],
     crumb=[("About", "/about/")])

# ---------------- CONTACT ----------------
contact = f'''
<section class="phero"><div class="wrap">
 <nav class="crumb label" aria-label="Breadcrumb"><a href="{{r}}">Home</a> / Contact</nav>
 <h1>Start a project.</h1>
 <p class="lede">Book a 30-minute intro call. Tell us what you're building, we'll tell you honestly whether we're the right team.</p>
 <ul class="assure label" aria-label="What to expect">
  <li>NDA on request</li><li>Reply in 1–2 business days</li><li>Proposal with estimate after the call</li>
 </ul>
</div></section>
<section class="sec" id="book" aria-labelledby="h-book" style="padding-top:clamp(48px,6vw,80px)"><div class="wrap contact-grid">
 <div>
  <div class="cal" id="cal">
   <div class="cal-top"><div><h2 id="h-book" class="cal-h">Intro call · 30 min</h2><div class="tz">Pick a preferred time · Dhaka (UTC+6) · <span data-week></span></div></div>
    <div class="cal-nav"><button type="button" data-prev>← Prev week</button><button type="button" data-next>Next week →</button></div></div>
   <div class="cal-grid" aria-live="polite"><noscript><p class="cal-nojs">Email <a class="link-u" href="mailto:{EMAIL}?subject=Intro%20call%20request">{EMAIL}</a> with two or three times that suit you (Sat–Thu, 9:00–18:00 Dhaka).</p></noscript></div>
   <div class="cal-foot"><span>Sat–Thu · 9:00–18:00 · Google Meet or at the studio in Uttara</span><span>We confirm by email with a calendar invite</span></div>
  </div>
 </div>
 <aside class="side" aria-label="Contact details">
  <h2 class="side-h">Or reach us directly</h2>
  <p class="fine">We usually reply within 1–2 business days. Happy to sign an NDA before you share details.</p>
  <dl>
   <div><dt>Email</dt><dd><a class="link-u" href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
   <div><dt>Phone</dt><dd><a href="tel:{TEL}">{PHONE}</a></dd></div>
   <div><dt>Studio</dt><dd>{ADDR}</dd></div>
   <div><dt>Hours</dt><dd>Sat–Thu · 9:00–18:00 (Dhaka)</dd></div>
  </dl>
 </aside>
</div></section>
<section class="sec" id="write" aria-labelledby="h-write"><div class="wrap">
 <div class="sec-head"><div class="num"><b>02</b> / Write instead</div><div><h2 id="h-write">Short message</h2><p>A sentence or two about the project is plenty. Sending opens your email app with the message ready to go to {EMAIL}.</p></div></div>
 <div class="about-grid"><div></div><div>
  <form class="short" id="short-form" action="mailto:{EMAIL}" method="post" enctype="text/plain">
   <div class="two">
    <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
   </div>
   <div class="field"><label for="f-co">Company <span class="opt">(optional)</span></label><input id="f-co" name="company" autocomplete="organization"></div>
   <div class="field"><label for="f-msg">What are you building?</label><textarea id="f-msg" name="message" required></textarea></div>
   <div class="form-row"><button class="btn" type="submit">Send message <span class="arr">→</span></button><span class="fine">Or email <a class="link-u" href="mailto:{EMAIL}">{EMAIL}</a></span></div>
   <div class="form-msg" id="form-msg" role="status" tabindex="-1"></div>
   <p class="fine">NDA available on request. We'll only use your details to reply. See the <a class="link-u" href="{{r}}privacy-policy/">Privacy Policy</a>.</p>
  </form>
 </div></div>
</div></section>
<div class="modal" id="modal" role="dialog" aria-modal="true" aria-labelledby="m-title">
 <div class="box">
  <button class="x" type="button" data-close>Close ✕</button>
  <span class="label muted">Intro call request</span>
  <h3 id="m-title">Request this time</h3>
  <div class="when"></div>
  <p>We'll check the slot and reply with a calendar invite. Sending opens your email app with the request filled in.</p>
  <div class="field" style="margin-top:8px"><label for="m-note">Anything we should know? <span class="opt">(optional)</span></label><input id="m-note" autocomplete="off"></div>
  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:24px"><a class="btn" id="m-send" href="mailto:{EMAIL}">Send request <span class="arr">→</span></a><button class="btn ghost" type="button" data-close>Pick another time</button></div>
 </div>
</div>
'''
page("contact/index.html", "Contact · Book an intro call · BindRaft",
     "Book a 30-minute intro call with BindRaft or send a short message. Sat–Thu, 9:00–18:00 Dhaka. contact@bindraft.com · +880 1558 934599 · Uttara, Dhaka.",
     contact, "contact", schema=[{"@type": "ContactPage", "@id": SITE + "/contact/#page", "url": SITE + "/contact/", "name": "Contact BindRaft",
        "about": {"@id": SITE + "/#org"}, "mainEntity": {"@id": SITE + "/#org"}}], crumb=[("Contact", "/contact/")])

# ---------------- 404 ----------------
nf = '''
<section class="nf"><div class="wrap">
 <span class="label muted">Error / Page not found</span>
 <div class="code" aria-hidden="true">4<span>0</span>4</div>
 <h1>This page isn't here.</h1>
 <p class="muted" style="max-width:48ch">It may have moved, or the link was mistyped. These pages do exist:</p>
 <div class="links"><a class="btn" href="{r}work/">See work <span class="arr">→</span></a><a class="btn ghost" href="{r}contact/#book">Contact</a><a class="btn ghost" href="{r}">Home</a></div>
</div></section>
'''
page("404.html", "Not found · BindRaft", "Page not found.", nf)

# ---------------- LEGAL (written for this site, see _src/legal/site_legal.py) ----------------
from site_legal import ALL as LEGAL_ALL, UPDATED
LEGAL = ["privacy-policy", "terms-of-use", "cookie-policy"]
for slug in LEGAL:
    d = LEGAL_ALL[slug]
    secs_d = [dict(x, num=k + 1) for k, x in enumerate(d["sections"])]
    toc = "".join(f'<li><a href="#{x["id"]}"{ON if k==0 else ""}><span class="n">{x["num"]:02d}</span><span class="t">{x["title"]}</span><i aria-hidden="true"></i></a></li>' for k,x in enumerate(secs_d))
    secs = "".join(f'<section class="lsec" id="{x["id"]}" aria-labelledby="{x["id"]}-h"><div class="lnum label"><b>{x["num"]:02d}</b></div><div class="lbody"><h2 id="{x["id"]}-h">{x["title"]}</h2><div class="lprose">{x["html"]}</div></div></section>' for x in secs_d)
    summ = f'<div class="lsum"><span class="label">Quick summary</span><p>{d["summary"]}</p></div>' if d["summary"] else ""
    others = " · ".join(f'<a class="link-u" href="{{r}}{o}/">{LEGAL_ALL[o]["title"]}</a>' for o in LEGAL if o != slug)
    body = f'''
<section class="phero legal-hero"><div class="wrap">
 <nav class="crumb label" aria-label="Breadcrumb"><a href="{{r}}">Home</a> / Legal / {d["title"]}</nav>
 <h1>{d["title"]}</h1>
 <p class="lede">{d["intro"]}</p>
 <dl class="legal-meta label">
  <div><dt>Last updated</dt><dd>{UPDATED}</dd></div>
  <div><dt>Sections</dt><dd>{len(secs_d):02d}</dd></div>
  <div><dt>Applies to</dt><dd>This website</dd></div>
 </dl>
</div></section>
<section class="legal-wrap"><div class="wrap legal">
 <aside class="legal-toc" aria-label="Contents">
  <span class="label muted">Contents</span>
  <ol data-spy>{toc}</ol>
 </aside>
 <div class="legal-body">{summ}{secs}
  <p class="note">Questions about this policy: <a class="link-u" href="mailto:{EMAIL}">{EMAIL}</a>. Also see: {others}.</p>
 </div>
</div></section>
'''
    page(f"{slug}/index.html", f"{d['title']} · BindRaft", d["intro"], body,
         schema=[{"@type": "WebPage", "@id": SITE + f"/{slug}/#page", "url": SITE + f"/{slug}/", "name": d["title"], "dateModified": "2026-10-28"}],
         crumb=[(d["title"], f"/{slug}/")])

# ---------------- robots.txt + sitemap.xml ----------------
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
pri = {"/": "1.0", "/work/": "0.8", "/services/": "0.8", "/contact/": "0.8", "/about/": "0.6"}
sm = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>2026-10-28</lastmod><priority>{pri.get(u, '0.7' if u.startswith('/work/') else '0.3')}</priority></url>\n" for u in SITEMAP)
open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + sm + "</urlset>\n")
print("wrote robots.txt, sitemap.xml (%d urls)" % len(SITEMAP))
