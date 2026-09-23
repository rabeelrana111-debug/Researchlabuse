#!/usr/bin/env python3
"""
Generate the site's HTML pages from one set of shared parts.

The site is deployed as plain static files with no build step, which means the
header, navigation and footer would otherwise be copy-pasted into every page
and drift apart the first time one of them changed. This script keeps them in
one place: edit HEADER or FOOTER below, re-run, and every page updates.

Running it is optional — site/*.html is committed and deploys as-is. This is a
maintenance tool, not part of the deploy.

    python3 tools/build_pages.py
"""

import hashlib
import json
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

# --------------------------------------------------------------------------
# Page dates
# --------------------------------------------------------------------------
#
# Pages carry a published and a last-updated date, because a reference site
# that makes regulatory and scientific claims without saying when it last
# checked them is asking to be taken on faith.
#
# The dates are recorded, never guessed. content/page-dates.json holds, per
# page, the two dates plus a hash of the page body. On each build the body is
# re-hashed: if it differs, the page genuinely changed and the updated date
# moves to today; if it matches, the stored date stands. The hash covers the
# body only, so a stylesheet revision or a nav tweak does not falsely age
# every page on the site.
#
# First time a page is seen, its published date is taken from the git commit
# that introduced it, so existing pages keep their real history rather than
# all claiming to be published the day this was added.

DATES_FILE = ROOT / "content" / "page-dates.json"
TODAY = date.today().isoformat()


def _git_added(rel: str) -> str | None:
    """The date the built file first appeared in git, if it is in git."""
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%cs", "--reverse", "--", rel],
            cwd=ROOT, capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    lines = [l for l in out.stdout.split("\n") if l.strip()]
    return lines[0] if lines else None


