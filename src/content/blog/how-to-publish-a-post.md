---
title: "How to publish a new post"
description: "The complete workflow for adding an article to this site, from creating the file to seeing it live."
pubDate: 2026-08-17
author: "Research Lab USA"
tags: ["guides", "site"]
---

This site is built with Astro and deployed automatically. Publishing an
article means adding one markdown file and pushing it — there is no admin
panel to log into.

## The short version

1. Create a file in `src/content/blog/` ending in `.md`
2. Give it front matter (see below)
3. Write the article in markdown
4. Commit and push to `main`
5. Wait about a minute — it builds and deploys itself

## The file name becomes the URL

A file at `src/content/blog/my-new-article.md` is published at
`/blog/my-new-article/`. Use lowercase words separated by hyphens, and keep it
short and descriptive. Changing the file name later changes the URL and breaks
any existing links to it, so it is worth getting right the first time.

## Front matter

Every post starts with a block of metadata between `---` markers:

```markdown
---
title: "The title shown on the page"
description: "One or two sentences. Used on cards, in search results and in social previews."
pubDate: 2026-08-18
author: "Research Lab USA"
tags: ["guides"]
draft: false
---
```

`title`, `description` and `pubDate` are required. `author`, `tags` and `draft`
are optional and have sensible defaults.

The `description` matters more than it looks — it is what appears under your
link in Google results and on the blog index, so write it for a reader
deciding whether to click.

## Drafts

Set `draft: true` and the post is visible while developing but excluded from
the built site. Remove the line or set it to `false` when you are ready to
publish.

## Checking your work before publishing

Run the site locally to preview changes:

```bash
npm install   # only needed the first time
npm run dev
```

Then open the address it prints, usually `http://localhost:4321`. The page
reloads as you save.

## What happens after you push

Pushing to `main` triggers a build. If the build succeeds, the finished HTML is
copied to the web server. If it fails — a malformed date, a missing required
field — the deploy stops and the live site is left exactly as it was. A broken
post cannot take the site down.
