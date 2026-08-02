# Nanobeam Diffraction & 4D-STEM (M&M 2026 Short Course X11)

Companion website for the Microscopy & Microanalysis 2026 Sunday short course
**X11: Nanobeam Diffraction and 4D-STEM Analysis of Crystalline and Disordered
Materials** (Sunday, August 2, 2026 · Baird Center, Milwaukee, WI).

Organizers: Colin Ophus (Stanford), Stephanie Ribet (LBNL), Ian MacLaren (Glasgow).

## Building the site

The site is built with [MyST Markdown](https://mystmd.org/):

```bash
npm install -g mystmd   # or: pip install mystmd
myst start              # local dev server with live reload
myst build --html       # static site in _build/html
```

## Deployment

Pushes to `main` trigger the GitHub Actions workflow in
`.github/workflows/deploy.yml`, which builds the site and publishes it to
GitHub Pages. One-time setup on GitHub: repository **Settings → Pages →
Source → GitHub Actions**.

## Layout

- `index.md`: landing page
- `agenda.md`: course schedule
- `topics/`: one page per module (teaching notes, Colab links, references)
- `resources.md`: collected reading list
- `assets/`: cover images and logos
- `style.css`: theme overrides for the MyST book-theme