class PageDates:
    def __init__(self) -> None:
        try:
            self.data = json.loads(DATES_FILE.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            self.data = {}
        self.dirty = False

    def for_page(self, route: str, rel: str, body: str) -> tuple[str, str]:
        digest = hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]
        entry = self.data.get(route)

        if entry is None:
            published = _git_added(rel) or TODAY
            entry = {"published": published, "updated": published, "hash": digest}
            self.data[route] = entry
            self.dirty = True
        elif entry.get("hash") != digest:
            entry["updated"] = TODAY
            entry["hash"] = digest
            self.dirty = True

        return entry["published"], entry["updated"]

    def save(self) -> None:
        if not self.dirty:
            return
        DATES_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATES_FILE.write_text(
            json.dumps(self.data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"updated {DATES_FILE.relative_to(ROOT)}")


DATES = PageDates()


def human_date(iso: str) -> str:
    y, m, d = (int(p) for p in iso.split("-"))
    months = ("January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December")
    return f"{months[m - 1]} {d}, {y}"


def byline(published: str, updated: str) -> str:
    """The trust-signal header: who wrote it and when it was last checked.

    There is deliberately no "scientifically reviewed by" line. Adding one
    without a named person who actually performed a review would be a false
    credential on health-adjacent content, which is worse than having none.
    """
    if updated != published:
        stamp = (f'<time datetime="{published}">{human_date(published)}</time>'
                 f'</span>\n\t\t\t\t<span class="byline__item">Last updated: '
                 f'<time datetime="{updated}">{human_date(updated)}</time>')
    else:
        stamp = f'<time datetime="{published}">{human_date(published)}</time>'
    return (f'\n\t\t\t<p class="byline">\n'
            f'\t\t\t\t<span class="byline__item">Written by: {SITE_NAME} '
            f'Editorial Team</span>\n'
            f'\t\t\t\t<span class="byline__item">Published: {stamp}</span>\n'
            f'\t\t\t</p>\n')


def asset(path: str) -> str:
    """Return an asset URL carrying a short hash of the file's contents.

    Stylesheets and scripts are cached hard by the browser, so an edit under
    the same URL stays invisible until the cache expires. Appending a hash of
    the contents changes the URL whenever the file changes — the new version
    is fetched immediately, and unchanged files still cache for a year.

    Regenerate the pages after editing CSS or JS, or the hash will be stale.
    """
    f = SITE / path.lstrip("/")
    if not f.exists():
        return path
    digest = hashlib.sha256(f.read_bytes()).hexdigest()[:10]
    return f"{path}?v={digest}"

SITE_NAME = "Research Lab USA"
EMAIL = "info@researchlabusa.com"

# Navigation. A third element, when present, is a dropdown of child pages.
NAV = [
    ("/", "Home", []),
    ("/sarms/", "SARMs", [
        ("/sarms/gw-501516/", "GW-501516 (Cardarine)"),
        ("/sarms/mk-2866/", "MK-2866 (Ostarine)"),
        ("/sarms/rad-140/", "RAD-140 (Testolone)"),
    ]),
    ("/peptides/", "Peptides", [
        ("/peptides/bpc-157/", "BPC-157"),
        ("/peptides/semaglutide/", "Semaglutide"),
        ("/peptides/tb-500/", "TB-500"),
    ]),
    ("/nootropics/", "Nootropics", [
        ("/nootropics/adrafinil/", "Adrafinil"),
        ("/nootropics/cyclazodone/", "Cyclazodone"),
        ("/nootropics/flmodafinil/", "Flmodafinil"),
        ("/nootropics/phenylpiracetam/", "Phenylpiracetam"),
    ]),
    ("/guides/", "Guides", []),
    ("/about/", "About", []),
    ("/contact/", "Contact", []),
]

# --- Icons ----------------------------------------------------------------

ICON_MAIL = ('<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18a1 1 0 0 '
             '1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm9 8L4.2 7.2v.9L12 '
             '14l7.8-5.9v-.9Z"/></svg>')

ICON_DNA = ('<svg class="eyebrow__ico" viewBox="0 0 24 24" aria-hidden="true">'
            '<path d="M7 2c0 4 10 4 10 8s-10 4-10 8" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round"/>'
            '<path d="M17 2c0 4-10 4-10 8s10 4 10 8" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round"/></svg>')

SOCIAL = {
    "X (Twitter)": "M18.9 2H22l-7.1 8.1L23.2 22h-6.5l-5.1-6.6L5.8 22H2.7l7.6-8.7L1.5 2H8l4.6 6.1L18.9 2Zm-1.1 18h1.7L7.3 3.7H5.5L17.8 20Z",
    "Facebook": "M13.5 22v-8h2.7l.4-3.1h-3.1V8.9c0-.9.25-1.5 1.55-1.5H16.7V4.6c-.29-.04-1.28-.13-2.44-.13-2.42 0-4.07 1.47-4.07 4.18v2.24H7.5V14h2.69v8h3.31Z",
    "LinkedIn": "M6.9 21H3.5V9h3.4v12ZM5.2 7.5a2 2 0 1 1 0-4 2 2 0 0 1 0 4ZM21 21h-3.4v-5.8c0-1.4 0-3.2-1.9-3.2s-2.2 1.5-2.2 3.1V21H10V9h3.3v1.6h.05a3.6 3.6 0 0 1 3.25-1.8c3.5 0 4.4 2.3 4.4 5.3V21Z",
    "Instagram": "M12 2.2c3.2 0 3.6 0 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.25.07 1.62.07 4.81 0 3.2 0 3.57-.07 4.81-.15 3.23-1.66 4.77-4.92 4.92-1.25.06-1.62.07-4.85.07-3.2 0-3.57 0-4.81-.07-3.27-.15-4.77-1.7-4.92-4.92C2.21 15.57 2.2 15.2 2.2 12c0-3.19 0-3.56.07-4.81.15-3.23 1.66-4.77 4.92-4.92C8.43 2.21 8.8 2.2 12 2.2Zm0 5.16a4.64 4.64 0 1 0 0 9.28 4.64 4.64 0 0 0 0-9.28Zm0 7.65a3.01 3.01 0 1 1 0-6.02 3.01 3.01 0 0 1 0 6.02Zm4.83-8.89a1.08 1.08 0 1 0 0 2.17 1.08 1.08 0 0 0 0-2.17Z",
}

LOGO_SVG = ('<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" fill="currentColor"/>'
            '<path d="M16 10h8v6l6 12a3 3 0 0 1-2.7 4.3H12.7A3 3 0 0 1 10 28l6-12v-6Z" fill="#fff"/>'
            '<circle cx="20" cy="26" r="2.5" fill="currentColor"/></svg>')


def social_links() -> str:
    out = []
    for label, path in SOCIAL.items():
        out.append(
            f'\t\t\t<a href="#" aria-label="{label}"><svg class="ico" viewBox="0 0 24 24" '
            f'aria-hidden="true"><path d="{path}"/></svg></a>'
        )
    return "\n".join(out)


def nav_links(current: str) -> str:
    """Render the main navigation, including dropdowns.

    Each dropdown is a real button with aria-expanded rather than a
    hover-only menu: hover alone is unusable on touch and unreachable by
    keyboard. CSS opens the panel on hover and on :focus-within so it still
    works with JavaScript disabled; script.js manages the button state.
    """
    out = []
    for href, label, children in NAV:
        # A parent is "current" when its own page or any child page is open.
        active = href == current or any(c == current for c, _ in children)
        cur = ' aria-current="page"' if active else ""

        if not children:
            out.append(f'\t\t\t<a href="{href}"{cur}>{label}</a>')
            continue

        menu_id = "menu-" + label.lower().replace(" ", "-")
        rows = []
        for c_href, c_label in children:
            # Built outside the f-string: expressions cannot contain
            # backslashes, and this needs escaped quotes.
            c_cur = ' aria-current="page"' if c_href == current else ''
            rows.append(
                f'\t\t\t\t\t<li><a href="{c_href}"{c_cur}>{c_label}</a></li>'
            )
        items = "\n".join(rows)
        out.append(
            f'\t\t\t<div class="navitem">\n'
            f'\t\t\t\t<a href="{href}"{cur}>{label}</a>\n'
            f'\t\t\t\t<button class="navitem__toggle" aria-expanded="false"\n'
            f'\t\t\t\t        aria-controls="{menu_id}">\n'
            f'\t\t\t\t\t<span class="sr-only">Show {label} pages</span>\n'
            f'\t\t\t\t\t<span class="navitem__chevron" aria-hidden="true"></span>\n'
            f'\t\t\t\t</button>\n'
            f'\t\t\t\t<ul class="submenu" id="{menu_id}">\n{items}\n\t\t\t\t</ul>\n'
            f'\t\t\t</div>'
        )
    return "\n".join(out)


def head(title: str, description: str, canonical: str | None,
         full_title: str | None = None, extra: str = "") -> str:
    # Pages get "Page | Site"; a page may override with its own full title
    # where a more descriptive one reads better in search results.
    if full_title is None:
        full_title = title if title == SITE_NAME else f"{title} | {SITE_NAME}"
    # A canonical of None means the page has no address of its own — the 404
    # body is served under whatever URL was missed, so pointing a canonical at
    # it would advertise a URL that does not exist. Keep it out of the index
    # instead.
    if canonical is None:
        index_meta = '<meta name="robots" content="noindex">'
    else:
        index_meta = f'<link rel="canonical" href="{BASE_URL}{canonical}">'
    return f"""<!doctype html>
<html lang="en">
<head>
\t<meta charset="utf-8">
\t<meta name="viewport" content="width=device-width, initial-scale=1">
\t<title>{full_title}</title>
\t<meta name="description" content="{description}">
\t{index_meta}
\t{extra}<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
\t<link rel="stylesheet" href="{asset('/styles.css')}">
</head>
<body>

<a class="skip" href="#main">Skip to content</a>

<!-- Utility bar -->
<div class="utilitybar">
\t<div class="wrap utilitybar__inner">
\t\t<ul class="utilitybar__contact">
\t\t\t<li>
\t\t\t\t{ICON_MAIL}
\t\t\t\t<a href="mailto:{EMAIL}">{EMAIL}</a>
\t\t\t</li>
\t\t</ul>
\t\t<nav class="utilitybar__social" aria-label="Social media">
{social_links()}
\t\t</nav>
\t</div>
</div>

<!-- Header -->
<header class="header">
\t<div class="wrap header__inner">
\t\t<a class="logo" href="/">
\t\t\t<span class="logo__mark" aria-hidden="true">
\t\t\t\t{LOGO_SVG}
\t\t\t</span>
\t\t\t<span class="logo__text">Research <strong>Lab USA</strong></span>
\t\t</a>

\t\t<button class="navtoggle" aria-expanded="false" aria-controls="mainnav">
\t\t\t<span class="navtoggle__bars" aria-hidden="true"></span>
\t\t\t<span class="sr-only">Menu</span>
\t\t</button>

\t\t<nav class="nav" id="mainnav" aria-label="Main">
{nav_links(canonical)}
\t\t</nav>

\t\t<div class="header__actions">
\t\t\t<a class="btn btn--ghost" href="/contact/">Inquire</a>
\t\t</div>
\t</div>
</header>

<main id="main">
"""


FOOTER = f"""</main>

<!-- Footer -->
<footer class="footer">
\t<div class="wrap">
\t\t<div class="footer__grid">
\t\t\t<div>
\t\t\t\t<p class="footer__title">{SITE_NAME}</p>
\t\t\t\t<p>Independent reference material for laboratory researchers.</p>
\t\t\t</div>
\t\t\t<div>
\t\t\t\t<p class="footer__title">Topics</p>
\t\t\t\t<ul class="footer__list">
\t\t\t\t\t<li><a href="/sarms/">SARMs</a></li>
\t\t\t\t\t<li><a href="/peptides/">Peptides</a></li>
\t\t\t\t\t<li><a href="/nootropics/">Nootropics</a></li>
\t\t\t\t\t<li><a href="/guides/">All guides</a></li>
\t\t\t\t</ul>
\t\t\t</div>
\t\t\t<div>
\t\t\t\t<p class="footer__title">Site</p>
\t\t\t\t<ul class="footer__list">
\t\t\t\t\t<li><a href="/about/">About</a></li>
\t\t\t\t\t<li><a href="/contact/">Contact</a></li>
\t\t\t\t\t<li><a href="/privacy/">Privacy Policy</a></li>
\t\t\t\t\t<li><a href="/terms/">Terms of Use</a></li>
\t\t\t\t</ul>
\t\t\t</div>
\t\t\t<div>
\t\t\t\t<p class="footer__title">Contact</p>
\t\t\t\t<ul class="footer__list">
\t\t\t\t\t<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
\t\t\t\t</ul>
\t\t\t</div>
\t\t</div>
\t\t<div class="footer__bottom">
\t\t\t<p>&copy; <span id="year">2026</span> {SITE_NAME}. All rights reserved.</p>
\t\t\t<p>For research use only. Not for human or veterinary consumption.</p>
\t\t</div>
\t</div>
</footer>

<a class="totop" href="#main" aria-label="Back to top"><span aria-hidden="true">Back to top</span></a>

<script src="{asset('/script.js')}" defer></script>
</body>
</html>
"""

# The research-use-only statement. Kept as one constant so the wording cannot
# drift between pages — inconsistent disclaimers are worse than none.
NOTICE = """\t<section class="section section--tight">
\t\t<div class="wrap">
\t\t\t<p class="notice">
\t\t\t\t<strong>For laboratory research use only.</strong> The research
\t\t\t\tmaterials described on this website are not intended for human or
\t\t\t\tveterinary use. Where we refer to an approved drug or active
\t\t\t\tingredient, we are describing the published regulatory status of that
\t\t\t\tspecific approved product &mdash; it does not mean a research material
\t\t\t\tsupplied by a third party is FDA-approved. Nothing here is medical
\t\t\t\tadvice or a recommendation about diagnosis, treatment, dosing or
\t\t\t\tpersonal use.
\t\t\t</p>
\t\t</div>
\t</section>
"""

# --------------------------------------------------------------------------
# Sourcing partner
# --------------------------------------------------------------------------
#
# A promotional placement for Avid Peptides, shown on the peptide pages only.
#
# The copy is straightforwardly promotional — it is an advert and reads like
# one. Two structural details carry the compliance load instead, and both
# should survive a rewrite of the words:
#
#   1. The "Partner" tag. An advertisement that is recognizable as an
#      advertisement needs no separate disclaimer, which is why banner ads do
#      not carry one — but strip the label and the same block becomes an
#      undisclosed endorsement, which is what the FTC's endorsement guidance
#      exists to stop. The tag is what keeps this an ad rather than a covert
#      recommendation, and it costs the promotion nothing.
#   2. rel="sponsored" on the link. That is the attribute Google specifies for
#      paid or promotional links; without it the link reads as an editorial
#      endorsement passing ranking signal, which is a link-scheme violation
#      that would count against this site's own rankings.
#
# Still no claims about purity, testing, shipping or price: nobody here has
# seen the partner's certificates, and unverifiable specifics are what the
# rest of the site teaches readers to discount.
PARTNER_NAME = "Avid Peptides"
PARTNER_URL = "https://avidpeptides.com"

PARTNER = f"""\t<section class="section section--tight">
\t\t<div class="wrap">
\t\t\t<aside class="partner" aria-labelledby="partner-heading">
\t\t\t\t<p class="partner__tag">Partner</p>
\t\t\t\t<div class="partner__body">
\t\t\t\t\t<h2 class="partner__title" id="partner-heading">Need research
\t\t\t\t\tpeptides? Visit {PARTNER_NAME}</h2>
\t\t\t\t\t<p>Research Lab USA publishes the reference material &mdash; our
\t\t\t\t\tpartner {PARTNER_NAME} supplies the peptides. If this guide covers
\t\t\t\t\tsomething you are ready to work with, head over and see what they
\t\t\t\t\thave available.</p>
\t\t\t\t</div>
\t\t\t\t<p class="partner__action">
\t\t\t\t\t<a class="btn btn--primary" href="{PARTNER_URL}"
\t\t\t\t\t   rel="sponsored noopener" target="_blank">Visit {PARTNER_NAME}
\t\t\t\t\t<span class="sr-only">(opens in a new tab)</span></a>
\t\t\t\t</p>
\t\t\t</aside>
\t\t</div>
\t</section>
"""


def with_partner(page_html: str) -> str:
    """Place the partner block immediately above the research-use notice."""
    return page_html.replace(NOTICE, PARTNER + NOTICE, 1)


def hero(eyebrow: str, title: str, lede: str) -> str:
    return f"""\t<section class="section">
\t\t<div class="wrap">
\t\t\t<div class="sectionhead">
\t\t\t\t<p class="eyebrow">{eyebrow}</p>
\t\t\t\t<h1>{title}</h1>
\t\t\t\t<p class="lede">{lede}</p>
\t\t\t</div>
\t\t</div>
\t</section>
"""


def topic_page(topic: str, eyebrow: str, title: str, lede: str,
               intro: str, covers: list, image: str, alt: str) -> str:
    """A subject overview page: SARMs, peptides, nootropics."""
    items = "\n".join(
        f"""\t\t\t\t<article class="card">
\t\t\t\t\t<h3>{h}</h3>
\t\t\t\t\t<p class="mb-0">{b}</p>
\t\t\t\t</article>""" for h, b in covers
    )
    return f"""{hero(eyebrow, title, lede)}
\t<section class="section section--tight">
\t\t<div class="wrap two-col">
\t\t\t<div class="measure">
{intro}
\t\t\t</div>
\t\t\t<div class="figure">
\t\t\t\t<img src="/assets/{image}" alt="{alt}" width="1600" height="1067"
\t\t\t\t     loading="lazy" decoding="async">
\t\t\t</div>
\t\t</div>
\t</section>

\t<section class="section section--alt">
\t\t<div class="wrap">
\t\t\t<div class="sectionhead sectionhead--center">
\t\t\t\t<p class="eyebrow eyebrow--center">{ICON_DNA} What we cover</p>
\t\t\t\t<h2>In our {topic} guides</h2>
\t\t\t</div>
\t\t\t<div class="cards">
{items}
\t\t\t</div>
\t\t</div>
\t</section>

{NOTICE}
\t<section class="cta">
\t\t<div class="wrap">
\t\t\t<div class="cta__panel">
\t\t\t\t<h2>Questions about a compound?</h2>
\t\t\t\t<p>If something in a guide is unclear, or you think we have it wrong,
\t\t\t\ttell us — corrections are published with a note explaining what changed.</p>
\t\t\t\t<div class="btnrow btnrow--center">
\t\t\t\t\t<a class="btn btn--primary" href="/contact/">Get in touch</a>
\t\t\t\t</div>
\t\t\t</div>
\t\t</div>
\t</section>
"""


BASE_URL = "https://researchlabusa.com"


def json_ld(canonical: str, title: str, description: str,
            published: str, updated: str, crumbs: list | None) -> str:
    """Structured data for one page.

    Organization and WebSite go on the home page only — repeating them on
    every page tells a crawler the same thing seventeen times. Interior pages
    get Article plus a BreadcrumbList matching the visible breadcrumb trail.
    """
    org = {"@type": "Organization", "name": SITE_NAME, "url": BASE_URL + "/"}
    graph: list = []

    if canonical == "/":
        graph.append({**org, "@id": BASE_URL + "/#organization",
                      "email": EMAIL})
        graph.append({"@type": "WebSite", "@id": BASE_URL + "/#website",
                      "url": BASE_URL + "/", "name": SITE_NAME,
                      "publisher": {"@id": BASE_URL + "/#organization"}})
    else:
        graph.append({
            "@type": "Article",
            "headline": title,
            "description": description,
            "mainEntityOfPage": BASE_URL + canonical,
            "author": org,
            "publisher": org,
            "datePublished": published,
            "dateModified": updated,
        })

    if crumbs:
        graph.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": n,
                 **({"item": BASE_URL + u} if u else {})}
                for i, (n, u) in enumerate(crumbs, start=1)
            ],
        })

    payload = json.dumps({"@context": "https://schema.org", "@graph": graph},
                         indent=None, separators=(",", ":"))
    return f'<script type="application/ld+json">{payload}</script>\n'


def rel_for(route: str, ext: str = "html") -> str:
    """The file a route is written to, relative to site/."""
    if route == "":
        return "index.html"
    if route == "404":
        return "404.html"
    return f"{route}/index.{ext}"


