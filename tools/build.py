"""Static page generator for the R.B.N. Construction website.
Shared header/footer/head live here once; output is plain HTML."""
import json, os, html

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

SITE = {
    'name': 'R.B.N. Construction',
    'url': 'https://www.yourdomain.lk',          # REPLACE with the live domain
    'phone': '+94 78 150 9110',
    'tel': '+94781509110',
    'wa': '94781509110',                          # CONFIRM WhatsApp number
    'email': '[EMAIL]',
    'street': 'No 46, Sudunellumgama',
    'locality': 'Gallalla',
    'region': 'Polonnaruwa',
    'hours': '[Business hours]',
    'cida': '[CIDA grade]',
    'cida_no': '[CIDA reg. no.]',
    'br_no': '[BR no.]',
    'founded': '[Year]',
}
ADDRESS = f"{SITE['street']}, {SITE['locality']}, {SITE['region']}"
MAP_Q = 'Gallalla,+Polonnaruwa,+Sri+Lanka'

def ph(text):
    """Visible placeholder for client-supplied facts (never invent)."""
    return f'<span class="placeholder">{text}</span>'

def esc(s): return html.escape(s, quote=True)

# ------------------------------------------------------------------ icons
ICONS = {
    'phone': '<path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/>',
    'wa': '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.25-.12-1.47-.72-1.7-.8s-.39-.12-.56.12-.64.8-.78.97-.29.18-.54.06a6.7 6.7 0 0 1-3.3-2.9c-.25-.43.25-.4.71-1.33a.45.45 0 0 0 0-.42c-.06-.12-.56-1.34-.76-1.84s-.4-.42-.56-.42h-.48a.92.92 0 0 0-.67.31 2.8 2.8 0 0 0-.87 2.08 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.69 2.23.75 3.03.63a2.6 2.6 0 0 0 1.7-1.2 2.1 2.1 0 0 0 .15-1.2c-.06-.1-.23-.17-.48-.29Z"/>',
    'mail': '<path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 4-8 5-8-5V6l8 5 8-5Z"/>',
    'pin': '<path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/>',
    'clock': '<path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm1 10.4 3.3 2-.8 1.3L11 13V7h2Z"/>',
    'arrow': '<path d="M5 12h12.2l-4.6-4.6L14 6l7 7-7 7-1.4-1.4 4.6-4.6H5z" transform="translate(0 -1)"/>',
    'menu': '<path d="M3 6h18v2H3zm0 5h18v2H3zm0 5h18v2H3z"/>',
    'close': '<path d="m6.4 5 5.6 5.6L17.6 5 19 6.4 13.4 12l5.6 5.6-1.4 1.4-5.6-5.6L6.4 19 5 17.6l5.6-5.6L5 6.4z"/>',
    'helmet': '<path d="M12 4a8 8 0 0 0-8 8v2H2v3h20v-3h-2v-2a8 8 0 0 0-8-8Zm-1 2.1V11h2V6.1a6 6 0 0 1 5 5.9v2H6v-2a6 6 0 0 1 5-5.9Z"/>',
    'doc': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Zm-1 7V3.5L18.5 9ZM8 13h8v2H8Zm0 4h8v2H8Zm0-8h3v2H8Z"/>',
    'ruler': '<path d="m2 17 15-15 5 5L7 22Zm4.2 1.4L8 16.6l1.4 1.4 1.4-1.4-1.4-1.4 1.4-1.4 2.1 2.1 1.4-1.4-2.1-2.1 1.4-1.4 1.4 1.4 1.4-1.4-1.4-1.4 1.4-1.4 2.1 2.1 1.4-1.4L16.5 6 4.8 17.7Z"/>',
    'shield': '<path d="M12 2 4 5v6c0 5 3.4 9.7 8 11 4.6-1.3 8-6 8-11V5Zm-1 14-4-4 1.4-1.4L11 13.2l4.6-4.6L17 10Z"/>',
    'user': '<path d="M12 12a5 5 0 1 0-5-5 5 5 0 0 0 5 5Zm0 2c-4.4 0-8 2.2-8 5v2h16v-2c0-2.8-3.6-5-8-5Z"/>',
    'drag': '<path d="M12 2 8 6h3v5H6V8l-4 4 4 4v-3h5v5H8l4 4 4-4h-3v-5h5v3l4-4-4-4v3h-5V6h3z"/>',
}

