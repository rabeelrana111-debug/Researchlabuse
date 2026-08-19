---
title: "Formatting reference for articles"
description: "Every markdown element this site styles, shown rendered, so you can see what is available while writing."
pubDate: 2026-08-16
author: "Research Lab USA"
tags: ["guides", "site"]
---

This post exists as a reference. Every element below is styled by the site's
design system, so you can see what is available while writing — and it doubles
as a visual check that nothing has broken after a change.

Delete this post whenever it stops being useful.

## Headings

Use `##` for main sections and `###` for subsections. Skip `#` entirely — the
article title is already the page's only level-one heading, and adding another
confuses screen readers and search engines alike.

### This is a subsection

Text under a subsection sits closer to its heading than a new section does,
which is what gives the page its rhythm.

## Text formatting

Ordinary paragraph text, with **bold for emphasis**, *italics for terms or
titles*, `inline code` for filenames and values, and
[links to other pages](/about/).

## Lists

Unordered:

- First item
- Second item, which runs on a little longer to show how wrapped lines sit
  underneath the marker rather than beside it
- Third item

Ordered:

1. Prepare the sample
2. Record the starting conditions
3. Measure at fixed intervals

## Blockquotes

> Quoted material is set apart with a coloured rule and a tinted background, so
> it reads clearly as someone else's words rather than yours.

## Code

Inline `values` sit within a sentence. Fenced blocks handle longer passages and
scroll sideways on their own if a line is too long, rather than making the
whole page scroll:

```bash
npm run dev
```

## Tables

| Parameter | Value | Notes |
|---|---|---|
| Temperature | 21 °C | Ambient, uncontrolled |
| Duration | 45 min | Measured from first addition |
| Replicates | 3 | Independent preparations |

Wide tables can be wrapped in a `<div class="rl-table-scroll">` so they scroll
within their own box.

## Horizontal rules

Use `---` on its own line to separate major shifts in topic:

---

## Images

Images are automatically constrained to the article width and given rounded
corners:

```markdown
![Description of the image for screen readers](/images/example.jpg)
```

Put image files in the `public/` folder and reference them from the site root.
Always write real alt text — describe what the image shows, not that it is an
image.