def write(route: str, title: str, description: str, body: str,
          full_title: str | None = None, prelude: str = "",
          ext: str = "html", crumbs: list | None = None,
          hash_body: str | None = None) -> None:
    """Write one page at a clean, extensionless URL.

    Routes map to directory indexes — "about" becomes site/about/index.html,
    served at /about. Apache resolves that through DirectoryIndex with no
    rewrite rules, so URLs stay clean without routing logic that could break
    the whole site if a pattern were wrong.

    Two routes are special: "" is the home page at site/index.html, and "404"
    stays a flat file because ErrorDocument points at a path, not a URL. The
    404 page also gets no canonical — it is served under the missing URL, not
    under one of its own.

    hash_body is the text the last-updated date is computed from. A page that
    prints its own dates must pass the version without them, or stamping the
    date would change the page, which would move the date, for ever.
    """
    rel = rel_for(route, ext)
    canonical = None if route == "404" else (
        "/" if route == "" else f"/{route}/")

    extra = ""
    if canonical is not None:
        published, updated = DATES.for_page(
            route, f"site/{rel}", hash_body if hash_body is not None else body)
        extra = json_ld(canonical, title, description, published, updated, crumbs)

    out = (prelude + head(title, description, canonical, full_title, extra)
           + body + FOOTER)
    dest = SITE / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8")
    print(f"wrote site/{rel}  -> {canonical or '(no canonical URL)'}")


# --------------------------------------------------------------------------
# Page content
# --------------------------------------------------------------------------

ABOUT = """\t<section class="section">
\t\t<div class="wrap">
\t\t\t<div class="sectionhead">
\t\t\t\t<p class="eyebrow">About us</p>
\t\t\t\t<h1>About Research Lab USA</h1>
\t\t\t\t<p class="lede">We publish reference material on research compounds
\t\t\t\tfor people who read the methods section first &mdash; researchers,
\t\t\t\tlaboratory staff, and anyone who would rather see the evidence than
\t\t\t\tbe told a conclusion.</p>
\t\t\t</div>
\t\t</div>
\t</section>

\t<section class="section section--tight">
\t\t<div class="wrap two-col">
\t\t\t<div class="measure prose">
\t\t\t\t<h2>Our purpose</h2>
\t\t\t\t<p>Sourcing information about research compounds is harder than it
\t\t\t\tshould be. Supplier pages read like advertising, forum threads
\t\t\t\tcontradict each other, and the primary literature is often behind a
\t\t\t\tpaywall or written for specialists. What sits in between is mostly
\t\t\t\twritten to rank in search results rather than to be useful.</p>
\t\t\t\t<p>We started publishing to fill that gap: material detailed enough
\t\t\t\tto act on, written plainly enough to read, and honest about the
\t\t\t\tconsiderable amount that remains unknown.</p>

\t\t\t\t<h2>What we are working towards</h2>
\t\t\t\t<p>A reference that researchers reach for first, and trust because it
\t\t\t\ttells them when the evidence is weak rather than only when it is
\t\t\t\tstrong. Every guide is built to answer three questions: what is this
\t\t\t\tmaterial, how should it be handled, and what has actually been
\t\t\t\tshown about it.</p>
\t\t\t\t<p>An absence of evidence is a finding in its own right, and it is
\t\t\t\tstated as clearly as a positive result.</p>

\t\t\t\t<h2>Who writes this</h2>
\t\t\t\t<p>[Describe your team here: who they are, their background, and the
\t\t\t\tdisciplines they work in &mdash; for example pharmacology, analytical
\t\t\t\tchemistry, molecular biology or laboratory practice. Name real people
\t\t\t\tand real qualifications where you can.]</p>
\t\t\t\t<p class="notice">
\t\t\t\t\t<strong>Fill this section in before launch.</strong> Claims about
\t\t\t\t\texpertise are the first thing a careful reader checks, and an
\t\t\t\t\tunsupported one costs more credibility than saying nothing. If
\t\t\t\t\tthere is no team yet, describe how the material is researched
\t\t\t\t\tinstead &mdash; that is verifiable, and it answers the same
\t\t\t\t\tquestion.
\t\t\t\t</p>

\t\t\t\t<h2>How we write</h2>
\t\t\t\t<p>Claims are tied to the study behind them, so you can read the
\t\t\t\toriginal rather than take our word for it. Where findings come from a
\t\t\t\tsingle research group, or have never been independently replicated,
\t\t\t\twe say so &mdash; a citation count is not the same as a body of
\t\t\t\tevidence.</p>
\t\t\t\t<p>We describe materials, not outcomes in people. Chemical identity,
\t\t\t\tpurity, physical form, solubility and storage are all fair game.
\t\t\t\tWhat a compound does in a human body is not something we assert,
\t\t\t\tbecause for almost everything cataloged here nobody reliably
\t\t\t\tknows.</p>

\t\t\t\t<h2>Corrections</h2>
\t\t\t\t<p>When something turns out to be wrong, the page is updated with a
\t\t\t\tdated note describing what changed and why. Pages are not quietly
\t\t\t\tedited: if you relied on an earlier version, you should be able to
\t\t\t\tsee that it changed.</p>
\t\t\t</div>
\t\t\t<div class="figure">
\t\t\t\t<img src="/assets/lab-pipetting.jpg"
\t\t\t\t     alt="Researcher in gloves transferring a sample into a tube rack"
\t\t\t\t     width="1600" height="1067" loading="lazy" decoding="async">
\t\t\t</div>
\t\t</div>
\t</section>

\t<section class="section section--alt">
\t\t<div class="wrap">
\t\t\t<div class="sectionhead sectionhead--center">
\t\t\t\t<p class="eyebrow eyebrow--center">What you will find here</p>
\t\t\t\t<h2>Four things we try to get right</h2>
\t\t\t</div>
\t\t\t<div class="cards">
\t\t\t\t<article class="card">
\t\t\t\t\t<h3>Sourced material</h3>
\t\t\t\t\t<p class="mb-0">Guides built from published work, with each claim
\t\t\t\t\tlinked to the study behind it so you can check the original.</p>
\t\t\t\t</article>
\t\t\t\t<article class="card">
\t\t\t\t\t<h3>Handling detail</h3>
\t\t\t\t\t<p class="mb-0">Storage, solubility and preparation written out in
\t\t\t\t\tfull, including the steps that get left off because they seem
\t\t\t\t\tobvious to whoever wrote them down.</p>
\t\t\t\t</article>
\t\t\t\t<article class="card">
\t\t\t\t\t<h3>Stated uncertainty</h3>
\t\t\t\t\t<p class="mb-0">Where the record is thin, contested, or rests on one
\t\t\t\t\tgroup's work, that appears at the top of the page rather than
\t\t\t\t\tburied at the bottom.</p>
\t\t\t\t</article>
\t\t\t\t<article class="card">
\t\t\t\t\t<h3>Verification first</h3>
\t\t\t\t\t<p class="mb-0">How to read a certificate of analysis and what
\t\t\t\t\tbatch traceability should look like &mdash; because mislabelling is
\t\t\t\t\twell documented across this whole product category.</p>
\t\t\t\t</article>
\t\t\t</div>
\t\t</div>
\t</section>

\t<section class="section section--tight">
\t\t<div class="wrap">\n\t\t\t<div class="measure prose">
\t\t\t<h2>Why read us rather than a supplier page</h2>
\t\t\t<p>A supplier has an interest in the answer. We would rather tell you
\t\t\tthat a compound is poorly characterized, that its development was
\t\t\tdiscontinued, or that the enthusiasm around it outruns the published
\t\t\twork &mdash; all of which appear on pages here.</p>
\t\t\t<p>That is the whole proposition. A reference that only ever sounds
\t\t\tpositive is not a reference.</p>

\t\t\t<h2>Get in touch</h2>
\t\t\t<p>Corrections, questions and suggestions for what to cover next are all
\t\t\twelcome, and corrections get published. Reach us at
\t\t\t<a href="mailto:""" + EMAIL + """">""" + EMAIL + """</a> or through the
\t\t\t<a href="/contact/">contact page</a>.</p>
\t\t\t</div>
\t\t</div>
\t</section>

""" + NOTICE + """
\t<section class="cta">
\t\t<div class="wrap">
\t\t\t<div class="cta__panel">
\t\t\t\t<h2>Found something wrong?</h2>
\t\t\t\t<p>Tell us and it gets fixed, with a note saying what changed.</p>
\t\t\t\t<div class="btnrow btnrow--center">
\t\t\t\t\t<a class="btn btn--primary" href="/contact/">Contact us</a>
\t\t\t\t\t<a class="btn btn--light" href="/guides/">Browse the guides</a>
\t\t\t\t</div>
\t\t\t</div>
\t\t</div>
\t</section>
"""

GUIDE_CARDS = [
    ("GW-501516", "ampoules-microscope.jpg",
     "Amber and clear glass ampoules on a bench in front of a microscope",
     "A PPAR&delta; receptor agonist studied in metabolic and endurance research. "
     "Covers chemical identity, handling and storage, and what the published animal "
     "literature does and does not establish.", True),
    ("TB-500", "lab-pipetting.jpg",
     "Researcher in gloves transferring a sample into a tube rack",
     "A synthetic peptide fragment related to thymosin beta-4. Sets out its sequence, "
     "reconstitution and cold-chain requirements, and summarizes the preclinical work "
     "published to date.", False),
    ("Cyclazodone", "capsule-selection.jpg",
     "Gloved hands using tweezers to place a capsule into a sample pot",
     "A substituted aminorex derivative from the nootropic research literature. Covers "
     "its structure, stability, and the notable gaps in the published record &mdash; "
     "which are considerable.", False),
]


def guide_cards() -> str:
    out = []
    for name, img, alt, body, accent in GUIDE_CARDS:
        head_cls = ' pcard__head--accent' if accent else ''
        out.append(f"""\t\t\t\t<article class="pcard">
\t\t\t\t\t<div class="pcard__head{head_cls}">
\t\t\t\t\t\t<h3 class="pcard__title">{name}</h3>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="pcard__media">
\t\t\t\t\t\t<img src="/assets/{img}" alt="{alt}" width="1600" height="1067"
\t\t\t\t\t\t     loading="lazy" decoding="async">
\t\t\t\t\t</div>
\t\t\t\t\t<div class="pcard__body">
\t\t\t\t\t\t<p class="pcard__meta">Reference guide</p>
\t\t\t\t\t\t<p>{body}</p>
\t\t\t\t\t</div>
\t\t\t\t</article>""")
    return "\n".join(out)


GUIDES = """\t<section class="section">
\t\t<div class="wrap">
\t\t\t<div class="sectionhead">
\t\t\t\t<p class="eyebrow">Guides</p>
\t\t\t\t<h1>Reference guides</h1>
\t\t\t\t<p class="lede">Each guide covers chemical identity, handling and storage,
\t\t\t\tand an honest account of what the published literature supports.</p>
\t\t\t</div>
\t\t\t<div class="cards">
""" + guide_cards() + """
\t\t\t</div>
\t\t\t<p class="mt-8 measure">More guides are in preparation. If there is a
\t\t\tcompound you would like covered,
\t\t\t<a href="/contact/">tell us</a> &mdash; requests genuinely shape what
\t\t\twe write next.</p>
\t\t</div>
\t</section>

""" + NOTICE