def icon(name, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'

BRAND_MARK = ('<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true" focusable="false">'
              '<rect x="4" y="27" width="32" height="7" fill="#E5E8E6"/>'
              '<rect x="8" y="17" width="26" height="7" fill="#9FB2C4"/>'
              '<rect x="12" y="7" width="20" height="7" fill="#F2A900"/></svg>')

# ------------------------------------------------------------------ nav
NAV = [('index.html', 'Home'), ('about.html', 'About'), ('services.html', 'Services'),
       ('projects.html', 'Projects'), ('careers.html', 'Careers'), ('blog.html', 'Blog'), ('contact.html', 'Contact')]
SECTION_OF = {  # which nav item is "current" for sub pages
    'project-detail.html': 'projects.html', 'team.html': 'about.html', 'faq.html': 'contact.html',
    'quote.html': None, 'privacy.html': None, 'terms.html': None, '404.html': None,
}

SERVICES = [
    dict(slug='residential-construction', name='Residential construction', img='residential-blue.svg',
         short='New houses and multi-storey homes, built from approved drawings to handover.',
         intro='Whether you are building your first family home or a two-storey residence with rental units, we manage the full build: site preparation, foundations, structure, roofing, services and finishes.',
         scope=['Site clearing, setting out and excavation', 'Foundations, columns, beams and slabs', 'Masonry, plastering and roofing', 'Electrical and plumbing installation', 'Tiling, painting, doors and windows', 'Final cleaning and handover inspection'],
         fit='Homeowners and families planning a new house or an extension.'),
    dict(slug='commercial-construction', name='Commercial construction', img='commercial-blue.svg',
         short='Shops, offices and mixed-use buildings delivered to schedule and budget.',
         intro='Commercial projects need careful sequencing so you can open on time. We plan the programme with you, coordinate trades and keep you updated at each milestone.',
         scope=['Shop houses and retail buildings', 'Office buildings and mixed-use blocks', 'Structural works and frame construction', 'Services coordination (electrical, plumbing)', 'Shop-front and façade works', 'Programme and milestone reporting'],
         fit='Business owners, investors and property developers.'),
    dict(slug='renovation-remodelling', name='Renovation & remodelling', img='renovation-blue.svg',
         short='Extensions, upgrades and repairs that respect what is already there.',
         intro='Renovations start with understanding the existing structure. We inspect first, explain what can and cannot change, and protect the parts of the building you are keeping.',
         scope=['Room additions and upper-floor extensions', 'Kitchen and bathroom remodelling', 'Roof replacement and waterproofing', 'Structural repairs and crack treatment', 'Re-plastering, re-tiling and repainting', 'Shop and office refurbishments'],
         fit='Owners of existing homes and commercial buildings.'),
    dict(slug='civil-works', name='Civil works', img='civil-ink.svg',
         short='Roads, drainage, culverts and site infrastructure.',
         intro='We carry out civil works for private and institutional clients, working from engineered drawings and specifications and following site safety procedures throughout.',
         scope=['Access roads and internal roads', 'Storm-water drains and culverts', 'Retaining walls and boundary walls', 'Concrete works and hard-standing', 'Earthworks and site grading', 'Water and drainage connections'],
         fit='Institutions, developers and government-funded projects.'),
    dict(slug='project-management', name='Project management', img='commercial-ink.svg',
         short='One accountable team coordinating design, trades, cost and time.',
         intro='If you already have designs, we can manage the build on your behalf: planning, procurement, supervision of trades and regular reporting so you always know where the project stands.',
         scope=['Programme planning and scheduling', 'Cost control against the BOQ', 'Subcontractor coordination', 'Quality and safety inspections', 'Progress reports with photos', 'Handover documentation'],
         fit='Clients who want a single point of contact for the whole build.'),
    dict(slug='maintenance-repairs', name='Maintenance & repairs', img='residential-ink.svg',
         short='Planned maintenance and quick repairs to keep buildings in shape.',
         intro='Small problems become expensive if they are left. We offer scheduled maintenance and responsive repairs for homes, shops and offices.',
         scope=['Roof leaks and gutter repairs', 'Damp and waterproofing treatment', 'Plaster, tile and floor repairs', 'Painting and surface protection', 'Plumbing and drainage repairs', 'Pre-monsoon building checks'],
         fit='Homeowners, landlords and facility managers.'),
]

PROJECTS = [
    dict(cat='residential', label='Residential', img='residential-blue.svg', status='Completed'),
    dict(cat='commercial', label='Commercial', img='commercial-blue.svg', status='Completed'),
    dict(cat='civil', label='Civil works', img='civil-ink.svg', status='Ongoing'),
    dict(cat='renovation', label='Renovation', img='renovation-steel.svg', status='Completed'),
    dict(cat='commercial', label='Commercial', img='industrial-steel.svg', status='Ongoing'),
    dict(cat='residential', label='Residential', img='residential-ink.svg', status='Completed'),
]

POSTS = [
    dict(slug='check-a-contractor-before-you-sign', img='commercial-ink.svg', date='[Publish date]', iso='',
         title='How to check a building contractor before you sign',
         excerpt='Six checks that protect your money and your timeline, starting with a contractor\'s CIDA registration.',
         body=[
            ('p', 'Choosing a contractor is the biggest decision in any building project. A careful check before you sign takes a few hours and can save months of delays and lakhs of rupees. These are the checks we recommend to every client, including the ones who choose us.'),
            ('h2', '1. Confirm CIDA registration and grade'),
            ('p', 'In Sri Lanka, contractors carrying out identified construction works are required to register with the Construction Industry Development Authority (CIDA), and CIDA registration is required for government contracts. CIDA grades contractors by category and by the value of work they can take on. You can search contractors who hold a valid registration on the CIDA website. Ask for the registration number and check it yourself.'),
            ('h2', '2. Visit a finished project'),
            ('p', 'Photos can be selected. A site visit cannot. Ask to see a completed building similar to yours and, if possible, speak to the owner about how the job ran.'),
            ('h2', '3. Ask for an itemised quotation'),
            ('p', 'A single total figure tells you very little. An itemised quotation or bill of quantities (BOQ) shows what is included, the specification of materials and the quantities. It also makes it far easier to compare contractors fairly.'),
            ('h2', '4. Agree a payment schedule linked to progress'),
            ('p', 'Payments should follow completed work, for example foundation, structure, roof and finishes, rather than fixed dates. Avoid paying a large share of the contract value up front.'),
            ('h2', '5. Put variations in writing'),
            ('p', 'Changes are normal in construction. Agree in the contract that every change is priced and approved in writing before the work is done.'),
            ('h2', '6. Ask about safety and insurance'),
            ('p', 'Ask how the contractor manages site safety and whether the works and workers are insured. A professional contractor will answer clearly.'),
            ('p', 'If you would like us to walk you through our own registration, references and quotation format, request a consultation.'),
         ]),
    dict(slug='what-to-agree-in-writing', img='residential-blue.svg', date='[Publish date]', iso='',
         title='What to agree in writing before construction starts',
         excerpt='Scope, drawings, payments, variations and defects: the five things your building contract must cover.',
         body=[
            ('p', 'Most construction disputes start with something that was agreed verbally. A clear written contract protects both you and your builder. Before the first excavation, make sure these points are written down and signed.'),
            ('h2', 'Scope and drawings'),
            ('p', 'List the approved drawings and specifications the contractor will build from. If something is not in the drawings or the BOQ, it is not in the price.'),
            ('h2', 'Price and payment schedule'),
            ('p', 'State the contract sum, what it includes, and when each payment is due. Linking payments to completed stages keeps the project moving and your risk low.'),
            ('h2', 'Programme'),
            ('p', 'Agree a start date, key milestones and a completion date, and what happens if either side causes a delay.'),
            ('h2', 'Variations'),
            ('p', 'Set a simple rule: no change is carried out until its cost and time impact is approved in writing.'),
            ('h2', 'Defects and handover'),
            ('p', 'Agree a defects period after handover during which the contractor returns to fix faults in their work, and what documents you receive at handover.'),
         ]),
    dict(slug='building-for-heat-and-heavy-rain', img='renovation-blue.svg', date='[Publish date]', iso='',
         title='Designing a home for heat and heavy rain',
         excerpt='Practical choices for roofs, ventilation and drainage that keep a house cooler and drier year-round.',
         body=[
            ('p', 'A house in a hot climate with intense seasonal rain has two jobs: keep heat out and move water away quickly. Good decisions at the design stage cost little and make a big difference to comfort and maintenance.'),
            ('h2', 'Generous roof overhangs'),
            ('p', 'Deep eaves shade walls and windows from the sun and protect them from driving rain, which reduces both heat gain and damp problems.'),
            ('h2', 'Cross ventilation'),
            ('p', 'Place openings on opposite sides of rooms so air can move through the house. High-level vents let hot air escape.'),
            ('h2', 'Roof and wall insulation'),
            ('p', 'A roof absorbs a lot of heat. Insulation or a ventilated ceiling space under the roof sheet reduces the heat that reaches the rooms below.'),
            ('h2', 'Drainage planned from day one'),
            ('p', 'Plan gutters, downpipes and surface drains with the site levels so storm water flows away from the foundations. Raising the floor level above the surrounding ground helps keep water out.'),
            ('h2', 'Durable finishes'),
            ('p', 'Choose finishes that tolerate humidity: good waterproofing in wet areas, quality external paint, and tiles or screeds that are easy to clean.'),
         ]),
]

JOBS = [
    dict(title='Site engineer', type='Full-time', loc=SITE['region'], desc='Supervise works on site, check quality against drawings and coordinate with the project team.'),
    dict(title='Quantity surveyor', type='Full-time', loc=SITE['region'], desc='Prepare BOQs, measure work done and support cost control on active projects.'),
    dict(title='Skilled masons and carpenters', type='Contract', loc='Project sites', desc='Experienced trades for residential and commercial projects.'),
]

FAQS = [
    ('Which areas do you work in?', f'We are based in {SITE["locality"]}, {SITE["region"]}. Contact us with your site location and we will confirm whether we can take on the project.'),
    ('How do I get a quotation?', 'Send your project details through the quote form or call us. For an accurate quotation we need drawings or a clear description, the site location and your preferred start date. We may arrange a site visit before pricing.'),
    ('Do you work from my architect\'s drawings?', 'Yes. We build from approved drawings and specifications. If you do not have drawings yet, tell us and we will explain the next steps.'),
    ('How long does it take to build a house?', 'It depends on the size, design, approvals and weather. Your quotation includes a programme with key milestones so you know what to expect.'),
    ('How are payments structured?', 'Payments are linked to completed stages of work, as agreed in the contract. You receive an itemised quotation before work starts.'),
    ('Are you registered with CIDA?', f'Our CIDA registration details: {SITE["cida"]}, registration number {SITE["cida_no"]}. You can verify registrations on the CIDA website.'),
    ('What happens if I want to change something during construction?', 'Tell us as early as possible. We will price the change and its effect on time, and carry it out only after you approve it in writing.'),
]

# ------------------------------------------------------------------ partials
def jsonld(obj): return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'

def org_schema():
    return {
        '@context': 'https://schema.org', '@type': 'GeneralContractor', '@id': SITE['url'] + '/#organization',
        'name': SITE['name'], 'url': SITE['url'] + '/', 'telephone': SITE['tel'],
        'image': SITE['url'] + '/assets/img/og-image.svg', 'logo': SITE['url'] + '/assets/img/favicon.svg',
        'address': {'@type': 'PostalAddress', 'streetAddress': SITE['street'], 'addressLocality': SITE['locality'],
                    'addressRegion': SITE['region'], 'addressCountry': 'LK'},
        'areaServed': {'@type': 'AdministrativeArea', 'name': SITE['region']},
    }

def crumbs_schema(trail):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE['url'] + '/' + (h if h != 'index.html' else '')}
        for i, (h, n) in enumerate(trail)]}

