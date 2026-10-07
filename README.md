# Pirenily — A Personal Archive

Pirenily is my personal portfolio: design work, side projects, coding, and the odd creative experiment, all in one dark, quiet archive. Live at [pirenily.com](https://pirenily.com).

## A short history of this repo

**2021–2024: someone else's template.** The repo started life as [koyeb/example-flask](https://github.com/koyeb/example-flask), Koyeb's starter Flask app. The first stretch of history isn't mine: an initial commit in November 2021, a `$PORT` fix in the Procfile, CI setup in 2023, and then a long tail of "Automated empty commit to keep repo active" commits from a GitHub Action. That's why the folder is still called `example-flask`.

**December 2024: my own website.** I forked the template on 8 December 2024 for my CS50 final project. The first commit is literally called "my own website", and the same day is a frantic pile of `center`, `center`, `center`, `final`, `finalize`, `final touches`. That version had the Design / Play split, the AFVS p5.js sketches, and the first hand-drawn visuals.

**July 2025: the summer rebuild.** A few days of mobile layout fights (`help me with the dimensions huhu`, `tf`, `j v tr`, `how to have less commit huhu`, `im sleeping`, `swear last time`). This is when the site got its navigation, more sub-pages, preview images, and actually worked on a phone.

**October 2025 – January 2026: sophomore year.** A run of commits as `aidenva` restyled the Play page: new fonts, tabs that hide until chosen, the randomized gallery layout, GIFs, and new photos. Then T4SG × 2ft, the CS1710 Unicode essay, and AM111 joined as project case studies.

**August 2026: cleaning house.** CommonSpirit Health, a batch of coding projects, a password gate for client work, and the first real refactor: image paths moved behind a Jinja `img()` helper and galleries started generating themselves from folder contents.

**October 2026: the case-study era.** Galleries merged into one template, every case study moved onto a shared layout with a glowing progress rail, and the Design page got its Selected / Brand / UI/UX / All filters. Also: HackHarvard and Merch case studies, hover pop-ups, a full-screen phone menu, the travel globe and flip card on About, and the leftover Koyeb CI workflows finally deleted.

## Architecture, briefly

A small Flask app (`app.py`) serves Jinja2 templates. No database and no build step: just HTML, CSS, and vanilla JavaScript. Pages extend a shared `layout.html`; images live under `static/asset/images/` and are referenced through helpers instead of hardcoded paths. Static assets are cache-busted with a version string in `app.py`.

- **Home**: landing page, a "finder" search bar that routes keywords to pages, and a Projects grid with Code / UI-UX tabs
- **Design**: club, commission, and UI/UX case studies
- **Play**: personal, non-commissioned work
- **About**: bio, photography, contact

## Running it locally

Requires Python 3.12 (pinned Flask 2.2).

```bash
git clone https://github.com/tuechile/pirenily.git
cd pirenily
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

Then open `http://127.0.0.1:5000`.

## Deployment

Hosted on [Koyeb](https://www.koyeb.com). The service is linked to this repo, so pushing to `main` redeploys automatically, and a custom domain points at it.
