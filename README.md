# Energy Brief OS

Apple product-page-inspired daily briefing site for new-energy policy, trading, pricing, and project signals.

## Local build

```powershell
python scripts/generate_daily.py
```

Generated files:

- `index.html`: latest issue
- `daily/YYYY-MM-DD.html`: individual daily issue
- `archive.html`: historical archive

## Publish

This repository is designed for GitHub Pages. The included workflow builds the static pages and uploads the site artifact.

Recommended repository name: `energy-brief-os`.
