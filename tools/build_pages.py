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
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"


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
    ("/sarms.html", "SARMs", [
        ("/sarms/gw-501516.html", "GW-501516 (Cardarine)"),
        ("/sarms/mk-2866.html", "MK-2866 (Ostarine)"),
        ("/sarms/rad-140.html", "RAD-140 (Testolone)"),
    ]),
    ("/peptides.html", "Peptides", [
        ("/peptides/bpc-157.html", "BPC-157"),
        ("/peptides/semaglutide.html", "Semaglutide"),
        ("/peptides/tb-500.html", "TB-500"),
    ]),
    ("/nootropics.html", "Nootropics", [
        ("/nootropics/adrafinil.html", "Adrafinil"),
        ("/nootropics/cyclazodone.html", "Cyclazodone"),
        ("/nootropics/flmodafinil.html", "Flmodafinil"),
        ("/nootropics/phenylpiracetam.html", "Phenylpiracetam"),
    ]),
    ("/guides.html", "Guides", []),
    ("/about.html", "About", []),
    ("/contact.html", "Contact", []),
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


def head(title: str, description: str, canonical: str,
         full_title: str | None = None) -> str:
    # Pages get "Page | Site"; a page may override with its own full title
    # where a more descriptive one reads better in search results.
    if full_title is None:
        full_title = title if title == SITE_NAME else f"{title} | {SITE_NAME}"
    return f"""<!doctype html>
<html lang="en">
<head>
\t<meta charset="utf-8">
\t<meta name="viewport" content="width=device-width, initial-scale=1">
\t<title>{full_title}</title>
\t<meta name="description" content="{description}">
\t<link rel="canonical" href="https://researchlabusa.com{canonical}">
\t<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
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
\t\t\t<span class="logo__text">Research<strong>Lab USA</strong></span>
\t\t</a>

\t\t<button class="navtoggle" aria-expanded="false" aria-controls="mainnav">
\t\t\t<span class="navtoggle__bars" aria-hidden="true"></span>
\t\t\t<span class="sr-only">Menu</span>
\t\t</button>

\t\t<nav class="nav" id="mainnav" aria-label="Main">
{nav_links(canonical)}
\t\t</nav>

\t\t<div class="header__actions">
\t\t\t<a class="btn btn--ghost" href="/contact.html">Enquire</a>
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
\t\t\t\t\t<li><a href="/sarms.html">SARMs</a></li>
\t\t\t\t\t<li><a href="/peptides.html">Peptides</a></li>
\t\t\t\t\t<li><a href="/nootropics.html">Nootropics</a></li>
\t\t\t\t\t<li><a href="/guides.html">All guides</a></li>
\t\t\t\t</ul>
\t\t\t</div>
\t\t\t<div>
\t\t\t\t<p class="footer__title">Site</p>
\t\t\t\t<ul class="footer__list">
\t\t\t\t\t<li><a href="/about.html">About</a></li>
\t\t\t\t\t<li><a href="/contact.html">Contact</a></li>
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
\t\t\t\t<strong>For laboratory and research use only.</strong> The materials
\t\t\t\tdiscussed on this website are not medicines, dietary supplements,
\t\t\t\tcosmetics or food. None has been evaluated or approved by the FDA for
\t\t\t\thuman or veterinary use. Nothing here is medical advice, and nothing
\t\t\t\there should be read as a suggestion that any compound is safe or
\t\t\t\teffective for any purpose.
\t\t\t</p>
\t\t</div>
\t</section>
"""


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
\t\t\t\t\t<a class="btn btn--primary" href="/contact.html">Get in touch</a>
\t\t\t\t</div>
\t\t\t</div>
\t\t</div>
\t</section>
"""


def write(path: str, title: str, description: str, body: str,
          full_title: str | None = None) -> None:
    canonical = "/" if path == "index.html" else f"/{path}"
    out = head(title, description, canonical, full_title) + body + FOOTER
    (SITE / path).write_text(out, encoding="utf-8")
    print(f"wrote site/{path}  ({len(out.splitlines())} lines)")


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
\t\t\t\tbecause for almost everything catalogued here nobody reliably
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
\t\t\tthat a compound is poorly characterised, that its development was
\t\t\tdiscontinued, or that the enthusiasm around it outruns the published
\t\t\twork &mdash; all of which appear on pages here.</p>
\t\t\t<p>That is the whole proposition. A reference that only ever sounds
\t\t\tpositive is not a reference.</p>

\t\t\t<h2>Get in touch</h2>
\t\t\t<p>Corrections, questions and suggestions for what to cover next are all
\t\t\twelcome, and corrections get published. Reach us at
\t\t\t<a href="mailto:""" + EMAIL + """">""" + EMAIL + """</a> or through the
\t\t\t<a href="/contact.html">contact page</a>.</p>
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
\t\t\t\t\t<a class="btn btn--primary" href="/contact.html">Contact us</a>
\t\t\t\t\t<a class="btn btn--light" href="/guides.html">Browse the guides</a>
\t\t\t\t</div>
\t\t\t</div>
\t\t</div>
\t</section>
"""

