# Site Guide — Research Lab USA

Everything you need to run, write for, and restyle this site.

The site is built with [Astro](https://astro.build). Markdown files become HTML
pages at build time, and GitHub Actions publishes the result to SiteGround.
There is no database, no admin login, and nothing on the server to keep
patched.

---

## 1. Running it on your computer

You need [Node.js](https://nodejs.org) 20 or newer installed once.

```bash
npm install     # first time only
npm run dev     # start the local preview
```

Open the address it prints (usually `http://localhost:4321`). Pages reload as
you save.

| Command | What it does |
|---|---|
| `npm run dev` | Local preview with live reload |
| `npm run build` | Build the site into `dist/` |
| `npm run preview` | Serve the built site, exactly as visitors will get it |

---

## 2. Publishing an article

1. Create a file in `src/content/blog/`, for example `my-first-post.md`.
   **The file name becomes the URL** — `my-first-post.md` publishes at
   `/blog/my-first-post/`.
2. Start it with front matter:

```markdown
---
title: "The title shown on the page"
description: "One or two sentences, used on cards and in search results."
pubDate: 2026-08-19
author: "Research Lab USA"
tags: ["guides"]
draft: false
---

Your article starts here.
```

3. Write the body in markdown.
4. Commit and push to `main`. It is live in about a minute.

**Required fields:** `title`, `description`, `pubDate`.
**Optional:** `author`, `tags`, `draft` — all have defaults.

Set `draft: true` to keep a post out of the published site while you work on
it. It still appears in `npm run dev`.

The schema is enforced at build time, so a malformed date or a missing title
fails the build rather than publishing something broken. **If a build fails,
the live site is left exactly as it was.**

`src/content/blog/formatting-reference.md` shows every markdown element the
site styles. Delete it once you no longer need it.

---

## 3. Changing the design

All colours, fonts and spacing are CSS custom properties at the top of
`src/styles/global.css`. Change a value there and it updates site-wide.

| Token | Value | Used for |
|---|---|---|
| `--rl-blue-700` | `#0B4A87` | Primary — buttons, links |
| `--rl-blue-900` | `#06274A` | Footer, dark sections |
| `--rl-blue-50` | `#F1F7FD` | Alternating section backgrounds |
| `--rl-ink` | `#0F172A` | Headings |
| `--rl-body` | `#45566B` | Body text |

To change the whole site's accent colour, edit `--rl-blue-700` alone.

Primary blue on white, and white on primary blue, both meet WCAG AA contrast
for normal text. If you lighten the palette, re-check contrast — `--rl-muted`
on white is the first pairing that will fail.

### Page structure

| File | Purpose |
|---|---|
| `src/layouts/BaseLayout.astro` | Page shell: head, header, footer |
| `src/layouts/PostLayout.astro` | Article pages |
| `src/components/Header.astro` | Navigation — edit the `links` array to change menu items |
| `src/components/Footer.astro` | Footer content |
| `src/pages/index.astro` | Homepage |
| `src/pages/about.astro` | About page |
| `src/pages/contact.astro` | Contact page |

To add a page, drop a `.astro` file into `src/pages/`. A file at
`src/pages/services.astro` is published at `/services/`.

---

## 4. The contact form needs a service

A static site has no server-side code, so it cannot process form submissions by
itself. The form in `src/pages/contact.astro` currently points at a placeholder.

Pick a form service — [Formspree](https://formspree.io),
[Web3Forms](https://web3forms.com) and [Basin](https://usebasin.com) all have
free tiers — then replace the `action` URL with the endpoint they give you:

```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
```

Then delete the yellow warning notice above the form.

If you would rather not use a form at all, delete the `<form>` block and leave
the email address.

---

## 5. Placeholders to fill in

Search the project for `[` to find them all:

- `src/components/Footer.astro` — city/state, phone number
- `src/pages/about.astro` — the "Who we are" section
- `src/pages/contact.astro` — phone number, street address
- Email addresses currently read `hello@researchlabusa.com`

---

## 6. What gets generated automatically

- **Sitemap** at `/sitemap-index.xml`, listing every page
- **RSS feed** at `/rss.xml`, updated with each post
- **Social preview tags** on every page, using `public/social-card.svg`
- **Canonical URLs**, so search engines index one address per page

These come from the `site` value in `astro.config.mjs`. If the domain ever
changes, update it there or every generated link will point at the old host.

---

## 7. Deploying

Push to `main`. GitHub Actions builds the site and copies `dist/` to the web
root. Watch progress in the repository's **Actions** tab.

The workflow refuses to deploy if the build produces no `index.html`, so a
broken build cannot blank the live site.

### Removing deleted pages from the server

By default the deploy only adds and updates files — it never deletes. That is
safe, but it means a post you delete from the repo stays reachable on the
server.

To make the live site mirror the repo exactly, set `DELETE_STALE: "true"` in
`.github/workflows/deploy.yml`. Before switching it on, make sure nothing else
lives in your web root, because anything not produced by the build will be
removed. `.well-known` is always protected, since deleting it can break SSL
certificate renewal.

See `DEPLOYMENT.md` for hosting credentials and troubleshooting.
