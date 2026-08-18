# Design System — Research Lab USA

Clinical blue and white. All values live as CSS custom properties in
`wp-content/themes/hello-elementor-child/style.css`. Change a token there and
it updates everywhere on the site.

---

## 1. Palette

| Token | Hex | Use |
|---|---|---|
| `--rl-blue-900` | `#06274A` | Footer, dark sections, overlays |
| `--rl-blue-800` | `#0A3A6C` | Badge text, deep accents |
| `--rl-blue-700` | `#0B4A87` | **Primary** — buttons, links |
| `--rl-blue-600` | `#1263AF` | Button hover |
| `--rl-blue-500` | `#2E7DD1` | Focus rings, interactive highlights |
| `--rl-blue-100` | `#DCEAF8` | Badge and icon backgrounds |
| `--rl-blue-50` | `#F1F7FD` | Alternating section background |
| `--rl-ink` | `#0F172A` | Headings |
| `--rl-body` | `#45566B` | Body text |
| `--rl-muted` | `#6B7C93` | Captions, meta text |
| `--rl-line` | `#E2E8F0` | Borders, dividers |
| `--rl-success` | `#0E7C66` | In stock, verified |
| `--rl-warning` | `#B4690E` | Low stock |
| `--rl-danger` | `#B42318` | Out of stock, required notices |

Primary blue on white and white on primary blue both clear WCAG AA for normal
text, so the core combinations are accessible by default. If you swap the
palette, re-check contrast before publishing — `--rl-muted` on white is the
first pairing that will fail if you lighten it.

### Mirror these into Elementor

Elementor styles widgets from its own global palette, so set the same values
there or the editor and the stylesheet will drift apart.

**Elementor → hamburger menu → Site Settings → Global Colors:**

| Elementor slot | Set to |
|---|---|
| Primary | `#0B4A87` |
| Secondary | `#06274A` |
| Text | `#45566B` |
| Accent | `#2E7DD1` |

Then add these under **Site Settings → Custom CSS** if you want to override
Elementor's own defaults site-wide, or simply apply the classes below to
sections and widgets.

---

## 2. Typography

Font stack is Inter with a full system fallback, so nothing breaks if Inter
fails to load. To actually serve Inter, add it under **Site Settings → Global
Fonts**, or self-host it for better privacy and speed.

Headings use a fluid `clamp()` scale — they resize smoothly between mobile and
desktop with no breakpoints to maintain.

| Element | Token | Desktop size |
|---|---|---|
| H1 | `--rl-text-4xl` | up to 3.5rem |
| H2 | `--rl-text-3xl` | up to 2.75rem |
| H3 | `--rl-text-2xl` | up to 2rem |
| H4 | `--rl-text-xl` | up to 1.5rem |
| Body | `--rl-text-base` | 1rem / 1.65 line height |

---

## 3. Using the classes in Elementor

Every Elementor widget, column, and section has an **Advanced → CSS Classes**
field. Type the class name there (without a dot) and the styling applies.

### Sections
| Class | Effect |
|---|---|
| `rl-section` | Standard vertical rhythm (6rem top and bottom) |
| `rl-section rl-section--tight` | Reduced padding (4rem) |
| `rl-section rl-section--alt` | Pale blue background, for alternating bands |
| `rl-section rl-section--dark` | Deep navy background with light text |

### Buttons
Set an Elementor Button widget's CSS class to `rl-btn rl-btn--primary`,
`rl-btn rl-btn--secondary`, or `rl-btn rl-btn--ghost`.

### Components
| Class | Use |
|---|---|
| `rl-eyebrow` | Small uppercase label above a heading |
| `rl-lede` | Larger intro paragraph under a heading |
| `rl-grid rl-grid--products` | Auto-fitting product grid |
| `rl-grid rl-grid--features` | Auto-fitting feature grid |
| `rl-card` | Bordered card with hover lift |
| `rl-badge` | Pill label — add `--verified`, `--low`, or `--out` |
| `rl-spec-table` | Product specification table |
| `rl-table-scroll` | Wrap a wide table so it scrolls itself, not the page |
| `rl-notice` | Research-use-only notice block |
| `rl-notice rl-notice--bar` | Full-width dark notice strip for the header |
| `rl-trustbar` | Row of reassurance items under the hero |
| `rl-faq__item` / `rl-faq__q` / `rl-faq__a` | FAQ built on `<details>`, no JS |

The grids use `auto-fit`, so columns collapse on smaller screens without any
responsive settings in Elementor.

---

## 4. Homepage section order

Matches `docs/website-copy.md`:

1. Notice bar — `rl-notice--bar`
2. Hero — heading, sub-headline, two buttons
3. Trust bar — `rl-trustbar`
4. Why choose us — 4 × `rl-card` in `rl-grid--features`
5. Category grid — `rl-grid--products`
6. How ordering works — 3 numbered steps
7. Testing explainer — `rl-section--alt`
8. Compliance block — `rl-notice`
9. FAQ — `rl-faq__item` list
10. Closing CTA — `rl-section--dark`
11. Footer with the full disclaimer

---

## 5. Editing workflow

CSS changes go through git, not the WordPress admin:

1. Edit `wp-content/themes/hello-elementor-child/style.css`
2. Commit and push to `main`
3. GitHub Actions deploys it in about ten seconds
4. Hard-refresh (Ctrl+F5) to bypass cached CSS

Do **not** paste large amounts of CSS into Elementor's Custom CSS box — that
lives in the database, is invisible to version control, and will drift out of
sync with this file.

Remember that Elementor **page designs** are stored in the database, so they
are not version-controlled and do not move between environments with a deploy.
Use Elementor's Tools → Import/Export Kit for those.