CONTACT = """\t<section class="section">
\t\t<div class="wrap">
\t\t\t<div class="sectionhead">
\t\t\t\t<p class="eyebrow">Contact</p>
\t\t\t\t<h1>Get in touch</h1>
\t\t\t\t<p class="lede">Questions about a guide, corrections, and suggestions
\t\t\t\tfor what to cover next are all welcome.</p>
\t\t\t</div>
\t\t</div>
\t</section>

\t<section class="section section--tight">
\t\t<div class="wrap two-col">
\t\t\t<div class="measure prose">
\t\t\t\t<h2>Email</h2>
\t\t\t\t<p>Write to <a href="mailto:""" + EMAIL + '">' + EMAIL + """</a> and we
\t\t\t\twill reply within one business day.</p>

\t\t\t\t<h2>What we can help with</h2>
\t\t\t\t<ul>
\t\t\t\t\t<li>Questions about the content of a guide</li>
\t\t\t\t\t<li>Corrections &mdash; including sources we have missed or misread</li>
\t\t\t\t\t<li>Suggestions for compounds or topics to cover</li>
\t\t\t\t\t<li>Requests to cite or reference our material</li>
\t\t\t\t</ul>

\t\t\t\t<h2>What we cannot help with</h2>
\t\t\t\t<p>We do not give dosing guidance, advise on human or veterinary use,
\t\t\t\tor recommend where to buy anything. Messages asking for those will not
\t\t\t\tget a useful reply, and we would rather say so up front than leave you
\t\t\t\twaiting.</p>
\t\t\t</div>
\t\t\t<div class="figure">
\t\t\t\t<img src="/assets/ampoules-microscope.jpg"
\t\t\t\t     alt="Glass ampoules on a bench in front of a microscope"
\t\t\t\t     width="1600" height="1067" loading="lazy" decoding="async">
\t\t\t</div>
\t\t</div>
\t</section>

""" + NOTICE