SARMS = topic_page(
    topic="SARMs",
    eyebrow="Topic",
    title="Selective androgen receptor modulators",
    lede="Reference material on SARMs as laboratory research compounds — identity, "
         "handling, and what the literature actually shows.",
    intro="""\t\t\t\t<h2>What this section covers</h2>
\t\t\t\t<p>SARMs are a class of compounds studied for their selective activity at
\t\t\t\tthe androgen receptor. Our guides describe them as materials: structure,
\t\t\t\tmolecular weight, solubility, stability and storage.</p>
\t\t\t\t<p>Where we discuss research findings, we describe what was measured, in
\t\t\t\twhat model, and what the authors concluded &mdash; not what the result
\t\t\t\tmight mean for a person. Most of this literature is preclinical, and
\t\t\t\ttreating it otherwise misrepresents it.</p>
\t\t\t\t<p>None of these compounds is approved for human or veterinary use in any
\t\t\t\tjurisdiction we are aware of. Several are prohibited in competitive sport.
\t\t\t\tThat context belongs in any honest write-up, so it appears in ours.</p>""",
    covers=[
        ("Chemical identity", "CAS number, molecular formula and weight, and the "
         "naming variants a compound appears under in the literature."),
        ("Handling and storage", "Physical form, solubility, and the storage "
         "conditions needed to keep material at its stated specification."),
        ("State of the evidence", "What has been published, in what models, and "
         "which findings have and have not been independently replicated."),
        ("Verifying a supply", "How to read a certificate of analysis, and what "
         "batch-level traceability should look like before you order."),
    ],
    image="ampoules-bench.jpg",
    alt="Amber glass ampoules on a laboratory bench beside a microscope",
)

PEPTIDES = topic_page(
    topic="peptide",
    eyebrow="Topic",
    title="Research peptides",
    lede="Sequences, reconstitution, cold-chain handling and stability — the "
         "practical details that determine whether a result is reproducible.",
    intro="""\t\t\t\t<h2>What this section covers</h2>
\t\t\t\t<p>Peptides are unforgiving materials to work with. Reconstitution
\t\t\t\tsolvent, temperature history and freeze-thaw cycles all affect what is
\t\t\t\tactually in the vial by the time it reaches an assay, and those details
\t\t\t\tare routinely left out of published protocols.</p>
\t\t\t\t<p>Our guides give the sequence, molecular weight and purity method for
\t\t\t\teach peptide, then set out reconstitution and storage in full &mdash;
\t\t\t\tincluding the steps that seem obvious to whoever wrote them down.</p>
\t\t\t\t<p>Lyophilized material and material in solution behave differently, and
\t\t\t\twe treat them separately rather than collapsing both into one
\t\t\t\tinstruction.</p>""",
    covers=[
        ("Sequence and identity", "Amino acid sequence, molecular weight, and the "
         "analytical method used to establish purity."),
        ("Reconstitution", "Appropriate solvents, concentrations, and the handling "
         "steps that affect stability after reconstitution."),
        ("Cold chain", "Storage temperatures for lyophilized and reconstituted "
         "material, and what freeze-thaw cycling costs you."),
        ("Preclinical literature", "What has been studied, in what model, and how "
         "far the findings have been replicated."),
    ],
    image="lab-pipetting.jpg",
    alt="Researcher in gloves transferring a sample into a tube rack",
)

NOOTROPICS = topic_page(
    topic="nootropic",
    eyebrow="Topic",
    title="Nootropic research compounds",
    lede="A subject area with more marketing than evidence — our guides are "
         "explicit about which is which.",
    intro="""\t\t\t\t<h2>What this section covers</h2>
\t\t\t\t<p>The nootropic literature is uneven. Some compounds have decades of
\t\t\t\tpublished pharmacology behind them; others have a handful of papers, a
\t\t\t\tgreat deal of forum speculation, and very little in between.</p>
\t\t\t\t<p>Our guides separate those cases plainly. Where a compound is
\t\t\t\tpoorly characterized, that is stated at the top of the page rather than
\t\t\t\tburied &mdash; an absence of evidence is itself the most useful thing we
\t\t\t\tcan tell you.</p>
\t\t\t\t<p>We cover structure, stability and analytical identity, and summarize
\t\t\t\twhat has been published without extrapolating it into claims about
\t\t\t\teffects in people.</p>""",
    covers=[
        ("Structure and class", "Chemical structure, the family a compound belongs "
         "to, and the closely related materials it is confused with."),
        ("Analytical identity", "How the compound is identified and what purity "
         "testing on it typically reports."),
        ("Stability", "Known degradation behavior and the storage conditions that "
         "affect it."),
        ("Evidence, honestly", "What has actually been published, and an explicit "
         "note where the record is thin."),
    ],
    image="capsule-selection.jpg",
    alt="Gloved hands using tweezers to place a capsule into a sample pot",
)


NOT_FOUND = """\t<section class="section">
\t\t<div class="wrap">
\t\t\t<div class="sectionhead">
\t\t\t\t<p class="eyebrow">Error 404</p>
\t\t\t\t<h1>We couldn&rsquo;t find that page</h1>
\t\t\t\t<p class="lede">The link may be out of date, or the page may have
\t\t\t\tmoved. The guides below are a good place to pick up.</p>
\t\t\t\t<div class="btnrow mt-8">
\t\t\t\t\t<a class="btn btn--primary" href="/guides/">Browse the guides</a>
\t\t\t\t\t<a class="btn btn--secondary" href="/">Go to the homepage</a>
\t\t\t\t</div>
\t\t\t</div>
\t\t</div>
\t</section>
"""

# --------------------------------------------------------------------------
# Legal pages
# --------------------------------------------------------------------------
#
# These are an honest description of what this site actually does, written so
# a reader can check each statement against the site itself: it has no
# accounts, no shopping cart, no analytics and no advertising network, and
# the only personal data it receives is what someone types into the contact
# form. That makes the policy short, and short is a feature — a policy that
# claims machinery the site does not have is worse than none.
#
# They still need a lawyer's eye before they can be relied on. State privacy
# statutes (notably the CCPA/CPRA in California) attach obligations to
# thresholds only the operator can assess, and nothing here can determine
# whether this business crosses them.

LEGAL_REVIEW = """\t<section class="section section--tight">
\t\t<div class="wrap">
\t\t\t<p class="notice notice--info">
\t\t\t\t<strong>Awaiting legal review.</strong> This page describes our
\t\t\t\tcurrent practice accurately, but it has not yet been reviewed by a
\t\t\t\tlawyer. If you need a binding answer about how your information is
\t\t\t\thandled before you send it, write to
\t\t\t\t<a href="mailto:""" + EMAIL + '">' + EMAIL + """</a> and ask.
\t\t\t</p>
\t\t</div>
\t</section>
"""

PRIVACY = hero(
    "Legal", "Privacy Policy",
    "What we collect, why, and how long we keep it. Short, because this site "
    "collects very little."
) + LEGAL_REVIEW + """
\t<section class="section section--tight">
\t\t<div class="wrap">
\t\t\t<div class="measure prose">
\t\t\t\t<h2>What we collect</h2>
\t\t\t\t<p>Only what you type into our contact form: your name, your email
\t\t\t\taddress, a subject line and your message. Every field is one you fill
\t\t\t\tin yourself &mdash; we do not collect anything about you in the
\t\t\t\tbackground.</p>
\t\t\t\t<p>Like every web server, ours records requests it receives,
\t\t\t\tincluding IP addresses, in standard server logs kept by our hosting
\t\t\t\tprovider. Those logs exist for security and troubleshooting. We do
\t\t\t\tnot use them to build a profile of you.</p>

\t\t\t\t<h2>What we do not do</h2>
\t\t\t\t<ul>
\t\t\t\t\t<li>We set no cookies and run no analytics or tracking scripts.
\t\t\t\t\tYou can confirm this: open your browser&rsquo;s developer tools on
\t\t\t\t\tany page of this site and look at the Application and Network
\t\t\t\t\ttabs.</li>
\t\t\t\t\t<li>We have no user accounts and no shopping cart, so there is no
\t\t\t\t\tpassword or payment information to lose.</li>
\t\t\t\t\t<li>We do not sell your information, and we do not share it with
\t\t\t\t\tanyone for their own marketing.</li>
\t\t\t\t</ul>

\t\t\t\t<h2>Why we use it</h2>
\t\t\t\t<p>To read your message and reply to it. That is the only purpose.
\t\t\t\tWe will not add you to a mailing list because you asked a
\t\t\t\tquestion.</p>

\t\t\t\t<h2>Who else sees it</h2>
\t\t\t\t<p>Our web host processes the form submission and carries the
\t\t\t\tresulting email, and our email provider stores it. They act as
\t\t\t\tservice providers on our behalf and are not free to use your message
\t\t\t\tfor their own purposes.</p>
\t\t\t\t<p>Pages in our peptides section link to
\t\t\t\t<a href=\"""" + PARTNER_URL + """\" rel="sponsored noopener" target="_blank">""" + PARTNER_NAME + """<span class="sr-only"> (opens in a new tab)</span></a>,
\t\t\t\tour peptide supply partner. Following that link takes you to their
\t\t\t\twebsite, which has its own privacy policy and is not covered by this
\t\t\t\tone. We do not pass them your contact details.</p>

\t\t\t\t<h2>How long we keep it</h2>
\t\t\t\t<p>Contact-form emails are kept while a conversation is open and for
\t\t\t\tup to two years afterwards, so we can pick up an earlier thread.
\t\t\t\tAfter that they are deleted. Ask us to delete yours sooner and we
\t\t\t\twill.</p>

\t\t\t\t<h2>Your choices</h2>
\t\t\t\t<p>Write to <a href="mailto:""" + EMAIL + '">' + EMAIL + """</a> to
\t\t\t\task what we hold about you, to have it corrected, or to have it
\t\t\t\tdeleted. We will respond within 30 days. Depending on where you live
\t\t\t\tyou may have further statutory rights; tell us what you need and we
\t\t\t\twill work out whether it applies.</p>

\t\t\t\t<h2>Children</h2>
\t\t\t\t<p>This site publishes laboratory reference material and is not
\t\t\t\tdirected to children. We do not knowingly collect information from
\t\t\t\tanyone under 16.</p>

\t\t\t\t<h2>Changes</h2>
\t\t\t\t<p>If this policy changes materially, the revised version will
\t\t\t\tappear here with a new date at the top of the page.</p>

\t\t\t\t<h2>Contact</h2>
\t\t\t\t<p>Questions about this policy go to
\t\t\t\t<a href="mailto:""" + EMAIL + '">' + EMAIL + """</a>.</p>
\t\t\t</div>
\t\t</div>
\t</section>
"""

