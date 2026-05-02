# Le Grand Jeu — Books

Print-ready A5 pocket books derived from play reports published at [legrandjeu.net](https://legrandjeu.net), and from workshop notes held in the LGJ archive.

The project is split into two companion volumes, sharing the same visual language:

## Book 1 — *Scenarios*

> `book1-scenarios/`

Five play reports from 2020–2021, each with its premise, setup, players, key moments, player inventions, and debrief:

- **PermaCoin** — land regeneration and a coin that funds itself
- **Pandemic** — COVID-XX: contagion, self-sufficiency, uneven safety
- **Down Under** — a dry valley and a coin at four-times leverage
- **Three Cities** (SOU) — what 23 children built in three hours
- **Strettonia** (Messina) — a port city between two seas

Plus an "About Le Grand Jeu" intro and an Appendix of all inventions, indexed by theme.

Page count: ≈ 62 pages.

## Book 2 — *Science &amp; Society at the Table*

> `book2-experiments/` *(planned)*

Two longer-form scenarios that deserved their own volume:

- **Eurofusion — Power to the People** — energy futures, public debate, research as play
- **SPES** — a serial scenario spanning many sessions and years

## How to use

Each book has its own folder with:

```
book1-scenarios/
├── book.css             ← shared design system (copy to book2 when needed)
├── build-book.py        ← assembles chapter fragments into book.html
├── ch00-front.html      ← front matter
├── ch01-about.html      ← About LGJ
├── ch02-*.html ... ch06-*.html  ← scenario chapters
├── ch99-appendix.html   ← inventions appendix
├── book.html            ← generated output
└── assets/              ← images, one subfolder per chapter
```

### Build a book

```bash
cd book1-scenarios
python3 build-book.py             # concatenates chapters → book.html
weasyprint book.html book.pdf     # renders to A5 PDF
```

### Download assets (first time only)

Each book has its own `download-assets.sh` in the `assets/` folder (or at the book root) that fetches images from `legrandjeu.net` into the right places. Run once before the first render.

### Print

Open `book.html` in a browser, print to PDF at A5, no margins, with "background graphics" on. Alternatively use `weasyprint book.html book.pdf` for identical results.

## Design notes

- **Typography** — system-ui sans for headings and labels, serif for body and epigraphs
- **Accent colour** — ochre (`#c97a1a`), neutral enough for B&W print
- **Monogram** — three overlapping rhombuses on the half-title and chapter covers, with scenario-specific accent triangles
- **Invention cards** — every player-invented mechanic appears with an ochre top rule, attribution, body prose, and a formalised "Mechanic:" line that other masters can lift into their own games
- **Running headers** — chapter name on the verso, "Le Grand Jeu" on the recto. Suppressed on blank verso pages and first pages

## Licence

All content licensed **CC BY-NC 4.0**, matching the source posts on legrandjeu.net. Design and HTML/CSS are part of `freddbomba/legrandjeu-rulebook`, CC BY-NC-SA 4.0.

---

*Federico Bonelli · April 2026*
