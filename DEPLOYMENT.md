# Deploying to SiteGround

Every push to `main` builds the Astro site and copies the generated HTML to
SiteGround. You can also run it on demand from the repository's **Actions** tab
(*Deploy to SiteGround* → **Run workflow**).

---

## ⚠️ Required after the move off WordPress

`SITEGROUND_REMOTE_PATH` still points at the old WordPress folder. The site is
now plain HTML served from the web root, so this must be updated or the deploy
will stop with an error.

**GitHub → Settings → Secrets and variables → Actions → `SITEGROUND_REMOTE_PATH`**

| | |
|---|---|
| Old value | `/home/customer/www/researchlabusa.com/public_html/wp-content` |
| New value | `/home/customer/www/researchlabusa.com/public_html` |

In other words: delete the trailing `/wp-content`. To confirm the exact path,
run this over SSH:

```
ssh -i <your-key> u3171-6mw78ij23p20@ssh.researchlabusa.com -p18765 "cd ~/www/researchlabusa.com/public_html && pwd"
```

The workflow checks for this specific mistake and tells you if the secret still
points inside `wp-content`.

---

## The five secrets

| Secret | Value |
|---|---|
| `SITEGROUND_SSH_HOST` | `ssh.researchlabusa.com` |
| `SITEGROUND_SSH_USER` | your SiteGround SSH username |
| `SITEGROUND_SSH_PORT` | `18765` |
| `SITEGROUND_SSH_KEY` | the **private** key, passphrase-free |
| `SITEGROUND_REMOTE_PATH` | the web root — see above |

The key must have **no passphrase**: GitHub Actions cannot type one.
SiteGround's own key generator forces a passphrase, so generate the key
locally and import only the public half into SiteGround:

```
ssh-keygen -t ed25519 -f %USERPROFILE%\.ssh\siteground_deploy
```

Press Enter twice when asked for a passphrase. Then:

- `siteground_deploy.pub` (public) → SiteGround, **Site Tools → Devs → SSH Keys Manager → Import**
- `siteground_deploy` (private) → GitHub secret `SITEGROUND_SSH_KEY`

To remove a passphrase from a key you already have:
`ssh-keygen -p -f <keyfile> -N ""`

---

## What the pipeline does

1. Installs dependencies with `npm ci`
2. Builds the site with `npm run build` into `dist/`
3. Refuses to continue if `dist/index.html` is missing, so a broken build
   cannot blank the live site
4. Validates the secrets and the SSH key, naming the specific problem if one is
   wrong
5. Connects to SiteGround, retrying with backoff on transient failures
6. Copies `dist/` to the web root with rsync

A failed build never touches the server — the previous version stays live.

### Deleting stale files

By default the deploy adds and updates only; it never deletes. A page removed
from the repo therefore stays reachable on the server.

To make the server mirror the repo exactly, set `DELETE_STALE: "true"` in
`.github/workflows/deploy.yml`. Check first that nothing else lives in your web
root, since anything not produced by the build will be removed. `.well-known`
is always protected, as deleting it can break SSL certificate renewal.

---

## Troubleshooting

The workflow diagnoses the common problems itself and names them in the log.

- **`SITEGROUND_REMOTE_PATH still points at wp-content`** — apply the change at
  the top of this document.
- **`The private key is passphrase-protected`** — strip the passphrase with
  `ssh-keygen -p -f <keyfile> -N ""` and update the secret.
- **`SITEGROUND_SSH_KEY contains a PUBLIC key`** — the halves are swapped. The
  private key goes in GitHub; the public key goes in SiteGround.
- **`Connection timed out`** — SiteGround's brute-force protection is
  throttling the runner's IP. The workflow retries automatically; if it still
  fails, wait a few minutes and re-run, then check **Site Tools → Security →
  Blocked IPs**.
- **`Permission denied (publickey)`** — the key in the secret does not match
  one registered in SiteGround. The log prints the public half of the key it
  loaded; compare that against the SSH Keys Manager.
- **Site looks stale after deploying** — hard-refresh (Ctrl+F5). HTML is set to
  no-cache in `public/.htaccess`, but browsers still hold onto CSS, which is
  fine because Astro fingerprints those filenames.