GUIDE_CARDS = [
    ("GW-501516", "ampoules-microscope.jpg",
     "Amber and clear glass ampoules on a bench in front of a microscope",
     "A PPAR&delta; receptor agonist studied in metabolic and endurance research. "
     "Covers chemical identity, handling and storage, and what the published animal "
     "literature does and does not establish.", True),
    ("TB-500", "lab-pipetting.jpg",
     "Researcher in gloves transferring a sample into a tube rack",
     "A synthetic peptide fragment related to thymosin beta-4. Sets out its sequence, "
     "reconstitution and cold-chain requirements, and summarises the preclinical work "
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
\t\t\t<a href="/contact.html">tell us</a> &mdash; requests genuinely shape what
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
\t\t\t\t<p>Lyophilised material and material in solution behave differently, and
\t\t\t\twe treat them separately rather than collapsing both into one
\t\t\t\tinstruction.</p>""",
    covers=[
        ("Sequence and identity", "Amino acid sequence, molecular weight, and the "
         "analytical method used to establish purity."),
        ("Reconstitution", "Appropriate solvents, concentrations, and the handling "
         "steps that affect stability after reconstitution."),
        ("Cold chain", "Storage temperatures for lyophilised and reconstituted "
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
\t\t\t\tpoorly characterised, that is stated at the top of the page rather than
\t\t\t\tburied &mdash; an absence of evidence is itself the most useful thing we
\t\t\t\tcan tell you.</p>
\t\t\t\t<p>We cover structure, stability and analytical identity, and summarise
\t\t\t\twhat has been published without extrapolating it into claims about
\t\t\t\teffects in people.</p>""",
    covers=[
        ("Structure and class", "Chemical structure, the family a compound belongs "
         "to, and the closely related materials it is confused with."),
        ("Analytical identity", "How the compound is identified and what purity "
         "testing on it typically reports."),
        ("Stability", "Known degradation behaviour and the storage conditions that "
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
\t\t\t\t\t<a class="btn btn--primary" href="/guides.html">Browse the guides</a>
\t\t\t\t\t<a class="btn btn--secondary" href="/">Go to the homepage</a>
\t\t\t\t</div>
\t\t\t</div>
\t\t</div>
\t</section>
"""


def main() -> None:
    home_body = (ROOT / "content" / "home.html").read_text(encoding="utf-8")

    write("index.html", SITE_NAME,
          "Independent guides, methods notes and reference data on research compounds, "
          "peptides and nootropics. Written for laboratory researchers. "
          "For research use only.",
          home_body,
          full_title="Research Lab USA \u2014 Research Compound Guides "
                     "&amp; Laboratory Resources")

    write("about.html", "About",
          "Who we are, how we write, and how we handle corrections. Independent "
          "reference material for laboratory researchers.", ABOUT)

    write("contact.html", "Contact",
          "Questions, corrections and suggestions for what to cover next. "
          f"Reach us at {EMAIL}.", CONTACT)

    write("guides.html", "Guides",
          "Reference guides covering chemical identity, handling, storage and the "
          "state of the published literature.", GUIDES)

    write("sarms.html", "SARMs",
          "Reference material on selective androgen receptor modulators as laboratory "
          "research compounds. For research use only.",
          with_compounds(SARMS, "/sarms.html"))

    write("peptides.html", "Peptides",
          "Research peptide reference material: sequences, reconstitution, cold-chain "
          "handling and stability. For research use only.",
          with_compounds(PEPTIDES, "/peptides.html"))

    write("nootropics.html", "Nootropics",
          "Reference material on nootropic research compounds, with an explicit account "
          "of where the published evidence is thin.",
          with_compounds(NOOTROPICS, "/nootropics.html"))

    write("404.html", "Page not found",
          "The page you were looking for does not exist.", NOT_FOUND)

    build_compound_pages()



# --------------------------------------------------------------------------
# Individual compound pages
# --------------------------------------------------------------------------
#
# Identifiers (CAS, formula, molecular weight) are deliberately left as
# placeholders. This is a reference site: a wrong CAS number sends someone
# after the wrong material, which is worse than an obvious blank. Fill each
# one in from the certificate of analysis for the batch you hold, and the
# blank makes it plain which pages are still unverified.

SPEC_FIELDS = [
    ("CAS number", "[CAS]"),
    ("Molecular formula", "[FORMULA]"),
    ("Molecular weight", "[MW] g/mol"),
    ("Physical form", "[FORM]"),
    ("Purity", "[PURITY]% by HPLC"),
    ("Storage", "[STORAGE]"),
]


def spec_table() -> str:
    rows = "\n".join(
        f"\t\t\t\t\t\t<tr><th scope=\"row\">{k}</th><td>{v}</td></tr>"
        for k, v in SPEC_FIELDS
    )
    return f"""\t\t\t\t<div class="table-scroll">
\t\t\t\t\t<table class="spec-table">
\t\t\t\t\t\t<tbody>
{rows}
\t\t\t\t\t\t</tbody>
\t\t\t\t\t</table>
\t\t\t\t</div>"""


def compound_page(name: str, parent_label: str, parent_href: str,
                  summary: str, body: str, image: str, alt: str) -> str:
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

\t\t\t<div class="two-col">
\t\t\t\t<div class="measure prose">
{body}
\t\t\t\t</div>
\t\t\t\t<div>
\t\t\t\t\t<div class="figure" style="margin-bottom:1.5rem">
\t\t\t\t\t\t<img src="/assets/{image}" alt="{alt}" width="1600" height="1067"
\t\t\t\t\t\t     loading="lazy" decoding="async">
\t\t\t\t\t</div>
\t\t\t\t\t<h2 class="h-sm">Specification</h2>
{spec_table()}
\t\t\t\t\t<p class="note-sm">Values in brackets are unverified. Confirm each
\t\t\t\t\tagainst the certificate of analysis for the batch you hold.</p>
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
\t\t\t\t\t<a class="btn btn--primary" href="/contact.html">Get in touch</a>
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
    "sarms/gw-501516.html": dict(
        name="GW-501516 (Cardarine)", parent_label="SARMs", parent_href="/sarms.html",
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

    "sarms/mk-2866.html": dict(
        name="MK-2866 (Ostarine)", parent_label="SARMs", parent_href="/sarms.html",
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

    "sarms/rad-140.html": dict(
        name="RAD-140 (Testolone)", parent_label="SARMs", parent_href="/sarms.html",
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
\t\t\t\t\tnot independently characterised, whether the compound or a
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

    "peptides/bpc-157.html": dict(
        name="BPC-157", parent_label="Peptides", parent_href="/peptides.html",
        title="BPC-157",
        summary="A synthetic pentadecapeptide studied in animal models, with almost "
                "no published human data.",
        image="lab-pipetting.jpg",
        alt="Researcher in gloves transferring a sample into a tube rack",
        body="""\t\t\t\t\t<h2>What it is</h2>
\t\t\t\t\t<p>BPC-157 is a synthetic peptide of fifteen amino acids, derived from
\t\t\t\t\ta sequence identified in gastric juice. It is supplied lyophilised and
\t\t\t\t\trequires reconstitution before use.</p>

\t\t\t\t\t<h2>State of the evidence</h2>
\t\t\t\t\t<p>The published literature is almost entirely preclinical, and a
\t\t\t\t\tlarge share of it comes from a small number of research groups. That
\t\t\t\t\tconcentration matters: findings replicated only within one group are
\t\t\t\t\tweaker evidence than the raw publication count suggests.</p>
\t\t\t\t\t<p>Controlled human data is minimal. Claims circulating outside the
\t\t\t\t\tliterature considerably outrun what has actually been demonstrated.</p>

\t\t\t\t\t<h2>Handling and stability</h2>
\t\t\t\t\t<p>Store lyophilised material cold and protected from light.
\t\t\t\t\tReconstituted peptide is markedly less stable than the lyophilised
\t\t\t\t\tform, and repeated freeze-thaw cycling degrades it. Record the
\t\t\t\t\treconstitution date &mdash; a peptide is not the same material three
\t\t\t\t\tweeks later.</p>

\t\t\t\t\t<h2>Regulatory status</h2>
\t\t\t\t\t<p>Not an approved medicine. In 2023 the FDA placed it in a category
\t\t\t\t\tof substances barred from compounding pending further evaluation.</p>"""),

    "peptides/semaglutide.html": dict(
        name="Semaglutide", parent_label="Peptides", parent_href="/peptides.html",
        title="Semaglutide",
        summary="A GLP-1 receptor agonist. Unlike most compounds catalogued here, "
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

    "peptides/tb-500.html": dict(
        name="TB-500", parent_label="Peptides", parent_href="/peptides.html",
        title="TB-500",
        summary="A synthetic fragment related to thymosin beta-4, supplied "
                "lyophilised.",
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
\t\t\t\t\t<p>Supplied lyophilised and requiring reconstitution. Store cold,
\t\t\t\t\tprotect from light, and avoid repeated freeze-thaw cycles.
\t\t\t\t\tReconstituted material has a considerably shorter usable life than
\t\t\t\t\tthe lyophilised powder.</p>

\t\t\t\t\t<h2>Regulatory status</h2>
\t\t\t\t\t<p>Not approved for human or veterinary use, and prohibited in sport
\t\t\t\t\tunder the WADA code.</p>"""),

    "nootropics/adrafinil.html": dict(
        name="Adrafinil", parent_label="Nootropics", parent_href="/nootropics.html",
        title="Adrafinil",
        summary="A prodrug that metabolises to modafinil, with a correspondingly "
                "different pharmacokinetic profile.",
        image="capsule-selection.jpg",
        alt="Gloved hands using tweezers to place a capsule into a sample pot",
        body="""\t\t\t\t\t<h2>What it is</h2>
\t\t\t\t\t<p>Adrafinil is a prodrug: it is metabolised in the liver to
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

    "nootropics/cyclazodone.html": dict(
        name="Cyclazodone", parent_label="Nootropics", parent_href="/nootropics.html",
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

    "nootropics/flmodafinil.html": dict(
        name="Flmodafinil", parent_label="Nootropics", parent_href="/nootropics.html",
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
\t\t\t\t\tstructural similarity is not evidence of comparable behaviour.</p>

\t\t\t\t\t<h2>Naming and identity</h2>
\t\t\t\t\t<p>Because several names are in use, verify identity by CAS number and
\t\t\t\t\tanalytical data rather than by the name on the label. This is the
\t\t\t\t\tcompound most likely in this catalogue to arrive as something other
\t\t\t\t\tthan what was ordered.</p>

\t\t\t\t\t<h2>Handling</h2>
\t\t\t\t\t<p>Supplied as a powder. Confirm purity and storage conditions against
\t\t\t\t\tyour certificate of analysis.</p>"""),

    "nootropics/phenylpiracetam.html": dict(
        name="Phenylpiracetam", parent_label="Nootropics", parent_href="/nootropics.html",
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
    entries = [(href, cfg) for href, cfg in COMPOUNDS.items()
               if cfg["parent_href"] == parent_href]
    cards = "\n".join(
        f"""\t\t\t\t<article class="card">
\t\t\t\t\t<h3><a href="/{href}">{cfg['name']}</a></h3>
\t\t\t\t\t<p class="mb-0">{cfg['summary']}</p>
\t\t\t\t</article>""" for href, cfg in entries
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
    for path, cfg in COMPOUNDS.items():
        (SITE / path).parent.mkdir(parents=True, exist_ok=True)
        body = compound_page(
            name=cfg["name"], parent_label=cfg["parent_label"],
            parent_href=cfg["parent_href"], summary=cfg["summary"],
            body=cfg["body"], image=cfg["image"], alt=cfg["alt"],
        )
        write(path, cfg["title"],
              f"{cfg['name']}: identity, handling and the state of the published "
              f"record. Laboratory research use only.", body)

if __name__ == "__main__":
    main()