def head(page, title, desc, schemas=(), b3d=False, noindex=False):
    canonical = SITE['url'] + '/' + ('' if page == 'index.html' else page)
    full = title if page == 'index.html' else f'{title} | {SITE["name"]}'
    robots = '<meta name="robots" content="noindex, follow">' if noindex else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
{robots}<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0B1A2B">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE['url']}/assets/img/og-image.jpg">
<meta property="og:locale" content="en_LK">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(full)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE['url']}/assets/img/og-image.jpg">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=swap">
<link rel="stylesheet" href="assets/css/main.css">
<script src="assets/js/main.js" defer></script>
{'<script src="assets/js/building3d.js" defer></script>' if b3d else ''}
{''.join(jsonld(s) for s in schemas)}
</head>'''

def header(page):
    current = SECTION_OF.get(page, page)
    def link(h, n, cls=''):
        cur = ' aria-current="page"' if h == current else ''
        return f'<a{cls} href="{h}"{cur}>{n}</a>'
    desk = ''.join(f'<li>{link(h, n)}</li>' for h, n in NAV)
    mob = ''.join(f'<li>{link(h, n, " class=\"m-link\"")}</li>' for h, n in NAV)
    return f'''<body data-phone="{SITE['phone']}">
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container">
    <a class="brand" href="index.html" aria-label="{SITE['name']} home">{BRAND_MARK}<span class="brand-text"><b>R.B.N.</b><small>Construction</small></span></a>
    <nav class="primary-nav" aria-label="Main"><ul class="nav-list">{desk}</ul></nav>
    <a class="header-phone" href="tel:{SITE['tel']}">{SITE['phone']}</a>
    <a class="btn header-cta" href="quote.html">Request a quote</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu">{icon('menu')}</button>
  </div>
</header>
<div class="mobile-nav" id="mobile-nav">
  <nav aria-label="Mobile"><ul>{mob}</ul></nav>
  <a class="btn" href="quote.html">Request a quote</a>
  <a class="btn btn--ghost" href="tel:{SITE['tel']}">{icon('phone')} Call {SITE['phone']}</a>
</div>
<main id="main">'''

def footer():
    svc = ''.join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES)
    return f'''</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-about">
        <a class="brand" href="index.html" aria-label="{SITE['name']} home">{BRAND_MARK}<span class="brand-text"><b>R.B.N.</b><small>Construction</small></span></a>
        <p class="mt-2">Building contractor in {SITE['region']}, Sri Lanka. Homes, commercial buildings, renovation and civil works.</p>
        <p>CIDA: {ph(SITE['cida'])} &nbsp; Reg. no. {ph(SITE['cida_no'])}</p>
      </div>
      <nav aria-label="Services"><h2>Services</h2><ul>{svc}</ul></nav>
      <nav aria-label="Company"><h2>Company</h2><ul>
        <li><a href="about.html">About us</a></li><li><a href="team.html">Our team</a></li><li><a href="projects.html">Projects</a></li>
        <li><a href="careers.html">Careers</a></li><li><a href="blog.html">Blog</a></li><li><a href="faq.html">FAQ</a></li></ul></nav>
      <div><h2>Contact</h2><ul class="footer-contact">
        <li>{icon('pin')}<span>{ADDRESS}</span></li>
        <li>{icon('phone')}<a href="tel:{SITE['tel']}">{SITE['phone']}</a></li>
        <li>{icon('wa')}<a href="https://wa.me/{SITE['wa']}" rel="noopener" target="_blank">WhatsApp us</a></li>
        <li>{icon('mail')}<span>{ph(SITE['email'])}</span></li>
        <li>{icon('clock')}<span>{ph(SITE['hours'])}</span></li></ul></div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> {SITE['name']}. All rights reserved.</span>
      <nav aria-label="Legal"><a href="privacy.html">Privacy policy</a><a href="terms.html">Terms</a><a href="sitemap.xml">Sitemap</a></nav>
      <span>Website by <a href="https://uiddevelopers.com" rel="noopener" target="_blank">UIDD</a></span>
    </div>
  </div>
</footer>
<nav class="action-bar" aria-label="Quick contact">
  <a href="tel:{SITE['tel']}">{icon('phone')}Call</a>
  <a href="https://wa.me/{SITE['wa']}" rel="noopener" target="_blank">{icon('wa')}WhatsApp</a>
  <a class="is-primary" href="quote.html">Get a quote</a>
</nav>
<a class="wa-float" href="https://wa.me/{SITE['wa']}" rel="noopener" target="_blank" aria-label="Chat with us on WhatsApp">{icon('wa')}</a>
</body>
</html>
'''

def page_hero(title, lead, trail):
    items = ''.join(
        f'<li><a href="{h}">{n}</a></li>' if i < len(trail) - 1 else f'<li aria-current="page">{n}</li>'
        for i, (h, n) in enumerate(trail))
    return f'''<section class="page-hero"><div class="container">
<nav class="breadcrumb" aria-label="Breadcrumb"><ol>{items}</ol></nav>
<h1>{title}</h1><p>{lead}</p></div></section>'''

def cta_band(h='Planning a build? Talk to us before you finalise drawings.', p='Early advice on structure, materials and sequence saves money later.'):
    return f'''<section class="cta-band" aria-labelledby="cta-h"><div class="container">
<div><h2 id="cta-h">{h}</h2><p>{p}</p></div>
<div class="cta-actions"><a class="btn btn--dark" href="quote.html">Request a quote</a><a class="btn btn--ghost" href="tel:{SITE['tel']}">{icon('phone')} {SITE['phone']}</a></div>
</div></section>'''

def img(src, alt, eager=False, w=1200, h=900):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="assets/img/{src}" alt="{esc(alt)}" width="{w}" height="{h}" decoding="async" {load}>'

def project_card(p, i, big=False):
    return f'''<a class="project-card" href="project-detail.html" data-category="{p['cat']}">
<div class="media">{img(p['img'], p['label'] + ' project drawing')}</div>
<h3>{ph('[Project name]')}</h3>
<div class="project-meta"><span class="chip">{p['label']}</span><span>{ph('[Location]')}, {ph('[Year]')}</span>
<span class="status{' status--ongoing' if p['status'] == 'Ongoing' else ''}">{p['status']}</span></div></a>'''

def write(name, content):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(content)
    print('wrote', name)

def form_common():
    return ('<input type="hidden" name="csrf_token" value="">'
            '<input type="hidden" name="form_started" value="">'
            '<div class="hp-field" aria-hidden="true"><label for="website">Leave this field empty</label>'
            '<input id="website" name="website" type="text" tabindex="-1" autocomplete="off"></div>')

def field(id_, label, type_='text', required=True, attrs='', hint='', opt_label=True):
    req = ' required' if required else ''
    opt = '' if required or not opt_label else ' <span class="opt">(optional)</span>'
    hint_html = f'<p class="field-hint" id="{id_}-hint">{hint}</p>' if hint else ''
    desc = f' aria-describedby="{id_}-hint"' if hint else ''
    if type_ == 'textarea':
        control = f'<textarea id="{id_}" name="{id_}"{req}{desc} {attrs}></textarea>'
    else:
        control = f'<input id="{id_}" name="{id_}" type="{type_}"{req}{desc} {attrs}>'
    return f'<div class="field"><label for="{id_}">{label}{opt}</label>{hint_html}{control}</div>'

# ================================================================== PAGES
def home():
    svc_rows = ''.join(f'''<li class="service-row"><a href="{s['slug']}.html">