TERMS = hero(
    "Legal", "Terms of Use",
    "The terms you accept by using this website, and the limits of what the "
    "material here is for."
) + LEGAL_REVIEW + """
\t<section class="section section--tight">
\t\t<div class="wrap">
\t\t\t<div class="measure prose">
\t\t\t\t<h2>What this site is</h2>
\t\t\t\t<p>""" + SITE_NAME + """ publishes reference material about research
\t\t\t\tcompounds for people working in a laboratory setting. We do not sell
\t\t\t\tcompounds, supply them, or broker their sale.</p>

\t\t\t\t<h2>Research use only</h2>
\t\t\t\t<p>Everything here describes materials intended for laboratory
\t\t\t\tresearch. Nothing on this site is medical advice, and nothing here
\t\t\t\tshould be read as a suggestion that any compound is safe or effective
\t\t\t\tfor use in people or animals. You are responsible for complying with
\t\t\t\tthe laws and institutional rules that apply where you are.</p>

\t\t\t\t<h2>Accuracy, and its limits</h2>
\t\t\t\t<p>We write carefully and cite our sources, and we publish
\t\t\t\tcorrections when we get something wrong. We cannot warrant that every
\t\t\t\tstatement is complete or current: the literature moves, and
\t\t\t\tregulatory status changes.</p>
\t\t\t\t<p>Identity data on our compound pages is reproduced from public
\t\t\t\tchemical databases, which we link so you can check the record
\t\t\t\tyourself. Properties that belong to a batch rather than a compound
\t\t\t\t&mdash; physical form, purity, storage &mdash; must come from the
\t\t\t\tcertificate of analysis for the material you hold. Do not substitute
\t\t\t\tanything on this site for that document.</p>
\t\t\t\t<p>Found an error? <a href="/contact/">Tell us</a> and it gets fixed,
\t\t\t\twith a note saying what changed.</p>

\t\t\t\t<h2>Links to other sites</h2>
\t\t\t\t<p>We link to external sources, and our peptides pages carry a
\t\t\t\tpromotional placement for our partner """ + PARTNER_NAME + """,
\t\t\t\tlabelled as a partner wherever it appears. We do not control those
\t\t\t\twebsites and are not responsible for their content, their products or
\t\t\t\ttheir practices. Any dealing you have with them is between you and
\t\t\t\tthem.</p>

\t\t\t\t<h2>Using our material</h2>
\t\t\t\t<p>The text and images on this site belong to us. You are welcome to
\t\t\t\tquote a passage or cite a page with attribution and a link.
\t\t\t\tRepublishing a guide wholesale, or using our material to train a
\t\t\t\tcommercial model, needs our written permission first &mdash;
\t\t\t\t<a href="/contact/">ask</a>, and we will usually say yes.</p>

\t\t\t\t<h2>Acceptable use</h2>
\t\t\t\t<p>Do not attempt to break, overload or gain unauthorized access to
\t\t\t\tthis site, and do not use the contact form to send unsolicited
\t\t\t\tcommercial messages.</p>

\t\t\t\t<h2>Liability</h2>
\t\t\t\t<p>This site is provided as it is, without warranties of any kind.
\t\t\t\tTo the fullest extent the law allows, we are not liable for loss
\t\t\t\tarising from your use of it or from reliance on anything published
\t\t\t\there. Nothing in these terms limits liability that cannot lawfully be
\t\t\t\tlimited.</p>

\t\t\t\t<h2>Changes</h2>
\t\t\t\t<p>We may revise these terms. The current version is always the one
\t\t\t\ton this page, with its last-updated date shown at the top.</p>

\t\t\t\t<h2>Contact</h2>
\t\t\t\t<p>Questions about these terms go to
\t\t\t\t<a href="mailto:""" + EMAIL + '">' + EMAIL + """</a>.</p>
\t\t\t</div>
\t\t</div>
\t</section>
"""


def main() -> None:
    home_body = (ROOT / "content" / "home.html").read_text(encoding="utf-8")

    write("", SITE_NAME,
          "Independent guides, methods notes and reference data on research compounds, "
          "peptides and nootropics. Written for laboratory researchers. "
          "For research use only.",
          home_body,
          full_title="Research Lab USA \u2014 Research Compound Guides "
                     "&amp; Laboratory Resources")

    write("about", "About",
          "Who we are, how we write, and how we handle corrections. Independent "
          "reference material for laboratory researchers.", ABOUT,
          crumbs=[("Home", "/"), ("About", None)])

    # Served as .php so the page can handle its own form submission.
    write("contact", "Contact",
          "Questions, corrections and suggestions for what to cover next. "
          f"Reach us at {EMAIL}.", CONTACT, prelude=CONTACT_PHP,
          ext="php", crumbs=[("Home", "/"), ("Contact", None)])

    write("privacy", "Privacy Policy",
          "What this site collects, why, who else sees it and how long it is "
          "kept. No cookies, no analytics, no tracking.", PRIVACY,
          crumbs=[("Home", "/"), ("Privacy Policy", None)])

    write("terms", "Terms of Use",
          "The terms you accept by using this website, and the limits of what "
          "the reference material here is for.", TERMS,
          crumbs=[("Home", "/"), ("Terms of Use", None)])

    write("guides", "Guides",
          "Reference guides covering chemical identity, handling, storage and the "
          "state of the published literature.", GUIDES,
          crumbs=[("Home", "/"), ("Guides", None)])

    write("sarms", "SARMs",
          "Reference material on selective androgen receptor modulators as laboratory "
          "research compounds. For research use only.",
          with_compounds(SARMS, "/sarms/"),
          crumbs=[("Home", "/"), ("SARMs", None)])

    write("peptides", "Peptides",
          "Research peptide reference material: sequences, reconstitution, cold-chain "
          "handling and stability. For research use only.",
          with_partner(with_compounds(PEPTIDES, "/peptides/")),
          crumbs=[("Home", "/"), ("Peptides", None)])

    write("nootropics", "Nootropics",
          "Reference material on nootropic research compounds, with an explicit account "
          "of where the published evidence is thin.",
          with_compounds(NOOTROPICS, "/nootropics/"),
          crumbs=[("Home", "/"), ("Nootropics", None)])

    write("404", "Page not found",
          "The page you were looking for does not exist.", NOT_FOUND)

    build_compound_pages()
    build_robots_and_sitemap()
    DATES.save()


def build_robots_and_sitemap() -> None:
    """Write robots.txt and sitemap.xml from the pages actually generated.

    Both are derived from the date manifest rather than typed out, so a page
    added later cannot be missing from the sitemap — the commonest way a
    sitemap goes stale is someone forgetting to update it by hand.

    Nothing is disallowed. There is no admin area, no search-results page and
    no faceted navigation here, so a Disallow rule would only risk hiding
    something legitimate. The 404 page is excluded because it carries
    noindex and has no URL of its own.
    """
    routes = sorted(r for r in DATES.data if r != "404")

    entries = []
    for route in routes:
        loc = BASE_URL + ("/" if route == "" else f"/{route}/")
        lastmod = DATES.data[route]["updated"]
        # The home page and topic hubs change as guides are added; individual
        # guides change when their content does.
        priority = "1.0" if route == "" else (
            "0.8" if "/" not in route else "0.6")
        entries.append(
            f"\t<url>\n\t\t<loc>{loc}</loc>\n"
            f"\t\t<lastmod>{lastmod}</lastmod>\n"
            f"\t\t<priority>{priority}</priority>\n\t</url>"
        )

    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "\n".join(entries) + "\n</urlset>\n")
    (SITE / "sitemap.xml").write_text(sitemap, encoding="utf-8")

    robots = (
        "# https://researchlabusa.com\n"
        "#\n"
        "# Everything here is public reference material meant to be found.\n"
        "# There is no admin area or private section to keep crawlers out of.\n"
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {BASE_URL}/sitemap.xml\n"
    )
    (SITE / "robots.txt").write_text(robots, encoding="utf-8")
    print(f"wrote site/robots.txt and site/sitemap.xml ({len(routes)} URLs)")



# --------------------------------------------------------------------------
# Individual compound pages
# --------------------------------------------------------------------------
#
# Identity data comes from the September 2026 QA audit, which sourced each
# value to PubChem and the FDA Global Substance Registration System. Every
# formula/weight pair was recomputed from the formula before publishing and
# agrees with the stated weight to within 0.05 g/mol, so none is a
# transcription error. The source link is published beside the table so a
# reader can check the record rather than take the site's word for it.
#
# Compounds without audited identity data get NO table at all. A published
# "[CAS]" is worse than a missing row: it looks like data, it indexes like
# data, and it invites someone to go looking for the wrong material.
#
# Physical form, purity and storage are deliberately absent from every page.
# Those three are properties of a batch, not of a compound, and this site
# represents no batch — publishing them here would imply a verification that
# has not happened. They belong on the certificate of analysis.

IDENTITY = {
    "sarms/gw-501516": dict(
        rows=[("CAS number", "317318-70-0"),
              ("Molecular formula", "C<sub>21</sub>H<sub>18</sub>F<sub>3</sub>NO<sub>3</sub>S<sub>2</sub>"),
              ("Molecular weight", "453.5 g/mol"),
              ("PubChem CID", "9803963")],
        source_url="https://pubchem.ncbi.nlm.nih.gov/compound/gw-501516",
        source_label="PubChem CID 9803963",
    ),
    "peptides/bpc-157": dict(
        rows=[("Identity", "BPC-157 free peptide"),
              ("Sequence", "Gly-Glu-Pro-Pro-Pro-Gly-Lys-Pro-Ala-Asp-Asp-Ala-Gly-Leu-Val"),
              ("CAS number", "137525-51-0"),
              ("Molecular formula", "C<sub>62</sub>H<sub>98</sub>N<sub>16</sub>O<sub>22</sub>"),
              ("Molecular weight", "1419.54 g/mol"),
              ("PubChem CID", "9941957")],
        source_url="https://pubchem.ncbi.nlm.nih.gov/compound/Bpc-157",
        source_label="PubChem CID 9941957",
        caution="These values describe the <strong>free peptide</strong>. Acetate "
                "and trifluoroacetate salts of BPC-157 have different formulas and "
                "molecular weights, so check which form your batch documentation "
                "describes before comparing.",
    ),
    "peptides/semaglutide": dict(
        rows=[("Identity", "Semaglutide free base"),
              ("CAS number", "910463-68-2"),
              ("Molecular formula", "C<sub>187</sub>H<sub>291</sub>N<sub>45</sub>O<sub>59</sub>"),
              ("Molecular weight", "4113.6 g/mol"),
              ("PubChem CID", "56843331")],
        source_url="https://pubchem.ncbi.nlm.nih.gov/compound/Semaglutide",
        source_label="PubChem CID 56843331",
    ),
    "peptides/tb-500": dict(
        rows=[("CAS number", "885340-08-9"),
              ("Molecular formula", "C<sub>38</sub>H<sub>68</sub>N<sub>10</sub>O<sub>14</sub>"),
              ("Molecular weight", "889.0 g/mol"),
              ("PubChem CID", "62707662")],
        source_url="https://pubchem.ncbi.nlm.nih.gov/compound/Unii-qhk6Z47gtg",
        source_label="PubChem CID 62707662",
        caution="TB-500 is <strong>not</strong> interchangeable with full-length "
                "thymosin beta-4, which PubChem lists separately at "
                "C<sub>212</sub>H<sub>350</sub>N<sub>56</sub>O<sub>78</sub>S and "
                "about 4963 g/mol &mdash; roughly five and a half times the mass. "
                "Confirm the sequence and chemical form on your batch "
                "documentation before relying on any figure here.",
    ),
    "nootropics/cyclazodone": dict(
        rows=[("CAS number", "14461-91-7"),
              ("Molecular formula", "C<sub>12</sub>H<sub>12</sub>N<sub>2</sub>O<sub>2</sub>"),
              ("Molecular weight", "216.24 g/mol"),
              ("PubChem CID", "135438121")],
        source_url="https://pubchem.ncbi.nlm.nih.gov/compound/Cyclazodone",
        source_label="PubChem CID 135438121",
    ),
    "nootropics/flmodafinil": dict(
        rows=[("Preferred name", "Flmodafinil (bisfluoromodafinil; CRL-40,940)"),
              ("CAS number", "90280-13-0"),
              ("Molecular formula", "C<sub>15</sub>H<sub>13</sub>F<sub>2</sub>NO<sub>2</sub>S"),
              ("Molecular weight", "309.3 g/mol")],
        source_url="https://pubchem.ncbi.nlm.nih.gov/compound/"
                   "2-_bis_4-fluorophenyl_methylsulfinyl_acetamide",
        source_label="PubChem",
    ),
}

SPEC_FIELDS = [
    ("CAS number", "[CAS]"),
    ("Molecular formula", "[FORMULA]"),
    ("Molecular weight", "[MW] g/mol"),
    ("Physical form", "[FORM]"),
    ("Purity", "[PURITY]% by HPLC"),
    ("Storage", "[STORAGE]"),
]


