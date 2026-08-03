# Ribet

Website for the Ribet group at the National Center for Electron Microscopy within the Molecular Foundry at Lawrence Berkeley National Laboratory.

The group develops computational methods, experimental techniques, and hardware for electron microscopy, with research spanning cryogenic electron microscopy, computational microscopy and open-source software, and functional materials.

## Website content

- `index.md` — group overview
- `research.md` — research themes
- `team.md` — current group members and alumni
- `users.md` — Molecular Foundry User Program information and user highlights
- `publications.md` — publication list
- `open-source-code.md` — open-source electron microscopy software
- `funding.md` — current projects and funding
- `footer.md` — site-wide footer content
- `assets/` — images, logos, and other static assets
- `style.css` — custom styling for the MyST book theme
- `myst.yml` — site metadata, navigation, and build configuration

## Local development

The site is built with [MyST Markdown](https://mystmd.org/). Install the MyST command-line tools with Node.js 18 or newer:

```bash
npm install -g mystmd
```

Fetch the book theme, apply the site-specific theme customizations, and start the development server:

```bash
myst build
python3 scripts/patch_theme.py
myst start
```

The patch keeps top-level navigation sections expanded and replaces the default dialog search with the compact search field used by the site. Reapply it whenever `_build/` is deleted or the MyST theme is refreshed.

To create a static build:

```bash
myst build --html
```

The generated site is written to `_build/html/`. Build output and installed dependencies are excluded from version control.

## Updating the site

Edit the Markdown page associated with the section you want to change and place new images in the appropriate `assets/` subdirectory. Use relative image paths in Markdown, for example:

````md
```{image} assets/people/example.jpg
:alt: A concise description of the image
```
````

Navigation labels and page order are configured in `myst.yml`. Shared visual styles are defined in `style.css`.

## Deployment

Pushes to `main` trigger `.github/workflows/deploy.yml`. The workflow installs MyST, fetches and patches the book theme, builds the static site with the repository base URL, and publishes `_build/html/` to GitHub Pages.

GitHub Pages must be configured to use **GitHub Actions** as its deployment source under **Settings → Pages**.