<h3>{s['name']}</h3><p>{s['short']}</p><span class="row-arrow" aria-hidden="true">{icon('arrow')}</span></a></li>''' for s in SERVICES)
    feat = ''.join(project_card(p, i) for i, p in enumerate(PROJECTS[:3]))
    steps = [
        ('Site visit and brief', 'We visit the site, review drawings or ideas, and confirm what you need, your budget range and your timeline.'),
        ('Foundations', 'Setting out, excavation and foundations, checked against the structural drawings before concrete is poured.'),
        ('Structure', 'Columns, beams and slabs floor by floor, with scaffolding, formwork and inspections at each level.'),
        ('Envelope and services', 'Walls, roof, windows, electrical and plumbing, so the building is weather-tight and ready for finishes.'),
        ('Finishes and handover', 'Finishes, snag checks and cleaning. You receive the keys, documents and a walkthrough of the building.'),
    ]
    step_html = ''.join(f'<li class="build-step" data-build-step="{i}"><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(steps))
    tabs = ''.join(f'<button type="button" class="stage-tab" data-stage-tab="{i}" aria-pressed="false">{n}</button>'
                   for i, n in enumerate(['Plan', 'Foundation', 'Structure', 'Envelope', 'Handover']))
    body = f'''
<section class="hero" aria-labelledby="hero-h">
  <div class="container hero-inner">
    <div>
      <p class="kicker">Building contractor in {SITE['region']}</p>
      <h1 id="hero-h">We build what the drawings promise.</h1>
      <p class="hero-lead">Homes, commercial buildings and civil works, delivered by one team that stays accountable from the first site visit to handover.</p>
      <div class="hero-actions">
        <a class="btn" href="quote.html">Request a quote</a>
        <a class="btn btn--ghost" href="projects.html">See our projects</a>
      </div>
      <div class="hero-meta">
        <span>{icon('phone')}<a href="tel:{SITE['tel']}">{SITE['phone']}</a></span>
        <span>{icon('pin')}{SITE['locality']}, {SITE['region']}</span>
      </div>
    </div>
    <div>
      <div class="b3d b3d-hero" id="hero-model" data-building3d data-autoplay data-stage="4"
        aria-label="3D model of a building going through five construction stages. Drag or use arrow keys to rotate."></div>
      <div class="b3d-ui" data-b3d-ui="hero-model">
        <div class="stage-tabs" role="group" aria-label="Construction stage">{tabs}</div>
        <span class="b3d-hint">{icon('drag')}Drag to rotate</span>
      </div>
    </div>
  </div>
</section>

<div class="container facts-wrap">
  <dl class="facts">
    <div class="fact"><dt>CIDA grade</dt><dd>{ph(SITE['cida'])}</dd></div>
    <div class="fact"><dt>CIDA registration</dt><dd>{ph(SITE['cida_no'])}</dd></div>
    <div class="fact"><dt>Building since</dt><dd>{ph(SITE['founded'])}</dd></div>
    <div class="fact"><dt>Based in</dt><dd>{SITE['region']}</dd></div>
    <div class="fact"><dt>Call the office</dt><dd><a href="tel:{SITE['tel']}" class="link">{SITE['phone']}</a></dd></div>
  </dl>
</div>

<section class="section" aria-labelledby="svc-h">
  <div class="container">
    <div class="section-head">
      <div><p class="kicker">What we build</p><h2 id="svc-h">Construction services</h2></div>
      <p>Choose a service to see the scope of work, how we run the project and what to prepare before you contact us.</p>
    </div>
    <ul class="service-index">{svc_rows}</ul>
  </div>
</section>

<section class="section section--concrete" aria-labelledby="proj-h">
  <div class="container">
    <div class="section-head">
      <div><p class="kicker">Recent work</p><h2 id="proj-h">Selected projects</h2></div>
      <p>Each project page shows the scope, the challenges on site and how we solved them. <a class="link" href="projects.html">View all projects</a></p>
    </div>
    <div class="project-grid project-grid--feature">{feat}</div>
  </div>
</section>

<section class="section section--ink" aria-labelledby="build-h">
  <div class="container">
    <div class="section-head">
      <div><p class="kicker">How we work</p><h2 id="build-h">From empty site to handover, in five stages</h2></div>
      <p>Scroll to watch the building go up. You get a programme with these milestones in every quotation, and payments are linked to them.</p>
    </div>
    <div class="build">
      <div class="build-stage"><div class="b3d" id="process-model" data-building3d data-stage="0"
        aria-label="3D model that changes as you scroll through the construction stages."></div></div>
      <ol class="build-steps" data-build-steps="process-model">{step_html}</ol>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="why-h">
  <div class="container grid-2">
    <div>
      <p class="kicker">Why clients choose us</p>
      <h2 id="why-h">Clear prices, safe sites, honest updates</h2>
      <p class="text-steel">Construction is a large commitment. These are the standards we work to on every project, whatever its size.</p>
      <a class="btn btn--dark mt-2" href="about.html">About R.B.N. Construction</a>
    </div>
    <ul class="commit-list">
      <li>{icon('doc')}<div><h3>Itemised quotations</h3><p>A BOQ-based quotation so you can see exactly what is included before you sign.</p></div></li>
      <li>{icon('helmet')}<div><h3>Safety on every site</h3><p>Protective equipment, safe scaffolding and daily site checks for our workers and your neighbours.</p></div></li>
      <li>{icon('ruler')}<div><h3>Built to the drawings</h3><p>Work is checked against approved drawings at each stage before we move on.</p></div></li>
      <li>{icon('user')}<div><h3>One point of contact</h3><p>A named site lead who answers your calls and sends regular progress updates with photos.</p></div></li>
    </ul>
  </div>
</section>

<section class="section section--concrete" aria-labelledby="plan-h">
  <div class="container">
    <div class="section-head">
      <div><p class="kicker">Plan your build</p><h2 id="plan-h">Work out your floor area in seconds</h2></div>
      <p>Enter the basics and send them straight to our quote form. We use this to prepare for your consultation.</p>
    </div>
    <form class="planner" data-planner aria-label="Build planner">
      <div class="form">
        <fieldset class="field"><legend>Project type</legend>
          <div class="choice-grid">
            <label class="choice"><input type="radio" name="type" value="residential" checked><span>New house</span></label>
            <label class="choice"><input type="radio" name="type" value="commercial"><span>Commercial building</span></label>
            <label class="choice"><input type="radio" name="type" value="renovation"><span>Renovation or extension</span></label>
          </div></fieldset>
        <div class="form-row">
          <div class="field"><label for="pl-floors">Number of floors</label><input id="pl-floors" name="floors" type="number" min="1" max="10" value="2" inputmode="numeric"></div>
          <div class="field"><label for="pl-area">Area per floor (sq ft)</label><input id="pl-area" name="area" type="number" min="100" max="100000" step="50" value="1200" inputmode="numeric"></div>
        </div>
        <div class="field"><label for="pl-finish">Finish level</label>
          <select id="pl-finish" name="finish"><option value="standard">Standard</option><option value="premium">Premium</option><option value="luxury">Luxury</option></select></div>
      </div>
      <div class="planner-out" aria-live="polite">
        <dl><div><dt>Total floor area</dt><dd data-out="total">—</dd></div><div><dt>In square metres</dt><dd data-out="sqm">—</dd></div></dl>
        <p class="note">Final pricing depends on drawings, site conditions and specifications. We confirm it in a written quotation.</p>
        <a class="btn" data-out="link" href="quote.html">Send to quote form</a>
      </div>
    </form>
  </div>
</section>

<section class="section" aria-labelledby="client-h">
  <div class="container grid-2">
    <div><p class="kicker">Client feedback</p><h2 id="client-h">What our clients say</h2>
      <p class="text-steel">Add real testimonials here, with the client's written permission.</p></div>
    <figure class="quote-block"><blockquote>{ph('[Client testimonial — add a real quote with permission]')}</blockquote>
      <figcaption>{ph('[Client name]')}, {ph('[Project type, location]')}</figcaption></figure>
  </div>
</section>
{cta_band()}'''
    schemas = [org_schema(), {'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE['name'], 'url': SITE['url'] + '/'}]
    write('index.html', head('index.html', f'{SITE["name"]} | Building contractor in {SITE["region"]}, Sri Lanka',
          f'{SITE["name"]} builds homes, commercial buildings and civil works in {SITE["region"]}. Itemised quotations, safe sites and one accountable team. Call {SITE["phone"]}.',
          schemas, b3d=True) + header('index.html') + body + footer())

def about():
    trail = [('index.html', 'Home'), ('about.html', 'About')]
    body = page_hero('A building contractor you can hold to a plan', f'{SITE["name"]} is a construction company based in {SITE["locality"]}, {SITE["region"]}.', trail) + f'''
