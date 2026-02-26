# CLAUDE.md

## Project Overview

This is a personal documentation site built with [MkDocs](https://www.mkdocs.org/) using the [Material theme](https://squidfunk.github.io/mkdocs-material/). It is deployed via GitHub Actions to GitHub Pages.

## Tech Stack

- **Generator**: MkDocs
- **Theme**: Material for MkDocs
- **Deployment**: GitHub Actions → `mkdocs gh-deploy` on push to `main`

## Directory Structure

```
docs/               # MkDocs source root (all .md files go here)
├── index.md        # Homepage
├── blog/           # Blog section (MkDocs blog plugin)
│   └── index.md
├── docs/           # "Docs" tab content
│   ├── notes.md
│   ├── webserver.md
│   └── prompts.md
└── cisco/          # "Cisco" tab content
    ├── ccna.md
    └── commands.md
mkdocs.yml          # MkDocs configuration (nav, theme, plugins)
.github/workflows/  # CI/CD — deploys on push to main
```

## Navigation

Navigation is defined explicitly in `mkdocs.yml` under the `nav:` key. When adding new pages:
1. Create the `.md` file under `docs/`
2. Add an entry to `nav:` in `mkdocs.yml`

Top-level nav entries become tabs (Material `navigation.tabs` feature).

## Running Locally

```bash
pip install mkdocs-material
mkdocs serve
```

Site will be available at `http://127.0.0.1:8000`.

## Deployment

Pushing to `main` triggers the GitHub Actions workflow (`.github/workflows/ci.yml`), which runs `mkdocs gh-deploy --force` to publish to GitHub Pages.

## Conventions

- Keep section index pages (`index.md`) minimal — use subsection pages for actual content
- Code blocks use fenced triple backticks with language hints where applicable
- Commands are wrapped in backticks inline or in fenced code blocks
