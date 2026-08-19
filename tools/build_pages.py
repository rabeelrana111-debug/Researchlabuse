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

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

SITE_NAME = "Research Lab USA"
EMAIL = "info@researchlabusa.com"

NAV = [
    ("/", "Home"),
    ("/sarms.html", "SARMs"),
    ("/peptides.html", "Peptides"),
    ("/nootropics.html", "Nootropics"),
    ("/guides.html", "Guides"),
    ("/about.html", "About"),
    ("/contact.html", "Contact"),
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
    out = []
    for href, label in NAV:
        # aria-current marks the page being viewed for assistive technology,
        # and the stylesheet keys the active underline off the same attribute.
        cur = ' aria-current="page"' if href == current else ""
        out.append(f'\t\t\t<a href="{href}"{cur}>{label}</a>')
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
\t<link rel="stylesheet" href="/styles.css">
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

<script src="/script.js" defer></script>
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
\t\t\t\t<p class="eyebrow">About</p>
\t\t\t\t<h1>Who we are and how we work</h1>
\t\t\t\t<p class="lede">We publish reference material on research compounds for
\t\t\t\tpeople who read the methods section first.</p>
\t\t\t</div>
\t\t</div>
\t</section>

\t<section class="section section--tight">
\t\t<div class="wrap two-col">
\t\t\t<div class="measure prose">
\t\t\t\t<h2>Why we publish</h2>
\t\t\t\t<p>Most writing about research compounds falls into one of two camps:
\t\t\t\ttoo thin to act on, or written to rank in search rather than to inform.
\t\t\t\tWe started publishing to fill the gap in between &mdash; material
\t\t\t\tdetailed enough to be useful, written plainly enough to be read.</p>

\t\t\t\t<h2>How we write</h2>
\t\t\t\t<p>Every guide states what is known, where that knowledge comes from,
\t\t\t\tand what remains unresolved. Claims are linked to the study behind
\t\t\t\tthem so you can check the original rather than take our word for it.</p>
\t\t\t\t<p>Where the evidence is thin or contested, we say so. Rounding an
\t\t\t\topen question up to a confident answer is the most common failure in
\t\t\t\tthis subject area, and it is the one we work hardest to avoid.</p>

\t\t\t\t<h2>Corrections</h2>
\t\t\t\t<p>When something turns out to be wrong, the page is updated with a
\t\t\t\tdated note describing what changed and why. We do not quietly edit
\t\t\t\tpages and leave no trace &mdash; if you relied on an earlier version,
\t\t\t\tyou deserve to know it changed.</p>

\t\t\t\t<h2>What we do not do</h2>
\t\t\t\t<p>We do not provide dosing guidance, protocols for human use, or
\t\t\t\tadvice on obtaining materials for personal use. Everything here is
\t\t\t\twritten for laboratory research by qualified professionals, and we
\t\t\t\tcannot answer questions that fall outside that.</p>
\t\t\t</div>
\t\t\t<div class="figure">
\t\t\t\t<img src="/assets/lab-pipetting.jpg"
\t\t\t\t     alt="Researcher in gloves transferring a sample into a tube rack"
\t\t\t\t     width="1600" height="1067" loading="lazy" decoding="async">
\t\t\t</div>
\t\t</div>
\t</section>

""" + NOTICE + """
\t<section class="cta">
\t\t<div class="wrap">
\t\t\t<div class="cta__panel">
\t\t\t\t<h2>Found something wrong?</h2>
\t\t\t\t<p>Corrections are genuinely welcome, and they get published.</p>
\t\t\t\t<div class="btnrow btnrow--center">
\t\t\t\t\t<a class="btn btn--primary" href="/contact.html">Tell us</a>
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
          "research compounds. For research use only.", SARMS)

    write("peptides.html", "Peptides",
          "Research peptide reference material: sequences, reconstitution, cold-chain "
          "handling and stability. For research use only.", PEPTIDES)

    write("nootropics.html", "Nootropics",
          "Reference material on nootropic research compounds, with an explicit account "
          "of where the published evidence is thin.", NOOTROPICS)

    write("404.html", "Page not found",
          "The page you were looking for does not exist.", NOT_FOUND)


if __name__ == "__main__":
    main()
