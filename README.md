# Ribet

Website for the Ribet group at the National Center for Electron Microscopy within the Molecular Foundry at Lawrence Berkeley National Laboratory.

## Building the site

The site is built with [MyST Markdown](https://mystmd.org/):

```bash
npm install -g mystmd   # or: pip install mystmd
myst build
python3 scripts/patch_theme.py
myst start              # local development server
myst build --html       # static site in _build/html
```

Reapply `scripts/patch_theme.py` whenever `_build/` is deleted or the MyST theme is refreshed.

## Deployment

Pushes to `main` trigger `.github/workflows/deploy.yml`, which builds the site and publishes it to GitHub Pages. GitHub Pages must use **Settings → Pages → Source → GitHub Actions**.