<section class="section"><div class="container layout-aside">
  <div class="prose">
    <h2 class="mt-0">Our story</h2>
    <p>{ph('[COMPANY HISTORY — how and when the company started, the founder, and how it has grown.]')}</p>
    <h2>Mission</h2><p>{ph('[Mission statement supplied by the client]')}</p>
    <h2>Vision</h2><p>{ph('[Vision statement supplied by the client]')}</p>
    <h2>How we work</h2>
    <ul class="check-list">
      <li>We give itemised quotations, so you know what you are paying for.</li>
      <li>We link payments to completed stages of work.</li>
      <li>We check our work against approved drawings before moving to the next stage.</li>
      <li>We keep sites safe, tidy and secure.</li>
      <li>We put every change in writing before doing the work.</li>
    </ul>
    <h2>Safety commitment</h2>
    <p>Everyone on our sites goes home safe. We provide protective equipment, inspect scaffolding and formwork, keep walkways clear, and brief workers before high-risk tasks.</p>
    <h2>Quality commitment</h2>
    <p>Quality is checked as we build, not at the end. Concrete, reinforcement and finishes are inspected at each stage, and defects found after handover are corrected within the agreed defects period.</p>
  </div>
  <aside class="aside-card">
    <h2>Company details</h2>
    <table class="info-table"><tbody>
      <tr><th scope="row">Registered name</th><td>{SITE['name']}</td></tr>
      <tr><th scope="row">CIDA grade</th><td>{ph(SITE['cida'])}</td></tr>
      <tr><th scope="row">CIDA reg. no.</th><td>{ph(SITE['cida_no'])}</td></tr>
      <tr><th scope="row">Business reg. no.</th><td>{ph(SITE['br_no'])}</td></tr>
      <tr><th scope="row">Established</th><td>{ph(SITE['founded'])}</td></tr>
      <tr><th scope="row">Office</th><td>{ADDRESS}</td></tr>
    </tbody></table>
    <a class="btn btn--block mt-2" href="team.html">Meet the team</a>
  </aside>
</div></section>
<section class="section section--concrete"><div class="container">
  <div class="section-head"><div><h2>Certifications and memberships</h2></div><p>Copies of certificates are available on request.</p></div>
  <dl class="facts" style="margin-top:0">
    <div class="fact"><dt>CIDA registration</dt><dd>{ph('[Grade, category]')}</dd></div>
    <div class="fact"><dt>Certification</dt><dd>{ph('[e.g. ISO certificate]')}</dd></div>
    <div class="fact"><dt>Membership</dt><dd>{ph('[Association]')}</dd></div>
    <div class="fact"><dt>Insurance</dt><dd>{ph('[Insurance cover]')}</dd></div>
    <div class="fact"><dt>Award</dt><dd>{ph('[Only if real]')}</dd></div>
  </dl>
</div></section>''' + cta_band()
    write('about.html', head('about.html', 'About us', f'Learn about {SITE["name"]}, a building contractor in {SITE["region"]}: our story, safety and quality commitments, and CIDA registration.',
          [org_schema(), crumbs_schema(trail)]) + header('about.html') + body + footer())

def services():
    trail = [('index.html', 'Home'), ('services.html', 'Services')]
    cards = ''.join(f'''<a class="project-card" href="{s['slug']}.html"><div class="media">{img(s['img'], s['name'] + ' drawing')}</div>
<h3>{s['name']}</h3><p class="text-steel mb-0">{s['short']}</p></a>''' for s in SERVICES)
    body = page_hero('Construction services', 'From a single-room extension to a multi-storey building, here is what we do and how each service works.', trail) + f'''
<section class="section"><div class="container"><div class="project-grid project-grid--all">{cards}</div></div></section>
<section class="section section--concrete"><div class="container grid-2">
  <div><h2>Not sure which service you need?</h2><p class="text-steel">Describe your project and we will recommend the right approach. Many projects combine services, for example a renovation with structural repairs.</p></div>
  <div><a class="btn btn--dark" href="quote.html">Describe your project</a></div>
</div></section>''' + cta_band()
    sch = [crumbs_schema(trail)] + [{'@context': 'https://schema.org', '@type': 'Service', 'name': s['name'], 'description': s['short'],
            'provider': {'@id': SITE['url'] + '/#organization'}, 'areaServed': SITE['region'], 'url': f"{SITE['url']}/{s['slug']}.html"} for s in SERVICES]
    write('services.html', head('services.html', 'Construction services', f'Residential and commercial construction, renovation, civil works, project management and maintenance in {SITE["region"]}.', sch)
          + header('services.html') + body + footer())

def service_detail(s):
    page = s['slug'] + '.html'
    SECTION_OF[page] = 'services.html'
    trail = [('index.html', 'Home'), ('services.html', 'Services'), (page, s['name'])]
    others = ''.join(f'<li><a class="link" href="{o["slug"]}.html">{o["name"]}</a></li>' for o in SERVICES if o is not s)
    scope = ''.join(f'<li>{x}</li>' for x in s['scope'])
    related = [p for p in PROJECTS if p['cat'] in s['slug']][:2] or PROJECTS[:2]
    body = page_hero(s['name'], s['short'], trail) + f'''
<section class="section"><div class="container layout-aside">
  <div class="prose">
    <div class="media mb-2">{img(s['img'], s['name'] + ' drawing', eager=True)}</div>
    <h2 class="mt-0">Overview</h2><p>{s['intro']}</p>
    <h2>Scope of work</h2><ul class="check-list">{scope}</ul>
    <h2>Who this is for</h2><p>{s['fit']}</p>
    <h2>How the project runs</h2>
    <ol><li><strong>Brief and site visit.</strong> We understand your needs and inspect the site.</li>
      <li><strong>Itemised quotation.</strong> You receive a BOQ-based price and programme.</li>
      <li><strong>Agreement.</strong> Scope, payments and timeline are agreed in writing.</li>
      <li><strong>Construction.</strong> Work proceeds stage by stage with regular updates.</li>
      <li><strong>Handover.</strong> Final inspection, documents and a walkthrough.</li></ol>
    <h2>What to prepare before you contact us</h2>
    <ul><li>Drawings or sketches, if you have them</li><li>Site location and land size</li><li>Your preferred start date and budget range</li></ul>
  </div>
  <aside class="aside-card">
    <h2>Get a quotation</h2><p class="text-steel">Tell us about your {s['name'].lower()} project.</p>
    <a class="btn btn--block" href="quote.html?type={'renovation' if 'renov' in s['slug'] else ('commercial' if 'commercial' in s['slug'] else 'residential')}">Request a quote</a>
    <a class="btn btn--ghost btn--block mt-2" href="tel:{SITE['tel']}">{icon('phone')} {SITE['phone']}</a>
    <h3 class="mt-2">Other services</h3><ul style="list-style:none;padding:0;display:grid;gap:.5rem">{others}</ul>
  </aside>
</div></section>
<section class="section section--concrete"><div class="container">
  <div class="section-head"><div><h2>Related projects</h2></div><p><a class="link" href="projects.html">All projects</a></p></div>
  <div class="project-grid">{''.join(project_card(p, i) for i, p in enumerate(related))}</div>
</div></section>''' + cta_band()
    sch = [crumbs_schema(trail), {'@context': 'https://schema.org', '@type': 'Service', 'name': s['name'], 'description': s['intro'],
           'provider': {'@id': SITE['url'] + '/#organization'}, 'areaServed': SITE['region']}]
    write(page, head(page, s['name'], f'{s["name"]} by {SITE["name"]} in {SITE["region"]}. {s["short"]}', sch) + header(page) + body + footer())

def projects():
    trail = [('index.html', 'Home'), ('projects.html', 'Projects')]
    filters = [('all', 'All'), ('residential', 'Residential'), ('commercial', 'Commercial'), ('renovation', 'Renovation'), ('civil', 'Civil works')]
    fb = ''.join(f'<button type="button" class="filter-btn" data-filter="{k}" aria-pressed="{str(k == "all").lower()}">{n}</button>' for k, n in filters)
    cards = ''.join(project_card(p, i) for i, p in enumerate(PROJECTS))
    body = page_hero('Projects', 'Completed and ongoing work. Filter by type, then open a project to see the scope, challenges and results.', trail) + f'''