def spec_table(route: str) -> str:
    """The identity block for one compound, or nothing if it has no data."""
    cfg = IDENTITY.get(route)
    if cfg is None:
        return ""

    rows = "\n".join(
        f"\t\t\t\t\t\t<tr><th scope=\"row\">{k}</th><td>{v}</td></tr>"
        for k, v in cfg["rows"]
    )
    caution = ""
    if cfg.get("caution"):
        caution = ('\n\t\t\t\t\t<p class="note-caution">' + cfg["caution"] + "</p>")

    return f"""\t\t\t\t\t<h2 class="h-sm">Identity</h2>
\t\t\t\t\t<div class="table-scroll">
\t\t\t\t\t\t<table class="spec-table">
\t\t\t\t\t\t\t<tbody>
{rows}
\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t</table>
\t\t\t\t\t</div>{caution}
\t\t\t\t\t<p class="note-sm">Identity data from
\t\t\t\t\t<a href="{cfg['source_url']}" rel="noopener" target="_blank">{cfg['source_label']}<span class="sr-only"> (opens in a new tab)</span></a>.
\t\t\t\t\tPhysical form, purity and storage are properties of a batch rather
\t\t\t\t\tthan of a compound, so they are not listed here &mdash; take them
\t\t\t\t\tfrom the certificate of analysis and safety data sheet for the
\t\t\t\t\tmaterial you hold.</p>"""


def compound_page(route: str, name: str, parent_label: str, parent_href: str,
                  summary: str, body: str, image: str, alt: str,
                  byline: str = "") -> str:
    """A single compound reference page."""
    return f"""\t<section class="section section--tight">
\t\t<div class="wrap">
\t\t\t<nav class="crumbs" aria-label="Breadcrumb">
\t\t\t\t<a href="/">Home</a>
\t\t\t\t<span aria-hidden="true">/</span>
\t\t\t\t<a href="{parent_href}">{parent_label}</a>
\t\t\t\t<span aria-hidden="true">/</span>
\t\t\t\t<span aria-current="page">{name}</span>
\t\t\t</nav>

\t\t\t<div class="sectionhead">
\t\t\t\t<p class="eyebrow">{parent_label}</p>
\t\t\t\t<h1>{name}</h1>
\t\t\t\t<p class="lede">{summary}</p>
\t\t\t</div>
{byline}
\t\t\t<div class="two-col">
\t\t\t\t<div class="measure prose">
{body}
\t\t\t\t</div>
\t\t\t\t<div>
\t\t\t\t\t<div class="figure" style="margin-bottom:1.5rem">
\t\t\t\t\t\t<img src="/assets/{image}" alt="{alt}" width="1600" height="1067"
\t\t\t\t\t\t     loading="lazy" decoding="async">
\t\t\t\t\t</div>
{spec_table(route)}
\t\t\t\t</div>
\t\t\t</div>
\t\t</div>
\t</section>

{NOTICE}
\t<section class="cta">
\t\t<div class="wrap">
\t\t\t<div class="cta__panel">
\t\t\t\t<h2>Spotted an error?</h2>
\t\t\t\t<p>If something here is wrong or out of date, tell us. Corrections are
\t\t\t\tpublished with a note describing what changed.</p>
\t\t\t\t<div class="btnrow btnrow--center">
\t\t\t\t\t<a class="btn btn--primary" href="/contact/">Get in touch</a>
\t\t\t\t\t<a class="btn btn--light" href="{parent_href}">All {parent_label}</a>
\t\t\t\t</div>
\t\t\t</div>
\t\t</div>
\t</section>
"""


