"""Legal copy written for this marketing website (not the client-project contracts).
Reviewed against what the site actually does: static pages, no accounts, no analytics,
no cookies, self-hosted fonts, contact via the visitor's own email app."""
UPDATED = "October 29, 2026"
E_ = "contact@bindraft.com"
M = f'<a href="mailto:{E_}">{E_}</a>'
ADDR = "Road-10, House-31, Sector-9, Uttara, Dhaka 1230, Bangladesh"

def S(id, title, html): return dict(id=id, title=title, html=html)

PRIVACY = dict(
 title="Privacy Policy",
 intro="What this website collects, why, and what you can ask us to do with it.",
 summary="This site has no accounts, no analytics and no tracking. If you email us or send a request through the contact page, we get what you write and use it to reply. Our hosting provider keeps standard server logs. That's it.",
 sections=[
  S("who-we-are","Who we are",f"<p>BindRaft (\"we\", \"us\") is a software studio at {ADDR}. This policy covers this website only. Work we do for clients is covered by the agreement we sign with each client.</p>"),
  S("what-we-collect","What we collect",
    "<h3>When you contact us</h3><p>The contact form and the intro-call picker don't submit anything to our servers. They open your own email app with a message addressed to us. When you send it, we receive:</p>"
    "<ul><li>Your name and email address</li><li>Anything you choose to write, such as your company, project details or a preferred call time</li></ul>"
    "<p>The same applies if you email or call us directly.</p>"
    "<h3>When you browse</h3><p>Like any website host, our hosting provider records basic request data (IP address, browser type, the page requested and the time) to run and secure the service.</p>"
    "<h3>What we don't collect</h3><ul><li>No user accounts or passwords</li><li>No analytics, advertising or tracking pixels</li><li>No payment details</li></ul>"),
  S("how-we-use-it","How we use it","<ul><li>To reply to you and talk about your project</li><li>To prepare a proposal or estimate if you ask for one</li><li>To keep the site secure and working</li></ul><p>We don't sell your data and we don't add you to a mailing list.</p>"),
  S("who-we-share-with","Who we share it with","<p>Only the services we need to run the site and answer you: our email provider and our website hosting provider. We may also disclose information if the law requires it.</p>"),
  S("transfers","Where it's processed","<p>Our email and hosting providers may store or process data outside Bangladesh. We pick established providers that protect data in transit and at rest.</p>"),
  S("retention","How long we keep it","<p>We keep enquiry emails for as long as the conversation, and any project that follows from it, needs them, plus any period the law requires for business records. Server logs are kept by the hosting provider for a limited period under its own retention settings.</p>"),
  S("your-rights","Your choices",f"<p>You can ask us to show you, correct or delete the messages and contact details we hold about you. Email {M} and we'll respond within 30 days.</p>"),
  S("security","Security","<p>The site is served over HTTPS. Access to our inbox is limited to the people who handle enquiries.</p>"),
  S("children","Children","<p>This site is meant for businesses and isn't directed at children.</p>"),
  S("changes","Changes to this policy","<p>If what the site collects changes, for example if we add analytics or an online booking tool, we'll update this page and the date at the top before the change goes live.</p>"),
  S("contact","Contact",f"<p>{M}<br>{ADDR}</p>"),
 ])

TERMS = dict(
 title="Terms of Use",
 intro="The rules for using this website. Project work is covered separately by a written agreement.",
 summary="Use the site lawfully, don't try to break it, and don't reuse our content as your own. The site is information about our studio, not an offer or a contract.",
 sections=[
  S("scope","What these terms cover","<p>These terms apply to your use of this website. Any software, design or consulting work BindRaft does for you is governed by the separate agreement we sign for that project, not by these terms.</p>"),
  S("using-the-site","Using the site","<ul><li>Use it only for lawful purposes</li><li>Don't try to disrupt, overload or gain unauthorised access to the site or its hosting</li><li>Don't use automated tools to copy the site in bulk</li></ul>"),
  S("content","Our content and names","<p>The text, design and code of this site and the BindRaft name belong to BindRaft. You may share links and short quotes with attribution.</p><p>Client names and websites shown in our work belong to those clients. We show them to describe work we delivered.</p>"),
  S("information","Information on the site","<p>Service descriptions and examples are general information. They aren't a quote or an offer. Scope, price and timelines are only binding once agreed in writing.</p>"),
  S("enquiries","Sending us an enquiry","<p>Contacting us doesn't create a client relationship or an obligation on either side. If you need confidentiality before sharing details, ask for an NDA and we'll sign one first.</p>"),
  S("links","Links to other sites","<p>Our case studies link to client websites. We don't control those sites and aren't responsible for their content, availability or privacy practices.</p>"),
  S("disclaimer","No warranty","<p>We try to keep the site accurate and available, but it is provided \"as is\" without warranties of any kind.</p>"),
  S("liability","Limitation of liability","<p>To the extent the law allows, BindRaft isn't liable for any loss arising from your use of this website or from relying on its content.</p>"),
  S("changes","Changes to these terms","<p>We may update these terms. The date at the top shows when they last changed.</p>"),
  S("law","Governing law","<p>These terms are governed by the laws of the People's Republic of Bangladesh.</p>"),
  S("contact","Contact",f"<p>{M}<br>{ADDR}</p>"),
 ])

COOKIES = dict(
 title="Cookie Policy",
 intro="This website doesn't set cookies. Here's what that means and what would change it.",
 summary="No cookies, no analytics, no advertising tags. Fonts are served from our own domain, so loading a page doesn't contact third-party font or tracking services.",
 sections=[
  S("what-are-cookies","What cookies are","<p>Cookies are small files a website can store in your browser, for example to keep you signed in or to measure visits.</p>"),
  S("what-we-use","What this site uses","<ul><li>No cookies of any kind, essential or otherwise</li><li>No analytics or advertising tools</li><li>No local storage used to track you</li></ul><p>Because nothing is set, there's no cookie banner to accept.</p>"),
  S("other-sites","Other websites","<p>When you follow a link to a client's site, an email provider or a map, that site may set its own cookies under its own policy.</p>"),
  S("controls","Your browser controls","<p>You can block or delete cookies in your browser settings at any time. It won't affect how this site works.</p>"),
  S("changes","If this changes","<p>If we add analytics or a booking tool that uses cookies, we'll update this page first and ask for your consent where required before any non-essential cookie is set.</p>"),
  S("contact","Contact",f"<p>{M}</p>"),
 ])

ALL = {"privacy-policy": PRIVACY, "terms-of-use": TERMS, "cookie-policy": COOKIES}