<section class="section"><div class="container">
  <div class="filters" data-filters role="group" aria-label="Filter projects by type">{fb}</div>
  <p class="visually-hidden" aria-live="polite" data-filter-count></p>
  <div class="project-grid project-grid--all">{cards}</div>
  <div class="empty-state" data-filter-empty hidden><p>No projects in this category yet.</p><a class="link" href="quote.html">Ask us about this type of project</a></div>
</div></section>''' + cta_band('Have a similar project in mind?', 'Tell us what you are planning and we will share relevant examples.')
    write('projects.html', head('projects.html', 'Projects', f'Residential, commercial, renovation and civil construction projects by {SITE["name"]}.', [crumbs_schema(trail)])
          + header('projects.html') + body + footer())

def project_detail():
    trail = [('index.html', 'Home'), ('projects.html', 'Projects'), ('project-detail.html', '[Project name]')]
    gallery = ''.join(f'<button type="button" data-lightbox="assets/img/{g}"><div class="media">{img(g, "Project image " + str(i + 1))}</div><span class="visually-hidden">Open image {i + 1}</span></button>'
                      for i, g in enumerate(['residential-blue.svg', 'renovation-blue.svg', 'interior-blue.svg', 'residential-ink.svg', 'interior-steel.svg', 'renovation-steel.svg']))
    body = page_hero(ph('[Project name]'), ph('[One-sentence project summary]'), trail) + f'''
<section class="section"><div class="container layout-aside">
  <div class="prose">
    <div class="media mb-2">{img('residential-blue.svg', 'Main project image', eager=True)}</div>
    <h2 class="mt-0">Project overview</h2><p>{ph('[PROJECT DESCRIPTION — what was built, for whom, and why.]')}</p>
    <h2>Scope of work</h2><ul class="check-list"><li>{ph('[Scope item]')}</li><li>{ph('[Scope item]')}</li><li>{ph('[Scope item]')}</li></ul>
  </div>
  <aside class="aside-card"><h2>Project information</h2>
    <table class="info-table"><tbody>
      <tr><th scope="row">Client</th><td>{ph('[Client — with permission]')}</td></tr>
      <tr><th scope="row">Location</th><td>{ph('[Location]')}</td></tr>
      <tr><th scope="row">Category</th><td>{ph('[Category]')}</td></tr>
      <tr><th scope="row">Status</th><td>{ph('[Completed / Ongoing]')}</td></tr>
      <tr><th scope="row">Completion</th><td>{ph('[Month Year]')}</td></tr>
      <tr><th scope="row">Floor area</th><td>{ph('[sq ft]')}</td></tr>
      <tr><th scope="row">Value</th><td>{ph('[Only if client agrees]')}</td></tr>
    </tbody></table>
    <a class="btn btn--block mt-2" href="quote.html">Plan a similar project</a></aside>
</div></section>
<section class="section section--concrete"><div class="container">
  <h2>Challenges, solutions and results</h2>
  <div class="case-steps mt-2">
    <article><h3>The challenge</h3><p>{ph('[What made this project difficult: site, time, budget, ground conditions]')}</p></article>
    <article><h3>Our solution</h3><p>{ph('[How the team solved it]')}</p></article>
    <article><h3>The result</h3><p>{ph('[Outcome: handed over on time, within budget, client feedback]')}</p></article>
  </div>
</div></section>
<section class="section"><div class="container"><h2>Gallery</h2><div class="gallery mt-2">{gallery}</div></div></section>
<dialog class="lightbox" id="lightbox" aria-label="Image viewer"><button class="lightbox-close" type="button" aria-label="Close image">{icon('close')}</button><img src="" alt=""></dialog>
<section class="section section--concrete"><div class="container">
  <div class="section-head"><div><h2>Related projects</h2></div></div>
  <div class="project-grid project-grid--all">{''.join(project_card(p, i) for i, p in enumerate(PROJECTS[1:4]))}</div>
</div></section>''' + cta_band()
    write('project-detail.html', head('project-detail.html', 'Project case study', f'Case study of a construction project by {SITE["name"]}: scope, challenges, solutions and results.', [crumbs_schema(trail)])
          + header('project-detail.html') + body + footer())

def team():
    trail = [('index.html', 'Home'), ('about.html', 'About'), ('team.html', 'Team')]
    cards = ''.join(f'<article class="team-card"><div class="media">{img("team-placeholder.svg", "Photo of team member", w=800, h=1000)}</div><h3>{ph("[Name]")}</h3><p>{ph(r)}</p></article>'
                    for r in ['[Managing Director]', '[Chief Engineer]', '[Quantity Surveyor]', '[Site Manager]'])
    body = page_hero('The people who run your project', 'Meet the team responsible for planning, building and handing over your project.', trail) + f'''
<section class="section"><div class="container"><div class="team-grid">{cards}</div></div></section>''' + cta_band('Want to work with us?', 'We are always looking for skilled engineers and trades.')
    write('team.html', head('team.html', 'Our team', f'Meet the engineers and managers at {SITE["name"]}.', [crumbs_schema(trail)]) + header('team.html') + body + footer())

def careers():
    trail = [('index.html', 'Home'), ('careers.html', 'Careers')]
    jobs = ''.join(f'''<li class="job"><div><h3>{j['title']}</h3><div class="project-meta"><span class="chip">{j['type']}</span><span>{j['loc']}</span></div>
<p class="text-steel mb-0 mt-2" style="margin-top:.5rem">{j['desc']}</p></div><a class="btn btn--ghost" href="#apply" data-role="{esc(j['title'])}">Apply</a></li>''' for j in JOBS)
    body = page_hero('Build your career with us', 'We hire engineers, surveyors and skilled trades who take pride in their work and in site safety.', trail) + f'''
<section class="section"><div class="container">
  <div class="section-head"><div><h2>Open positions</h2></div><p>Listings are examples. {ph('[Update with current vacancies]')}</p></div>
  <ul class="job-list">{jobs}</ul>
</div></section>
<section class="section section--concrete" id="apply"><div class="container grid-2">
  <div><h2>Apply</h2><p class="text-steel">Send your details and we will contact you if there is a suitable role. Please attach your CV by email after submitting, or bring it to our office.</p></div>
  <form class="form" action="api/submit.php" method="post" data-validate data-token-url="api/token.php" data-success="Application sent. We will contact you if your profile matches a role.">
    <input type="hidden" name="form_type" value="career">{form_common()}
    <div class="form-row">{field('name', 'Full name', attrs='autocomplete="name" maxlength="100"')}{field('phone', 'Phone number', 'tel', attrs='autocomplete="tel" pattern="[0-9 +()-]{9,20}" data-error="Enter a phone number, for example 077 123 4567."')}</div>
    {field('email', 'Email', 'email', required=False, attrs='autocomplete="email" maxlength="150"')}
    <div class="field"><label for="role">Position</label><select id="role" name="role" required><option value="">Select a position</option>{''.join(f'<option>{j["title"]}</option>' for j in JOBS)}<option>Other</option></select></div>
    {field('message', 'Experience and qualifications', 'textarea', attrs='maxlength="2000" minlength="20"')}
    <div class="form-status" role="status" tabindex="-1"></div>
    <button class="btn" type="submit">Send application</button>
  </form>
</div></section>'''
    write('careers.html', head('careers.html', 'Careers', f'Jobs at {SITE["name"]}: site engineers, quantity surveyors and skilled trades in {SITE["region"]}.', [crumbs_schema(trail)])
          + header('careers.html') + body + footer())

def blog():
    trail = [('index.html', 'Home'), ('blog.html', 'Blog')]
    cards = ''.join(f'''<a class="post-card" href="{p['slug']}.html"><div class="media">{img(p['img'], '')}</div>