# Body copy per compound. Each describes the material and the state of the
# published record. None describes effects in people, recommends use, or
# gives dosing — that would turn a reference page into a drug claim.
COMPOUNDS = {
    "sarms/gw-501516": dict(
        name="GW-501516 (Cardarine)", parent_label="SARMs", parent_href="/sarms/",
        title="GW-501516",
        summary="A PPAR&delta; agonist, frequently grouped with SARMs although it acts "
                "on a different receptor family entirely.",
        image="ampoules-microscope.jpg",
        alt="Amber and clear glass ampoules on a bench in front of a microscope",
        body="""\t\t\t\t\t<h2>What it is</h2>
\t\t\t\t\t<p>GW-501516 is an agonist at the peroxisome proliferator-activated
\t\t\t\t\treceptor delta (PPAR&delta;), a nuclear receptor involved in lipid
\t\t\t\t\tmetabolism. It is routinely listed alongside SARMs by suppliers, but
\t\t\t\t\tit is not a selective androgen receptor modulator and does not act on
\t\t\t\t\tthe androgen receptor. Treating the two classes as interchangeable is
\t\t\t\t\ta common and consequential error.</p>

\t\t\t\t\t<h2>Development history</h2>
\t\t\t\t\t<p>The compound was investigated in the early 2000s and development
\t\t\t\t\twas discontinued. Published rodent carcinogenicity findings are the
\t\t\t\t\tusually cited reason. Any honest write-up has to lead with that
\t\t\t\t\trather than bury it, and we would rather you read it here than
\t\t\t\t\tdiscover it later.</p>

\t\t\t\t\t<h2>Regulatory status</h2>
\t\t\t\t\t<p>It is not approved for human or veterinary use in any jurisdiction
\t\t\t\t\twe are aware of, and it appears on the World Anti-Doping Agency
\t\t\t\t\tprohibited list.</p>

\t\t\t\t\t<h2>Handling</h2>
\t\t\t\t\t<p>Confirm physical form, solubility and storage against the
\t\t\t\t\tcertificate of analysis for your batch. Solubility differs
\t\t\t\t\tsubstantially between the free acid and salt forms, which is a
\t\t\t\t\tfrequent source of preparation error.</p>"""),

    "sarms/mk-2866": dict(
        name="MK-2866 (Ostarine)", parent_label="SARMs", parent_href="/sarms/",
        title="MK-2866",
        summary="One of the most extensively studied SARMs, and the one with the "
                "largest published clinical record.",
        image="ampoules-bench.jpg",
        alt="Amber glass ampoules on a laboratory bench beside a microscope",
        body="""\t\t\t\t\t<h2>What it is</h2>
\t\t\t\t\t<p>MK-2866 is a non-steroidal selective androgen receptor modulator.
\t\t\t\t\tSARMs bind the androgen receptor with tissue selectivity that differs
\t\t\t\t\tfrom steroidal androgens, which is the property the class was
\t\t\t\t\tdeveloped to exploit.</p>

\t\t\t\t\t<h2>Published record</h2>
\t\t\t\t\t<p>It has been through clinical trials, which makes its record
\t\t\t\t\tunusually substantial for this class &mdash; most SARMs have only
\t\t\t\t\tpreclinical data behind them. Development did not lead to approval.</p>
\t\t\t\t\t<p>Being better studied than its peers is a low bar, and it should not
\t\t\t\t\tbe read as an established safety profile.</p>

\t\t\t\t\t<h2>Regulatory status</h2>
\t\t\t\t\t<p>Not approved for human or veterinary use. Prohibited in sport under
\t\t\t\t\tthe WADA code, and a recurring cause of adverse findings in athlete
\t\t\t\t\ttesting &mdash; often through contaminated supplements rather than
\t\t\t\t\tdeliberate use.</p>

\t\t\t\t\t<h2>Handling</h2>
\t\t\t\t\t<p>Verify identity and purity against your certificate of analysis.
\t\t\t\t\tMislabelling is well documented across this product category, so the
\t\t\t\t\tcertificate matters more here than the label does.</p>"""),

    "sarms/rad-140": dict(
        name="RAD-140 (Testolone)", parent_label="SARMs", parent_href="/sarms/",
        title="RAD-140",
        summary="A non-steroidal SARM whose published record is preclinical, with "
                "notably less human data than MK-2866.",
        image="lab-pipetting.jpg",
        alt="Researcher in gloves transferring a sample into a tube rack",
        body="""\t\t\t\t\t<h2>What it is</h2>
\t\t\t\t\t<p>RAD-140 is a non-steroidal selective androgen receptor modulator
\t\t\t\t\tinvestigated in preclinical work, including studies in animal models
\t\t\t\t\tof muscle wasting and, separately, hormone-receptor-positive breast
\t\t\t\t\tcancer.</p>

\t\t\t\t\t<h2>State of the evidence</h2>
\t\t\t\t\t<p>The published record is thinner than for MK-2866 and largely
\t\t\t\t\tpreclinical. Case reports of liver injury associated with products
\t\t\t\t\tsold as RAD-140 exist in the literature; because those products were
\t\t\t\t\tnot independently characterized, whether the compound or a
\t\t\t\t\tcontaminant was responsible generally cannot be established.</p>
\t\t\t\t\t<p>That ambiguity is itself the point. Without analytical
\t\t\t\t\tcharacterisation you cannot attribute an outcome to a compound at
\t\t\t\t\tall.</p>

\t\t\t\t\t<h2>Regulatory status</h2>
\t\t\t\t\t<p>Not approved for human or veterinary use anywhere we are aware of,
\t\t\t\t\tand prohibited in sport under the WADA code.</p>

\t\t\t\t\t<h2>Handling</h2>
\t\t\t\t\t<p>Confirm form, solubility and storage against your certificate of
\t\t\t\t\tanalysis before preparing anything.</p>"""),

    "peptides/bpc-157": dict(
        name="BPC-157", parent_label="Peptides", parent_href="/peptides/",
        title="BPC-157",
        summary="A synthetic pentadecapeptide studied in animal models, with almost "
                "no published human data.",
        image="lab-pipetting.jpg",
        alt="Researcher in gloves transferring a sample into a tube rack",
        body="""\t\t\t\t\t<h2>What it is</h2>
\t\t\t\t\t<p>BPC-157 is a synthetic peptide of fifteen amino acids, derived from
\t\t\t\t\ta sequence identified in gastric juice. It is supplied lyophilized and
\t\t\t\t\trequires reconstitution before use.</p>

\t\t\t\t\t<h2>State of the evidence</h2>
\t\t\t\t\t<p>The published literature is almost entirely preclinical, and a
\t\t\t\t\tlarge share of it comes from a small number of research groups. That
\t\t\t\t\tconcentration matters: findings replicated only within one group are
\t\t\t\t\tweaker evidence than the raw publication count suggests.</p>
\t\t\t\t\t<p>Controlled human data is minimal. Claims circulating outside the
\t\t\t\t\tliterature considerably outrun what has actually been demonstrated.</p>

\t\t\t\t\t<h2>Handling and stability</h2>
\t\t\t\t\t<p>Store lyophilized material cold and protected from light.
\t\t\t\t\tReconstituted peptide is markedly less stable than the lyophilized
\t\t\t\t\tform, and repeated freeze-thaw cycling degrades it. Record the
\t\t\t\t\treconstitution date &mdash; a peptide is not the same material three
\t\t\t\t\tweeks later.</p>

\t\t\t\t\t<h2>Regulatory status</h2>
\t\t\t\t\t<p>Not an approved medicine. In 2023 the FDA placed it in a category
\t\t\t\t\tof substances barred from compounding pending further evaluation.</p>"""),

    "peptides/semaglutide": dict(
        name="Semaglutide", parent_label="Peptides", parent_href="/peptides/",
        title="Semaglutide",
        summary="A GLP-1 receptor agonist. Unlike most compounds cataloged here, "
                "approved medicines containing it exist.",
        image="ampoules-microscope.jpg",
        alt="Amber and clear glass ampoules on a bench in front of a microscope",
        body="""\t\t\t\t\t<h2>What it is</h2>
\t\t\t\t\t<p>Semaglutide is a glucagon-like peptide-1 receptor agonist: a
\t\t\t\t\tmodified peptide engineered for a substantially longer half-life than
\t\t\t\t\tnative GLP-1.</p>

\t\t\t\t\t<h2>An important distinction</h2>
\t\t\t\t\t<p>Approved prescription medicines containing semaglutide exist, which
\t\t\t\t\tmakes this page different from the others here. Those medicines are
\t\t\t\t\tregulated products with established manufacturing, and material sold
\t\t\t\t\tas a research chemical is not equivalent to them in any respect that
\t\t\t\t\tmatters &mdash; not purity, not sterility, not fill accuracy.</p>
\t\t\t\t\t<p>Research-grade material is not a substitute for a prescribed
\t\t\t\t\tmedicine, and nothing on this page should be read as suggesting
\t\t\t\t\totherwise. Compounded and grey-market semaglutide has been the subject
\t\t\t\t\tof repeated regulatory warnings, including dosing errors traced to
\t\t\t\t\tunlabelled concentration differences.</p>

\t\t\t\t\t<h2>Handling and stability</h2>
\t\t\t\t\t<p>Peptides of this size are sensitive to temperature and to
\t\t\t\t\tagitation. Follow the storage conditions on your certificate of
\t\t\t\t\tanalysis, and treat cold-chain excursions as affecting the
\t\t\t\t\tspecification rather than as a formality.</p>"""),

    "peptides/tb-500": dict(
        name="TB-500", parent_label="Peptides", parent_href="/peptides/",
        title="TB-500",
        summary="A synthetic fragment related to thymosin beta-4, supplied "
                "lyophilized.",
        image="capsule-selection.jpg",
        alt="Gloved hands using tweezers to place a capsule into a sample pot",
        body="""\t\t\t\t\t<h2>What it is</h2>
\t\t\t\t\t<p>TB-500 is a synthetic peptide corresponding to an active region of
\t\t\t\t\tthymosin beta-4, a naturally occurring protein involved in actin
\t\t\t\t\tregulation. It is a fragment, not the full protein &mdash; a
\t\t\t\t\tdistinction frequently lost in product descriptions, and one that
\t\t\t\t\tmatters when comparing against literature on thymosin beta-4
\t\t\t\t\titself.</p>

\t\t\t\t\t<h2>State of the evidence</h2>
\t\t\t\t\t<p>Published work is preclinical. Studies on full-length thymosin
\t\t\t\t\tbeta-4 are sometimes cited as though they establish something about
\t\t\t\t\tthe fragment; they do not, and conflating them overstates the
\t\t\t\t\tevidence.</p>

\t\t\t\t\t<h2>Handling and stability</h2>
\t\t\t\t\t<p>Supplied lyophilized and requiring reconstitution. Store cold,
\t\t\t\t\tprotect from light, and avoid repeated freeze-thaw cycles.
\t\t\t\t\tReconstituted material has a considerably shorter usable life than
\t\t\t\t\tthe lyophilized powder.</p>

\t\t\t\t\t<h2>Regulatory status</h2>
\t\t\t\t\t<p>Not approved for human or veterinary use, and prohibited in sport
\t\t\t\t\tunder the WADA code.</p>"""),

    "nootropics/adrafinil": dict(
        name="Adrafinil", parent_label="Nootropics", parent_href="/nootropics/",
        title="Adrafinil",
        summary="A prodrug that metabolizes to modafinil, with a correspondingly "
                "different pharmacokinetic profile.",
        image="capsule-selection.jpg",
        alt="Gloved hands using tweezers to place a capsule into a sample pot",
        body="""\t\t\t\t\t<h2>What it is</h2>
\t\t\t\t\t<p>Adrafinil is a prodrug: it is metabolized in the liver to
\t\t\t\t\tmodafinil, which is the active compound. It was developed in France
\t\t\t\t\tin the 1970s and later withdrawn from the market there.</p>

\t\t\t\t\t<h2>Why the prodrug relationship matters</h2>
\t\t\t\t\t<p>Because conversion happens in the liver, the compound places a
\t\t\t\t\tmetabolic load that modafinil itself does not. Studies on modafinil
\t\t\t\t\tdo not transfer cleanly to adrafinil for that reason, and treating
\t\t\t\t\tthe two as equivalent misreads both.</p>

\t\t\t\t\t<h2>Regulatory status</h2>
\t\t\t\t\t<p>Not an approved medicine in the United States. Modafinil, its
\t\t\t\t\tmetabolite, is a prescription medicine and a controlled substance
\t\t\t\t\tthere &mdash; a distinction worth understanding before ordering
\t\t\t\t\teither.</p>

\t\t\t\t\t<h2>Handling</h2>
\t\t\t\t\t<p>Supplied as a powder. Confirm purity and identity against the
\t\t\t\t\tcertificate of analysis for your batch.</p>"""),

    "nootropics/cyclazodone": dict(
        name="Cyclazodone", parent_label="Nootropics", parent_href="/nootropics/",
        title="Cyclazodone",
        summary="A substituted aminorex derivative with a notably thin published "
                "record.",
        image="capsule-selection.jpg",
        alt="Gloved hands using tweezers to place a capsule into a sample pot",
        body="""\t\t\t\t\t<h2>What it is</h2>
\t\t\t\t\t<p>Cyclazodone is a derivative of aminorex, related structurally to
\t\t\t\t\tpemoline. It belongs to a family of stimulant compounds, several of
\t\t\t\t\twhich were withdrawn from medical use.</p>

\t\t\t\t\t<h2>State of the evidence</h2>
\t\t\t\t\t<p>The published record is very thin. There is little peer-reviewed
\t\t\t\t\tpharmacology, essentially no controlled human data, and no
\t\t\t\t\testablished safety profile.</p>
\t\t\t\t\t<p>We state that plainly because an absence of evidence is the most
\t\t\t\t\tuseful thing we can tell you about this compound. Related compounds in
\t\t\t\t\tthe same family have documented hepatotoxicity, which is a reason for
\t\t\t\t\tcaution in interpreting the silence rather than comfort.</p>

\t\t\t\t\t<h2>Handling</h2>
\t\t\t\t\t<p>Verify identity and purity analytically. For compounds this poorly
\t\t\t\t\tcharacterised, a certificate of analysis is the only meaningful
\t\t\t\t\tevidence of what you actually have.</p>"""),

    "nootropics/flmodafinil": dict(
        name="Flmodafinil", parent_label="Nootropics", parent_href="/nootropics/",
        title="Flmodafinil",
        summary="A fluorinated modafinil analogue, also written CRL-40,940 and "
                "bisfluoromodafinil.",
        image="ampoules-bench.jpg",
        alt="Amber glass ampoules on a laboratory bench beside a microscope",
        body="""\t\t\t\t\t<h2>What it is</h2>
\t\t\t\t\t<p>Flmodafinil is a modafinil analogue carrying fluorine substitutions
\t\t\t\t\ton the aromatic rings. It appears in the literature and in product
\t\t\t\t\tlistings under several names &mdash; CRL-40,940, bisfluoromodafinil,
\t\t\t\t\tlauflumide &mdash; which makes searching for it unusually
\t\t\t\t\tawkward.</p>

\t\t\t\t\t<h2>State of the evidence</h2>
\t\t\t\t\t<p>Published pharmacology is limited. Claims about how it compares to
\t\t\t\t\tmodafinil circulate widely but rest on very little published work, and
\t\t\t\t\tstructural similarity is not evidence of comparable behavior.</p>

\t\t\t\t\t<h2>Naming and identity</h2>
\t\t\t\t\t<p>Because several names are in use, verify identity by CAS number and
\t\t\t\t\tanalytical data rather than by the name on the label. This is the
\t\t\t\t\tcompound most likely in this catalog to arrive as something other
\t\t\t\t\tthan what was ordered.</p>

\t\t\t\t\t<h2>Handling</h2>
\t\t\t\t\t<p>Supplied as a powder. Confirm purity and storage conditions against
\t\t\t\t\tyour certificate of analysis.</p>"""),

    "nootropics/phenylpiracetam": dict(
        name="Phenylpiracetam", parent_label="Nootropics", parent_href="/nootropics/",
        title="Phenylpiracetam",
        summary="A phenylated racetam developed in the Soviet Union, with much of "
                "its literature published in Russian.",
        image="lab-pipetting.jpg",
        alt="Researcher in gloves transferring a sample into a tube rack",
        body="""\t\t\t\t\t<h2>What it is</h2>
\t\t\t\t\t<p>Phenylpiracetam is a member of the racetam family, structurally
\t\t\t\t\tpiracetam with a phenyl group added. It was developed in the Soviet
\t\t\t\t\tUnion and has been used medically in some post-Soviet states.</p>

\t\t\t\t\t<h2>Reading the literature</h2>
\t\t\t\t\t<p>Much of the published work is in Russian and predates current
\t\t\t\t\ttrial-reporting standards. That does not make it worthless, but it
\t\t\t\t\tdoes mean the evidence base is harder to appraise than a raw citation
\t\t\t\t\tcount suggests &mdash; and English-language summaries of it are often
\t\t\t\t\tmore confident than the underlying papers.</p>

\t\t\t\t\t<h2>Stereochemistry</h2>
\t\t\t\t\t<p>The compound is chiral and is usually supplied as a racemic
\t\t\t\t\tmixture. Where a supplier claims a single enantiomer, that claim needs
\t\t\t\t\tanalytical support, because the two are not interchangeable.</p>

\t\t\t\t\t<h2>Regulatory status</h2>
\t\t\t\t\t<p>Not an approved medicine in the United States or European Union.
\t\t\t\t\tProhibited in sport under the WADA code.</p>"""),
}


def compound_list(parent_href: str) -> str:
    """Links to every compound page under a topic, for the topic page itself.

    A dropdown is not a substitute for links in the page body: it is invisible
    to anyone who arrives from search, and search engines follow body links
    more reliably than JavaScript-adjacent menus.
    """
    entries = [(route, cfg) for route, cfg in COMPOUNDS.items()
               if cfg["parent_href"] == parent_href]
    cards = "\n".join(
        f"""\t\t\t\t<article class="card">
\t\t\t\t\t<h3><a href="/{route}/">{cfg['name']}</a></h3>
\t\t\t\t\t<p class="mb-0">{cfg['summary']}</p>
\t\t\t\t</article>""" for route, cfg in entries
    )
    return f"""\t<section class="section section--tight">
\t\t<div class="wrap">
\t\t\t<div class="sectionhead">
\t\t\t\t<h2>Compounds in this section</h2>
\t\t\t</div>
\t\t\t<div class="cards">
{cards}
\t\t\t</div>
\t\t</div>
\t</section>

"""


def with_compounds(topic_html: str, parent_href: str) -> str:
    """Insert the compound list ahead of the research-use-only notice."""
    return topic_html.replace(NOTICE, compound_list(parent_href) + NOTICE, 1)


