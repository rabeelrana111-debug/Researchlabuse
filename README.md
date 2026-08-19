# Research Lab USA

Static website for **https://researchlabusa.com**, built with
[Astro](https://astro.build) and deployed automatically to SiteGround.

Blog posts are markdown files. Push to `main` and the site rebuilds and
publishes itself in about a minute — no database, no admin login, nothing on
the server to keep patched.

## Quick start

```bash
npm install
npm run dev      # http://localhost:4321
```

## Layout

```
src/
  content/blog/      Blog posts (markdown) — one file per article
  pages/             Routes: index, about, contact, blog, 404
  layouts/           Page shell and article template
  components/        Header, footer, post card, meta tags
  styles/global.css  Design system — all colours and spacing live here
public/              Files copied as-is: favicon, robots.txt, .htaccess
.github/workflows/   Build and deploy pipeline
```

## Publishing an article

Add a markdown file to `src/content/blog/` with front matter, then push:

```markdown
---
title: "Article title"
description: "Shown on cards and in search results."
pubDate: 2026-08-19
tags: ["guides"]
---
```

The file name becomes the URL. Full instructions, design tokens, and the
contact-form setup are in **[docs/SITE-GUIDE.md](./docs/SITE-GUIDE.md)**;
hosting and deployment details are in **[DEPLOYMENT.md](./DEPLOYMENT.md)**.