<time>{ph(p['date'])}</time><h3>{p['title']}</h3><p class="text-steel mb-0">{p['excerpt']}</p></a>''' for p in POSTS)
    body = page_hero('Advice for building owners', 'Practical guidance on planning, contracts and building well in Sri Lanka.', trail) + f'''
<section class="section"><div class="container"><div class="post-grid">{cards}</div></div></section>''' + cta_band()
    write('blog.html', head('blog.html', 'Blog', 'Construction advice for homeowners and businesses: checking contractors, contracts and building for heat and rain.', [crumbs_schema(trail)])
          + header('blog.html') + body + footer())

def post(p):
    page = p['slug'] + '.html'
    SECTION_OF[page] = 'blog.html'
    trail = [('index.html', 'Home'), ('blog.html', 'Blog'), (page, p['title'])]
    content = ''.join(f'<{t}>{x}</{t}>' for t, x in p['body'])
    others = ''.join(f'<li><a class="link" href="{o["slug"]}.html">{o["title"]}</a></li>' for o in POSTS if o is not p)
    body = page_hero(p['title'], p['excerpt'], trail) + f'''
<section class="section"><div class="container layout-aside">
  <article class="prose"><p class="text-steel"><time>{ph(p['date'])}</time> &nbsp; By {ph('[Author]')}</p>
    <div class="media mb-2">{img(p['img'], '', eager=True)}</div>{content}
    <p><a class="btn mt-2" href="quote.html">Request a consultation</a></p></article>
  <aside class="aside-card"><h2>More articles</h2><ul style="list-style:none;padding:0;display:grid;gap:.75rem">{others}</ul></aside>
</div></section>'''
    sch = [crumbs_schema(trail), {'@context': 'https://schema.org', '@type': 'Article', 'headline': p['title'], 'description': p['excerpt'],
           'publisher': {'@id': SITE['url'] + '/#organization'}, 'mainEntityOfPage': f"{SITE['url']}/{page}", 'image': f"{SITE['url']}/assets/img/{p['img']}"}]
    write(page, head(page, p['title'], p['excerpt'], sch) + header(page) + body + footer())

def contact():
    trail = [('index.html', 'Home'), ('contact.html', 'Contact')]
    body = page_hero('Contact us', 'Call, WhatsApp or send a message. For project pricing, the quote form is the fastest route.', trail) + f'''
<section class="section"><div class="container grid-2">
  <div class="stack">
    <div class="contact-cards">
      <a class="contact-cards-link" href="tel:{SITE['tel']}">{icon('phone')}<span><small>Phone</small><strong>{SITE['phone']}</strong></span></a>
      <a class="contact-cards-link" href="https://wa.me/{SITE['wa']}" rel="noopener" target="_blank">{icon('wa')}<span><small>WhatsApp</small><strong>Chat with us</strong></span></a>
      <div>{icon('mail')}<span><small>Email</small><strong>{ph(SITE['email'])}</strong></span></div>
      <div>{icon('pin')}<span><small>Office</small><strong>{ADDRESS}</strong></span></div>
      <div>{icon('clock')}<span><small>Business hours</small><strong>{ph(SITE['hours'])}</strong></span></div>
    </div>
    <iframe class="map-frame" title="Map showing the {SITE['name']} office in {SITE['locality']}, {SITE['region']}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
      src="https://www.google.com/maps?q={MAP_Q}&output=embed"></iframe>
    <p><a class="link" href="https://www.google.com/maps/search/?api=1&query={MAP_Q}" rel="noopener" target="_blank">Open in Google Maps</a></p>
  </div>
  <div>
    <h2>Send a message</h2>
    <form class="form" action="api/submit.php" method="post" data-validate data-token-url="api/token.php">
      <input type="hidden" name="form_type" value="contact">{form_common()}
      <div class="form-row">{field('name', 'Full name', attrs='autocomplete="name" maxlength="100"')}{field('phone', 'Phone number', 'tel', attrs='autocomplete="tel" pattern="[0-9 +()-]{9,20}" data-error="Enter a phone number, for example 077 123 4567."')}</div>
      {field('email', 'Email', 'email', required=False, attrs='autocomplete="email" maxlength="150"')}
      {field('message', 'Message', 'textarea', attrs='maxlength="2000" minlength="10"')}
      <p class="field-hint">We use your details only to reply to you. See our <a href="privacy.html">privacy policy</a>.</p>
      <div class="form-status" role="status" tabindex="-1"></div>
      <button class="btn" type="submit">Send message</button>
    </form>
    <div class="aside-card mt-2"><h3>Need a price?</h3><p class="text-steel">The quote form asks the right questions so we can respond with useful numbers.</p><a class="link" href="quote.html">Request a quote</a></div>
  </div>
</div></section>'''
    sch = [crumbs_schema(trail), dict(org_schema(), **{'@type': ['GeneralContractor', 'LocalBusiness']})]
    write('contact.html', head('contact.html', 'Contact', f'Contact {SITE["name"]} in {SITE["locality"]}, {SITE["region"]}. Call {SITE["phone"]} or WhatsApp us.', sch)
          + header('contact.html') + body + footer())

def quote():
    trail = [('index.html', 'Home'), ('quote.html', 'Request a quote')]
    types = [('residential', 'New house'), ('commercial', 'Commercial building'), ('renovation', 'Renovation / extension'),
             ('civil', 'Civil works'), ('maintenance', 'Maintenance / repairs'), ('other', 'Something else')]
    tchoice = ''.join(f'<label class="choice"><input type="radio" name="project_type" value="{v}" required><span>{n}</span></label>' for v, n in types)
    budget = ''.join(f'<option>{b}</option>' for b in ['Under LKR 5 million', 'LKR 5–15 million', 'LKR 15–50 million', 'Over LKR 50 million', 'Not sure yet'])
    start = ''.join(f'<option>{b}</option>' for b in ['As soon as possible', 'Within 3 months', '3–6 months', 'More than 6 months', 'Just exploring'])
    body = page_hero('Request a quote', 'Three short steps. We reply within one working day to arrange a call or site visit.', trail) + f'''
