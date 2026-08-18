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

### Step 1 — Create a passphrase-free key and register it with SiteGround

> **Important:** SiteGround's own key generator *requires* a passphrase, and
> GitHub Actions cannot type a passphrase — a passphrase-protected key fails
> with `incorrect passphrase supplied to decrypt private key`. So generate the
> key locally without one and import its public half into SiteGround.

1. On your computer, generate a key pair with an empty passphrase (`-N ""`):
   ```
   ssh-keygen -t ed25519 -f %USERPROFILE%\.ssh\siteground_deploy -N ""
   ```
   (macOS/Linux: `ssh-keygen -t ed25519 -f ~/.ssh/siteground_deploy -N ""`)

   This writes two files: `siteground_deploy` (**private**) and
   `siteground_deploy.pub` (**public**).

2. Print the **public** key and copy the whole line:
   ```
   type %USERPROFILE%\.ssh\siteground_deploy.pub
   ```

3. In SiteGround: **Site Tools → Devs → SSH Keys Manager → Import** (or *Add
   existing key*) → paste the **public** key → save.

4. Keep the **private** key (`siteground_deploy`, no `.pub`) for Step 3 — it
   goes into the GitHub secret, and nowhere else.

> **Already generated a key in SiteGround?** You don't have to start over —
> just strip the passphrase off it. Save the private key to a file, then run
> `ssh-keygen -p -f <keyfile> -N ""` and enter the existing passphrase when
> prompted. The public key stays the same, so it remains registered in
> SiteGround; only the private key file changes.

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

The workflow diagnoses the common setup mistakes itself and names them in the
Actions log. The three you're most likely to hit:

- **`The private key is passphrase-protected`** — SiteGround generated the key
  and forced a passphrase on it. Strip it with `ssh-keygen -p -f <keyfile> -N ""`
  (see the note in Step 1), then update the secret.
- **`SITEGROUND_SSH_KEY contains a PUBLIC key`** — the halves are swapped. The
  private key (the multi-line `-----BEGIN OPENSSH PRIVATE KEY-----` block) goes
  in the GitHub secret; the public key (`ssh-ed25519 AAAA...`) goes in SiteGround.
- **`Permission denied (publickey)`** — the private key in `SITEGROUND_SSH_KEY`
  doesn't match a key registered in SiteGround, or the user/host is wrong.
  Re-copy the full key including the BEGIN/END lines. The workflow prints the
  public half of whatever key it loaded — compare that line against the key
  listed in SiteGround's SSH Keys Manager.
- **Connection times out** — check `SITEGROUND_SSH_PORT` (usually `18765`, not
  `22`) and that SSH is enabled in Site Tools.
- **Files deploy but the site doesn't change** — confirm `SITEGROUND_REMOTE_PATH`
  points at the live `public_html/wp-content`, and that the active theme in
  **WP Admin → Appearance → Themes** is the one you're deploying.
