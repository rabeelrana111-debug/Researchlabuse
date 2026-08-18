# Deploying to SiteGround (auto-deploy on every push)

This repo auto-deploys your WordPress custom code (`wp-content/`) to your
SiteGround hosting for **https://researchlabusa.com/** every time you push to
the `main` branch, using GitHub Actions + rsync over SSH.

The deploy is **non-destructive**: it uploads and updates the files tracked in
this repo but never deletes anything already on your live server. Your
database, uploads, WordPress core, and admin-installed plugins are untouched.

---

## One-time setup

You do this once. After that, every `git push` to `main` deploys automatically.

### Step 1 — Turn on SSH access in SiteGround

1. Log in to SiteGround and open **Site Tools** for `researchlabusa.com`.
2. Go to **Devs → SSH Keys Manager**.
3. Under **Generate New Key**, enter a name (e.g. `github-deploy`), leave the
   passphrase empty (CI can't type a passphrase), and click **Create**.
4. In the key list, use **Actions → Private Key** to reveal and **copy the full
   private key** (from `-----BEGIN ... -----` to `-----END ... -----`). Keep it
   handy for Step 3.
   - *Alternative:* if you'd rather generate the key yourself, run
     `ssh-keygen -t ed25519 -f siteground_deploy -N ""` locally and paste the
     **public** key (`siteground_deploy.pub`) into SiteGround's *Import Key* box.
     You'll then use the private key you generated in Step 3.

### Step 2 — Collect your SSH connection details

In the same **SSH Keys Manager / SSH access** panel, note:

| What | Where to find it | Example |
|------|------------------|---------|
| **Hostname** | SSH access details (server IP or host) | `12.34.56.78` |
| **Username** | SSH access details | `u1234-abcd` |
| **Port** | SSH access details (SiteGround is **not** 22) | `18765` |
| **Remote path** | File Manager address bar for `wp-content` | `/home/customer/www/researchlabusa.com/public_html/wp-content` |

> To confirm the remote path, open **Site Tools → File Manager**, browse to
> `public_html/wp-content`, and copy the full path shown. On most SiteGround
> accounts it looks like `/home/customer/www/researchlabusa.com/public_html/wp-content`.

### Step 3 — Add the secrets to GitHub

In this GitHub repo: **Settings → Secrets and variables → Actions → New
repository secret**. Add these five secrets (names must match exactly):

| Secret name | Value |
|-------------|-------|
| `SITEGROUND_SSH_HOST` | the hostname/IP from Step 2 |
| `SITEGROUND_SSH_USER` | the username from Step 2 |
| `SITEGROUND_SSH_PORT` | the port from Step 2 (e.g. `18765`) |
| `SITEGROUND_SSH_KEY` | the **entire private key** from Step 1 |
| `SITEGROUND_REMOTE_PATH` | the `wp-content` path from Step 2 |

### Step 4 — Deploy

Push to `main` (or run the workflow manually from the **Actions** tab →
*Deploy to SiteGround* → **Run workflow**). Watch the run in the **Actions**
tab. The "Verify SSH connection" step prints `SSH OK` when credentials are
correct; the rsync step lists every file it transfers.

---

## How it maps

```
This repo                          SiteGround server
─────────────────────────────     ─────────────────────────────────────────────
wp-content/themes/researchlabusa/  →  <REMOTE_PATH>/themes/researchlabusa/
wp-content/plugins/<your-plugin>/  →  <REMOTE_PATH>/plugins/<your-plugin>/
wp-content/mu-plugins/<file>.php   →  <REMOTE_PATH>/mu-plugins/<file>.php
```

Anything under `wp-content/uploads/`, `cache/`, etc. is skipped — see
`.deployignore`.

---

## What to put in this repo (and what not to)

**Do version-control:** your custom theme(s), your custom plugins, must-use
plugins — your own code.

**Do NOT version-control** (already excluded via `.gitignore`): WordPress core,
`wp-config.php`, the database, `wp-content/uploads/`, and third-party plugins
you install through the WP admin (those live on the server and update
themselves).

If your live site already uses a theme with a **different name**, either rename
this `wp-content/themes/researchlabusa/` folder to match it, or delete this
starter folder and add your real theme folder instead. The workflow deploys
whatever theme/plugin folders exist under `wp-content/`.

---

## Optional: exact mirroring with `--delete`

By default nothing is ever deleted on the server. Once you're confident the
repo holds the authoritative copy of a specific theme, you can make that one
folder mirror exactly (so files you delete in git also get removed on the
server). Edit `.github/workflows/deploy.yml` and change the rsync source/target
to that folder and add `--delete`, for example:

```yaml
rsync -rlvz --delete --no-perms --no-owner --no-group \
  -e "ssh -i ~/.ssh/deploy_key -p ${{ secrets.SITEGROUND_SSH_PORT }}" \
  wp-content/themes/researchlabusa/ \
  "${{ secrets.SITEGROUND_SSH_USER }}@${{ secrets.SITEGROUND_SSH_HOST }}:${{ secrets.SITEGROUND_REMOTE_PATH }}/themes/researchlabusa/"
```

Scope `--delete` to a single theme/plugin folder — never the whole
`wp-content/` — so it can't touch uploads or plugins that aren't in the repo.

---

## Troubleshooting

- **`Permission denied (publickey)`** — the private key in `SITEGROUND_SSH_KEY`
  doesn't match a key registered in SiteGround, or the user/host is wrong.
  Re-copy the full key including the BEGIN/END lines.
- **Connection times out** — check `SITEGROUND_SSH_PORT` (usually `18765`, not
  `22`) and that SSH is enabled in Site Tools.
- **Files deploy but the site doesn't change** — confirm `SITEGROUND_REMOTE_PATH`
  points at the live `public_html/wp-content`, and that the active theme in
  **WP Admin → Appearance → Themes** is the one you're deploying.