<section class="section"><div class="container layout-aside">
  <form class="form" action="api/submit.php" method="post" data-validate data-wizard data-token-url="api/token.php"
    data-success="Quote request sent. We will contact you within one working day.">
    <input type="hidden" name="form_type" value="quote">{form_common()}
    <ol class="steps-nav" aria-label="Form progress"><li>1. Project</li><li>2. Details</li><li>3. Your contact</li></ol>

    <div class="form-step">
      <fieldset class="field"><legend><h2 class="mb-0" style="font-size:var(--fs-xl)">What do you want to build?</h2></legend>
        <div class="choice-grid">{tchoice}</div></fieldset>
      <div class="step-actions"><span></span><button type="button" class="btn" data-next>Continue</button></div>
    </div>

    <div class="form-step" hidden>
      <h2 style="font-size:var(--fs-xl)">Project details</h2>
      {field('location', 'Site location', attrs='maxlength="150" placeholder="Town or area"')}
      <div class="form-row">
        {field('floors', 'Number of floors', 'number', required=False, attrs='min="1" max="50" inputmode="numeric"')}
        {field('floor_area', 'Area per floor (sq ft)', 'number', required=False, attrs='min="0" max="1000000" inputmode="numeric"')}
      </div>
      <div class="form-row">
        <div class="field"><label for="budget">Budget range <span class="opt">(optional)</span></label><select id="budget" name="budget"><option value="">Select</option>{budget}</select></div>
        <div class="field"><label for="start">When do you want to start?</label><select id="start" name="start" required><option value="">Select</option>{start}</select></div>
      </div>
      <div class="field"><label for="drawings">Do you have drawings?</label><select id="drawings" name="drawings" required><option value="">Select</option><option>Yes, approved</option><option>Yes, not yet approved</option><option>No, not yet</option></select></div>
      {field('details', 'Tell us more', 'textarea', required=False, attrs='maxlength="3000"')}
      <div class="step-actions"><button type="button" class="btn btn--ghost" data-prev>Back</button><button type="button" class="btn" data-next>Continue</button></div>
    </div>

    <div class="form-step" hidden>
      <h2 style="font-size:var(--fs-xl)">How can we reach you?</h2>
      <div class="form-row">{field('name', 'Full name', attrs='autocomplete="name" maxlength="100"')}{field('phone', 'Phone number', 'tel', attrs='autocomplete="tel" pattern="[0-9 +()-]{9,20}" data-error="Enter a phone number, for example 077 123 4567."')}</div>
      {field('email', 'Email', 'email', required=False, attrs='autocomplete="email" maxlength="150"')}
      <div class="field"><label for="contact_pref">Preferred contact</label><select id="contact_pref" name="contact_pref"><option>Phone call</option><option>WhatsApp</option><option>Email</option></select></div>
      <p class="field-hint">We use your details only to respond to this request. See our <a href="privacy.html">privacy policy</a>.</p>
      <div class="form-status" role="status" tabindex="-1"></div>
      <div class="step-actions"><button type="button" class="btn btn--ghost" data-prev>Back</button><button type="submit" class="btn">Send quote request</button></div>
    </div>
  </form>
  <aside class="aside-card">
    <h2>Prefer to talk?</h2><p class="text-steel">Call or WhatsApp and we will take the details over the phone.</p>
    <a class="btn btn--block" href="tel:{SITE['tel']}">{icon('phone')} {SITE['phone']}</a>
    <a class="btn btn--ghost btn--block mt-2" href="https://wa.me/{SITE['wa']}" rel="noopener" target="_blank">{icon('wa')} WhatsApp</a>
    <h3 class="mt-2">What happens next</h3>
    <ol class="text-steel"><li>We call to discuss your project.</li><li>We visit the site if needed.</li><li>You receive an itemised quotation.</li></ol>
  </aside>
</div></section>'''
    write('quote.html', head('quote.html', 'Request a quote', f'Request a construction quotation from {SITE["name"]}. Three quick steps; we reply within one working day.', [crumbs_schema(trail)])
          + header('quote.html') + body + footer())

def faq():
    trail = [('index.html', 'Home'), ('faq.html', 'FAQ')]
    items = ''.join(f'<details><summary>{q}</summary><div class="acc-body"><p>{a}</p></div></details>' for q, a in FAQS)
    body = page_hero('Frequently asked questions', 'Answers to the questions clients ask most before starting a project.', trail) + f'''
<section class="section"><div class="container layout-aside"><div class="accordion">{items}</div>
<aside class="aside-card"><h2>Still have a question?</h2><p class="text-steel">Call or message us and we will answer it directly.</p>
<a class="btn btn--block" href="contact.html">Contact us</a></aside></div></section>'''
    sch = [crumbs_schema(trail), {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQS if '[' not in a]}]
    write('faq.html', head('faq.html', 'FAQ', f'Common questions about building with {SITE["name"]}: quotations, timelines, payments and CIDA registration.', sch)
          + header('faq.html') + body + footer())

def legal(page, title, sections):
    trail = [('index.html', 'Home'), (page, title)]
    content = ''.join(f'<h2>{h}</h2>' + ''.join(f'<p>{p}</p>' for p in ps) for h, ps in sections)
    body = page_hero(title, f'Last updated: {ph("[Date]")}', trail) + f'<section class="section"><div class="container"><div class="prose">{content}<p class="text-steel">{ph("[Have this page reviewed by a legal adviser before publishing.]")}</p></div></div></section>'
    write(page, head(page, title, f'{title} for the {SITE["name"]} website.', [crumbs_schema(trail)]) + header(page) + body + footer())

def privacy():
    legal('privacy.html', 'Privacy policy', [
        ('Who we are', [f'{SITE["name"]}, {ADDRESS}, Sri Lanka. Contact: {SITE["phone"]}, {ph(SITE["email"])}.']),
        ('Information we collect', ['When you use our contact, quote or careers forms we collect the details you provide: your name, phone number, email address, project details and messages. Our hosting provider records standard technical logs such as IP address and browser type for security.']),
        ('How we use it', ['We use your information only to respond to your enquiry, prepare quotations, consider job applications and keep records of our communication. We do not sell or rent your personal information.']),
        ('Legal basis and your rights', ['We process personal data in line with the Personal Data Protection Act, No. 9 of 2022 of Sri Lanka. You may ask to access, correct or delete your personal data by contacting us.']),
        ('How long we keep it', [f'Enquiries are kept for {ph("[period]")} unless they become part of a contract, in which case they are kept as required for business and legal records.']),
        ('Third-party services', ['This website uses Google Fonts and an embedded Google Map, which may collect technical data under Google\'s own privacy policy. Links to WhatsApp open WhatsApp\'s service.']),
        ('Security', ['We use HTTPS, restricted access and other reasonable measures to protect your information.']),
    ])

def terms():
    legal('terms.html', 'Terms and conditions', [
        ('Use of this website', [f'This website provides general information about {SITE["name"]} and its services. By using it you agree to these terms.']),
        ('Information and quotations', ['Content on this website, including the floor-area planner, is for general information only and is not a quotation. Prices and scope are confirmed only in a written quotation and signed agreement.']),
        ('Intellectual property', [f'Text, graphics and design on this website belong to {SITE["name"]} or are used with permission. Do not copy them without written consent.']),
        ('Project images', ['Images of projects are shown with the permission of the owners where required.']),
        ('Liability', ['We take care to keep information accurate but do not guarantee that the website is error-free or always available.']),
        ('Governing law', ['These terms are governed by the laws of Sri Lanka.']),
    ])

def not_found():
    body = f'''<section class="section error-page"><div class="container"><p class="error-code" aria-hidden="true">404</p>
<h1 style="font-size:var(--fs-2xl)">This page is not on the plans</h1><p class="text-steel" style="margin-inline:auto">The link may be old or mistyped. Try one of these instead.</p>
<div class="hero-actions" style="justify-content:center"><a class="btn" href="index.html">Go to the homepage</a><a class="btn btn--ghost" href="projects.html">View projects</a><a class="btn btn--ghost" href="contact.html">Contact us</a></div></div></section>'''
    write('404.html', head('404.html', 'Page not found', 'The page you are looking for could not be found.', noindex=True) + header('404.html') + body + footer())

def extras():
    pages = ['index.html', 'about.html', 'team.html', 'services.html'] + [s['slug'] + '.html' for s in SERVICES] + \
            ['projects.html', 'project-detail.html', 'careers.html', 'blog.html'] + [p['slug'] + '.html' for p in POSTS] + \
            ['contact.html', 'quote.html', 'faq.html', 'privacy.html', 'terms.html']
    urls = ''.join(f'<url><loc>{SITE["url"]}/{"" if p == "index.html" else p}</loc><changefreq>monthly</changefreq><priority>{"1.0" if p == "index.html" else "0.7"}</priority></url>\n' for p in pages)
    write('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    write('robots.txt', f'User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE["url"]}/sitemap.xml\n')
    fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="6" fill="#0B1A2B"/>'
           '<rect x="6" y="27" width="28" height="6" fill="#E5E8E6"/><rect x="9" y="18" width="24" height="6" fill="#9FB2C4"/><rect x="12" y="9" width="20" height="6" fill="#F2A900"/></svg>')
    write('assets/img/favicon.svg', fav)
    write('site.webmanifest', json.dumps({'name': SITE['name'], 'short_name': 'R.B.N.', 'start_url': '/', 'display': 'standalone',
          'background_color': '#F6F7F6', 'theme_color': '#0B1A2B', 'icons': [{'src': 'assets/img/favicon.svg', 'sizes': 'any', 'type': 'image/svg+xml'}]}, indent=2))

if __name__ == '__main__':
    home(); about(); services()
    for s in SERVICES: service_detail(s)
    projects(); project_detail(); team(); careers(); blog()
    for p in POSTS: post(p)
    contact(); quote(); faq(); privacy(); terms(); not_found(); extras()
