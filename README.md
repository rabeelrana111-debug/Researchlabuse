# Research Lab USA

WordPress custom code for **https://researchlabusa.com/**, hosted on SiteGround.

Pushing to the `main` branch automatically deploys the contents of
`wp-content/` to the SiteGround server via GitHub Actions (rsync over SSH).

## Repository layout

```
wp-content/
  themes/
    hello-elementor-child/   Child theme — your custom CSS and PHP
  plugins/                   Custom / version-controlled plugins
  mu-plugins/                Must-use plugins (optional)
.github/workflows/
  deploy.yml                 Auto-deploy workflow (push to main → SiteGround)
.deployignore                Files rsync skips when deploying
```

The site runs **Hello Elementor + Elementor Pro**. Those are installed and
updated through the WordPress admin and are deliberately kept out of this repo;
your customisations go in the child theme. Note that Elementor page designs are
stored in the database, so they are not moved by this pipeline — see
[DEPLOYMENT.md](./DEPLOYMENT.md).

## Getting started

The deploy pipeline needs a one-time setup (SiteGround SSH key + five GitHub
secrets). Full instructions are in **[DEPLOYMENT.md](./DEPLOYMENT.md)**.

Only your own code lives here — WordPress core, `wp-config.php`, the database,
and `wp-content/uploads/` stay on the server and are excluded from git.
