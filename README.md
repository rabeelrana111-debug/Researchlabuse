# Research Lab USA

Website for **https://researchlabusa.com**, hosted on SiteGround.

Pushing to `main` publishes the site automatically. Nothing else is required —
no build step, no framework, no server-side code.

## How it works

Put your files in **`site/`**. Whatever is in there is published to the web
root exactly as-is:

```
site/index.html   ->  https://researchlabusa.com/
site/about.html   ->  https://researchlabusa.com/about.html
site/styles.css   ->  https://researchlabusa.com/styles.css
```

Edit, commit, push. It is live in under a minute.

`site/index.html` currently holds a placeholder — replace it and start
building.

## Preview locally

Open `site/index.html` in a browser, or serve the folder so root-relative
paths behave exactly as they will in production:

```bash
python3 -m http.server -d site 8000   # then open http://localhost:8000
```

## Adding a build tool later

The pipeline handles both shapes without any edits:

| Repo state | What gets published |
|---|---|
| No `package.json` | `site/` as-is |
| `package.json` present | runs `npm ci && npm run build`, publishes `dist/` |

So if you later adopt a framework, add it in the normal way and the deploy
switches over on its own.

## Deployment

Credentials, the required GitHub secrets, and troubleshooting are documented in
**[DEPLOYMENT.md](./DEPLOYMENT.md)**.
