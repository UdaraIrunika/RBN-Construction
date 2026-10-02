# R.B.N. Construction — Website (v2)

Custom HTML, CSS and vanilla JavaScript. No frameworks, no build step required, no third-party JS.
Built by **UIDD (Software Solutions)** — https://uiddevelopers.com

## Highlights

- **Custom 3D construction engine** (`assets/js/building3d.js`, ~300 lines, CSS 3D transforms only).
  A building assembles through 5 stages: Plan → Foundation → Structure → Envelope → Handover.
  Future stages are drawn as dashed blueprint outlines; crane and scaffolding appear and disappear with the stages.
  - Hero: plays the build once when seen, then drag / arrow keys to rotate, stage buttons to jump.
  - "How we work" section: the same model is driven by scrolling through the five steps.
  - Pauses when off-screen; respects `prefers-reduced-motion` (shows the finished building, no auto-rotation).
- **Lead generation:** 3-step quote wizard, floor-area planner that pre-fills the quote form, sticky mobile Call / WhatsApp / Quote bar, WhatsApp button, click-to-call everywhere.
- **Trust:** CIDA grade + registration fact sheet, certifications block, filterable portfolio, case-study project page, team page.
- **SEO:** unique titles/descriptions, canonical, Open Graph + Twitter, JSON-LD (GeneralContractor, LocalBusiness, Service, BreadcrumbList, Article, FAQPage), `sitemap.xml`, `robots.txt`, one `<h1>` per page, descriptive URLs.
- **Accessibility:** skip link, keyboard-operable 3D model, visible focus, labelled forms with inline errors, `aria-live` status messages, reduced motion.
- **Security:** PHP form handler with CSRF token, same-origin check, honeypot, minimum fill time, per-IP rate limiting, whitelist validation, header-injection-safe mail; `.htaccess` with CSP and security headers, HTTPS redirect, hidden-file blocking.

## Structure

```
index.html                 Home
about.html  team.html      Company
services.html              Service index
residential-construction.html, commercial-construction.html,
renovation-remodelling.html, civil-works.html,
project-management.html, maintenance-repairs.html   Service detail pages
projects.html              Filterable portfolio (?type=residential etc.)
project-detail.html        Case-study template (duplicate per project)
careers.html  blog.html  + 3 articles
contact.html  quote.html  faq.html  privacy.html  terms.html  404.html
assets/css/main.css        Design system + all styles (sectioned)
assets/js/main.js          Nav, filters, lightbox, forms, wizard, planner
assets/js/building3d.js    3D engine (loaded on home page only)
assets/img/                Blueprint drawings used as image slots, favicon, OG image
api/                       submit.php, token.php, bootstrap.php, config.php
tools/                     build.py (page generator), gen_svg.py (drawings) — optional
.htaccess  sitemap.xml  robots.txt  site.webmanifest
```

## Before going live — replace placeholders

Placeholders are shown with a striped amber highlight (`.placeholder`). **Never publish invented facts.**

| Item | Where |
|---|---|
| Domain `https://www.yourdomain.lk` | `tools/build.py` → `SITE['url']`, rebuild (or find & replace in all files incl. sitemap/robots) |
| `[EMAIL]`, `[Business hours]` | All pages (footer/contact) |
| `[CIDA grade]`, `[CIDA reg. no.]`, `[BR no.]`, `[Year]` | Home fact sheet, About, footer, FAQ |
| Company history, mission, vision | `about.html` |
| Certifications / insurance / awards (only real ones) | `about.html` |
| Projects: name, location, year, photos, case-study text | `projects.html`, `project-detail.html`, home |
| Team names, roles, photos | `team.html` |
| Testimonial (with written permission) | Home |
| Blog publish dates & author | blog pages |
| Vacancies | `careers.html` |
| Confirm services list | `tools/build.py` → `SERVICES` |
| Confirm WhatsApp number (currently same as phone) | `SITE['wa']` |
| Privacy retention period; legal review | `privacy.html`, `terms.html` |

### Images
Replace `assets/img/*.svg` drawings with real photos: export **WebP/AVIF** (1600px wide, < 250 KB) plus JPEG fallback, keep the `width`/`height` attributes and write real `alt` text.

## Editing pages
Two options:
1. **Edit HTML directly** — header/footer blocks are identical on every page.
2. **Regenerate** (recommended for site-wide changes): edit `tools/build.py` and run `python3 tools/build.py` (set `OUT` at the top to the project folder).

## Forms setup (LankaHost / cPanel, PHP 8+)
1. Set environment variables (or edit `api/config.php` defaults):
   `RBN_MAIL_TO`, `RBN_MAIL_FROM` (an address on your domain), optional `RBN_STORAGE_DIR` outside `public_html`.
2. Create the `RBN_MAIL_FROM` mailbox in cPanel and set SPF/DKIM so mail is not marked as spam.
3. For best delivery switch `mail()` to authenticated SMTP (PHPMailer) — credentials from env vars only.

Opening pages via `file://` works for everything except form submission (needs PHP on a server).

## Run locally
```
python3 -m http.server 5500      # static preview (forms will show a friendly error)
php -S localhost:8000            # full preview incl. forms
```

## Test checklist
- 320 / 375 / 768 / 1024 / 1280 / 1440 / 1920 px widths
- Keyboard only: Tab through nav, 3D model (arrow keys), stage buttons, quote wizard
- Quote wizard: required fields block "Continue"; planner → quote pre-fill
- Projects filter + `?type=civil` deep link; lightbox opens/closes with Esc
- Lighthouse (mobile) target ≥ 90 performance, 100 accessibility/SEO after real images
- Rich Results Test for JSON-LD; securityheaders.com after deploy