def build_compound_pages() -> None:
    for route, cfg in COMPOUNDS.items():
        shared = dict(
            route=route, name=cfg["name"], parent_label=cfg["parent_label"],
            parent_href=cfg["parent_href"], summary=cfg["summary"],
            body=cfg["body"], image=cfg["image"], alt=cfg["alt"],
        )
        # Build once without the byline to date the page, then again with it.
        # Hashing the date-free version is what stops the stamp from being its
        # own reason to re-stamp.
        undated = compound_page(**shared, byline="")
        published, updated = DATES.for_page(
            route, f"site/{rel_for(route)}", undated)
        body = compound_page(**shared, byline=byline(published, updated))

        # The partner sells peptides, so the placement runs on the peptide
        # pages only. Showing it against a SARM or a nootropic would promote
        # a supplier for material they do not stock.
        if cfg["parent_href"] == "/peptides/":
            body = with_partner(body)

        write(route, cfg["title"],
              f"{cfg['name']}: identity, handling and the state of the published "
              f"record. Laboratory research use only.", body,
              hash_body=undated,
              crumbs=[("Home", "/"),
                      (cfg["parent_label"], cfg["parent_href"]),
                      (cfg["name"], None)])


# --------------------------------------------------------------------------
# Contact page
# --------------------------------------------------------------------------
#
# The site is otherwise plain static files, but a static page cannot send an
# email. SiteGround serves this over Apache with PHP available, so the contact
# page is a .php file that both renders itself and handles its own POST. That
# avoids depending on a third-party form service.
#
# If PHP mail() turns out to be blocked on the hosting plan, the fallback is a
# form service (Formspree, Web3Forms, Basin): change the form's action to the
# endpoint they give you and delete the PHP block.

CONTACT_PHP = r"""<?php
/**
 * Contact form handler for researchlabusa.com.
 *
 * Renders the page and, on POST, emails the inquiry to the address in $to.
 * Kept in one file so a failed submission can redisplay the form with the
 * visitor's text still in it, rather than losing what they typed.
 */

$sent   = false;
$errors = [];
$values = ['name' => '', 'email' => '', 'phone' => '', 'subject' => '', 'message' => ''];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    foreach ($values as $key => $_) {
        $values[$key] = trim((string) ($_POST[$key] ?? ''));
    }

    // Honeypot. The field is hidden from people, so anything in it came from
    // a bot. Report success rather than an error: telling a bot it failed
    // just invites a retry with the field left empty.
    if (trim((string) ($_POST['company'] ?? '')) !== '') {
        $sent   = true;
        $values = array_fill_keys(array_keys($values), '');
    } else {

        if ($values['name'] === '') {
            $errors[] = 'Please tell us your name.';
        }
        if (!filter_var($values['email'], FILTER_VALIDATE_EMAIL)) {
            $errors[] = 'Please enter an email address we can reply to.';
        }
        if ($values['message'] === '') {
            $errors[] = 'Please write a message.';
        }

        if (!$errors) {
            $to = 'info@researchlabusa.com';

            // Strip CR and LF from anything that reaches a mail header.
            // Without this a crafted address could append its own headers and
            // turn the form into an open relay.
            $header_safe = static function ($value) {
                return trim(str_replace(["\r", "\n", "%0a", "%0d"], ' ', $value));
            };

            $subject = $values['subject'] !== ''
                ? $header_safe($values['subject'])
                : 'Website inquiry';

            // From must be an address on this domain or SPF and DKIM fail and
            // the mail lands in spam. The visitor's address goes in Reply-To,
            // so hitting reply still reaches them.
            $headers = implode("\r\n", [
                'From: Research Lab USA <noreply@researchlabusa.com>',
                'Reply-To: ' . $header_safe($values['email']),
                'Content-Type: text/plain; charset=UTF-8',
                'MIME-Version: 1.0',
            ]);

            $body = "New inquiry from the website contact form.\n\n"
                  . 'Name:    ' . $values['name'] . "\n"
                  . 'Email:   ' . $values['email'] . "\n"
                  . 'Phone:   ' . ($values['phone'] !== '' ? $values['phone'] : '(not given)') . "\n"
                  . 'Subject: ' . ($values['subject'] !== '' ? $values['subject'] : '(none)') . "\n\n"
                  . "Message:\n" . $values['message'] . "\n";

            $sent = @mail($to, '[Website] ' . $subject, $body, $headers);

            if ($sent) {
                $values = array_fill_keys(array_keys($values), '');
            } else {
                $errors[] = 'Something went wrong sending your message. '
                          . 'Please email us directly at info@researchlabusa.com.';
            }
        }
    }
}

/** Escape a value for safe output in HTML. */
function e($value) {
    return htmlspecialchars((string) $value, ENT_QUOTES, 'UTF-8');
}
?>
"""

CONTACT = """\t<section class="section">
\t\t<div class="wrap">
\t\t\t<div class="sectionhead">
\t\t\t\t<p class="eyebrow">""" + ICON_DNA + """ Contact us</p>
\t\t\t\t<h1>Write to us any time</h1>
\t\t\t\t<p class="lede">Questions about a guide, corrections, and suggestions
\t\t\t\tfor what to cover next are all welcome. We reply within one business
\t\t\t\tday.</p>
\t\t\t</div>

\t\t\t<div class="contactgrid">
\t\t\t\t<!-- Contact details panel -->
\t\t\t\t<aside class="contactpanel">
\t\t\t\t\t<div class="contactpanel__top">
\t\t\t\t\t\t<div class="contactpanel__item">
\t\t\t\t\t\t\t<span class="contactpanel__icon" aria-hidden="true">
\t\t\t\t\t\t\t\t<svg viewBox="0 0 24 24"><path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm9 8L4.2 7.2v.9L12 14l7.8-5.9v-.9Z"/></svg>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t\t<div>
\t\t\t\t\t\t\t\t<p class="contactpanel__label">Send an email</p>
\t\t\t\t\t\t\t\t<p class="contactpanel__value">
\t\t\t\t\t\t\t\t\t<a href="mailto:""" + EMAIL + '">' + EMAIL + """</a>
\t\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="contactpanel__item">
\t\t\t\t\t\t\t<span class="contactpanel__icon" aria-hidden="true">
\t\t\t\t\t\t\t\t<svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg>
\t\t\t\t\t\t\t</span>
\t\t\t\t\t\t\t<div>
\t\t\t\t\t\t\t\t<p class="contactpanel__label">Response time</p>
\t\t\t\t\t\t\t\t<p class="contactpanel__value">Within one business day</p>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

\t\t\t\t\t<div class="contactpanel__media">
\t\t\t\t\t\t<img src="/assets/ampoules-microscope.jpg"
\t\t\t\t\t\t     alt="Glass ampoules on a bench in front of a microscope"
\t\t\t\t\t\t     width="1600" height="1067" loading="lazy" decoding="async">
\t\t\t\t\t</div>
\t\t\t\t</aside>

\t\t\t\t<!-- Inquiry form -->
\t\t\t\t<div class="contactform">
<?php if ($sent): ?>
\t\t\t\t\t<p class="formnote formnote--ok" role="status">
\t\t\t\t\t\t<strong>Thank you &mdash; your message has been sent.</strong>
\t\t\t\t\t\tWe reply within one business day.
\t\t\t\t\t</p>
<?php endif; ?>
<?php if ($errors): ?>
\t\t\t\t\t<div class="formnote formnote--error" role="alert">
\t\t\t\t\t\t<strong>Your message was not sent.</strong>
\t\t\t\t\t\t<ul>
<?php foreach ($errors as $error): ?>
\t\t\t\t\t\t\t<li><?= e($error) ?></li>
<?php endforeach; ?>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>
<?php endif; ?>

\t\t\t\t\t<form method="post" action="/contact/#form" id="form" novalidate>
\t\t\t\t\t\t<div class="formgrid">
\t\t\t\t\t\t\t<div class="field">
\t\t\t\t\t\t\t\t<label class="label" for="name">Your name</label>
\t\t\t\t\t\t\t\t<input class="input" type="text" id="name" name="name"
\t\t\t\t\t\t\t\t       value="<?= e($values['name']) ?>" required>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="field">
\t\t\t\t\t\t\t\t<label class="label" for="email">Email address</label>
\t\t\t\t\t\t\t\t<input class="input" type="email" id="email" name="email"
\t\t\t\t\t\t\t\t       value="<?= e($values['email']) ?>" required>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="field">
\t\t\t\t\t\t\t\t<label class="label" for="phone">Phone <span class="label__opt">(optional)</span></label>
\t\t\t\t\t\t\t\t<input class="input" type="tel" id="phone" name="phone"
\t\t\t\t\t\t\t\t       value="<?= e($values['phone']) ?>">
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t<div class="field">
\t\t\t\t\t\t\t\t<label class="label" for="subject">Subject <span class="label__opt">(optional)</span></label>
\t\t\t\t\t\t\t\t<input class="input" type="text" id="subject" name="subject"
\t\t\t\t\t\t\t\t       value="<?= e($values['subject']) ?>">
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="field">
\t\t\t\t\t\t\t<label class="label" for="message">Your message</label>
\t\t\t\t\t\t\t<textarea class="textarea" id="message" name="message" rows="8"
\t\t\t\t\t\t\t          required><?= e($values['message']) ?></textarea>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<!-- Honeypot: hidden from people, irresistible to bots. -->
\t\t\t\t\t\t<div class="hp" aria-hidden="true">
\t\t\t\t\t\t\t<label for="company">Company</label>
\t\t\t\t\t\t\t<input type="text" id="company" name="company" tabindex="-1" autocomplete="off">
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<button class="btn btn--primary" type="submit">Send message</button>
\t\t\t\t\t\t<p class="note-sm">We use what you send through this form only to
\t\t\t\t\t\tread and answer your inquiry. Please do not submit confidential,
\t\t\t\t\t\tpatient or medical information. We do not sell contact-form
\t\t\t\t\t\tinformation or share it with anyone for their own marketing. It
\t\t\t\t\t\tmay be handled by the service providers that run our website and
\t\t\t\t\t\temail, under confidentiality obligations. For the detail, read our
\t\t\t\t\t\t<a href="/privacy/">Privacy Policy</a> and
\t\t\t\t\t\t<a href="/terms/">Terms of Use</a>.</p>
\t\t\t\t\t</form>
\t\t\t\t</div>
\t\t\t</div>
\t\t</div>
\t</section>

\t<section class="section section--tight">
\t\t<div class="wrap">
\t\t\t<div class="measure prose">
\t\t\t\t<h2>What we can help with</h2>
\t\t\t\t<ul>
\t\t\t\t\t<li>Questions about anything in a guide</li>
\t\t\t\t\t<li>Corrections, including sources we have missed or misread</li>
\t\t\t\t\t<li>Suggestions for compounds or topics to cover next</li>
\t\t\t\t\t<li>Requests to cite or reference our material</li>
\t\t\t\t</ul>

\t\t\t\t<h2>What we cannot help with</h2>
\t\t\t\t<p>We do not give dosing guidance or advise on human or veterinary
\t\t\t\tuse, and we do not vet suppliers or settle disputes with them.
\t\t\t\tMessages asking for those will not get a useful reply, and we would
\t\t\t\trather say so here than leave you waiting for one.</p>
\t\t\t\t<p>""" + PARTNER_NAME + """ is our peptide supply partner, and you
\t\t\t\twill see them featured on our peptide pages. Questions about their
\t\t\t\tcatalogue, an order or a batch should go to them directly &mdash; we
\t\t\t\tcannot answer those for them.</p>
\t\t\t</div>
\t\t</div>
\t</section>

""" + NOTICE

if __name__ == "__main__":
    main()
