# Fastly — App Landing Page

## Project Overview

Marketing and support website for **Fastly**, a digital fasting iOS app. Built with Jekyll and deployed to GitHub Pages via GitHub Actions. The site serves as the App Store support URL and public-facing landing page.

Hosted at: `https://digital-fasting.github.io/fastly-app/`

## Tech Stack

- **Static site generator**: Jekyll 4.4 (Ruby)
- **Styling**: SCSS (`_sass/`) compiled through `main.scss`
- **Icons**: Font Awesome (via CDN in `_includes/head.html`)
- **Deployment**: GitHub Actions → GitHub Pages (push to `main` triggers deploy)

## Project Structure

```
_config.yml          # All site content, app metadata, theme colors
_layouts/
  default.html       # Main landing page layout (hero, features, footer)
  page.html          # Sub-page layout (privacy policy, changelog)
_includes/
  head.html          # <head> tag, meta, Font Awesome CDN
  header.html        # Top navigation bar with app icon
  features.html      # Feature grid driven by _config.yml features list
  footer.html        # Support section, social icons, footer links
  screencontent.html  # App screenshot/video carousel
  appstoreimages.html # App Store badge SVGs
_sass/
  base.scss          # Variables, resets, typography, global link styles
  layout.scss        # All layout: grid, header, hero, features, footer, support
  github-markdown.scss # Markdown body styles for sub-pages
_pages/
  changelog.md       # App changelog (rendered as sub-page)
privacy.html         # Privacy policy page
index.html           # Landing page entry point (uses default layout)
main.scss            # SCSS entrypoint — maps _config.yml values to SCSS variables
```

## Key Conventions

### Content is config-driven

Almost all visible text, features, links, and theme colors live in `_config.yml`. When changing copy, features, or colors, edit the config — not the HTML templates.

### Theme colors

All color values flow from `_config.yml` → `main.scss` (as SCSS variables) → `_sass/*.scss`. Never hardcode colors in layout files; add a new config key and variable instead.

### Footer support section

The footer includes a prominent email-based support section required by App Store review guidelines. The support email is configured via `email_address` in `_config.yml`. This section must remain visible and functional — it is the App Store Connect support URL destination.

### Adding features

Add entries to the `features` list in `_config.yml` with `title`, `description`, and `fontawesome_icon_name`. The feature grid in `_includes/features.html` renders them automatically.

### Sub-pages

Create Markdown files in `_pages/` with layout `page`. They use `_layouts/page.html` which renders content inside a `.markdown-body` styled container.

## Local Development

```sh
bundle install
bundle exec jekyll serve
```

Site will be available at `http://localhost:4000`.

## Deployment

Push to `main` triggers `.github/workflows/jekyll.yml` which builds and deploys to GitHub Pages automatically. No manual deploy steps needed.
