# The Spinner Foundation — Website Handoff

A four-page marketing site for The Spinner Foundation, a family-run charitable
foundation. Static HTML + a single shared stylesheet. Fully responsive
(desktop + mobile) with no build step.

---

## Quick start

Open any `.html` file in a browser, or serve the folder:

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

No framework, no bundler. The only external dependencies are Google Fonts
(loaded via `@import` in `assets/styles.css`).

---

## File structure

```
spinner-foundation-handoff/
├── index.html              Home
├── causes.html             Causes & Recipients (directory)
├── stories.html            Stories (long-form)
├── about.html              About the Family
├── brand-guide.html        Visual design-system reference (colors, type, components)
├── spinner-foundation.css  Consolidated stylesheet (core + all page components)
├── README.md               This file
└── assets/
    ├── styles.css          CORE design system (tokens, layout, components, mobile)
    ├── wordmark-light.png   Stacked wordmark — for light/cream backgrounds
    ├── wordmark-dark.png    Stacked wordmark — cream, for dark backgrounds
    ├── favicon.png          Crimson "V" on cream square
    ├── mark-seal.png        Transparent "V" stamp (footer sign-off)
    ├── mark-light/dark.png  Circular V monogram variants
    └── photos/              Photography library (.jpg / .png)
```

### How the CSS is wired

- **`assets/styles.css`** is the source of truth for the design system: tokens,
  typography, layout, nav, hero, buttons, footer, social row, seal, and all
  global responsive (`@media`) rules. Every page links it.
- **Page-specific components** (directory rows, story rows + TOC, team grid,
  scrapbook gallery, CTA bands) live in a `<style>` block in the `<head>` of
  each page. They use unique class names, so there are no collisions.
- **`spinner-foundation.css`** is a convenience file that concatenates the core
  stylesheet + every page's component styles into one, for reference or if you
  prefer a single external file. (The pages themselves do **not** load it.)

---

## Branding

**Typography** — Cormorant Garamond (display / serif) + Inter (body / sans),
loaded from Google Fonts.

**Color tokens** (defined on `:root` in `styles.css`):

| Token | Value | Role |
|---|---|---|
| `--paper` | `oklch(.975 .008 75)` | Page background (warm cream) |
| `--paper-2` | `oklch(.955 .010 75)` | Shaded bands |
| `--ink` | `oklch(.18 .010 35)` | Headings / body |
| `--ink-2` | `oklch(.36 .010 35)` | Secondary text |
| `--ink-3` | `oklch(.58 .008 50)` | Meta / captions |
| `--crimson` | `#8C1A1A` | Primary brand accent |
| `--crimson-d` | `#6E1414` | Hover / pressed |
| `--honey` | `oklch(.66 .13 70)` | Warm secondary accent |

**Spacing** — 8-based scale `--s-1`(4px) … `--s-10`(144px). Sections use
`--section-y` (144px) top/bottom; gutter is 56px desktop / 24px mobile.

**Logo & seal** — the stacked wordmark (light/dark variants), the favicon, and
the transparent "V" seal used as a quiet sign-off above the footer. See
`brand-guide.html` for usage.

---

## Responsive

Breakpoint at **760px**. On mobile the nav stacks (logo → links → Donate
button, centered), every multi-column grid collapses to one column, the hero
image goes full-width above the text, and the footer centers. Intermediate
tweaks at 980px / 1080px. Open any page and narrow the window to see it.

---

## Before launch — content placeholders

Spots awaiting real content are marked with a pink/crimson pill
(`<span class="ph">…</span>`), e.g. `[YEAR — client]`, `[# — client]`,
`[TOTAL]`, `[opens — client]`. **To resolve:** drop in the real value and
remove the `<span class="ph">` wrapper — the text reverts to the standard,
unhighlighted style.

Other launch notes:
- **Donate buttons** currently open an email (`mailto:`) since there is no
  payment processor yet. Swap the `mailto:` hrefs for the checkout URL when a
  merchant is set up.
- **Social links** in the footer are placeholders (`href="#"`, each tagged
  `data-social="…"`). Replace with the live profile URLs (client has them).
- The `data-sq` attributes / `.sq-mapping` pills are design annotations
  (Squarespace section mapping); hidden unless `data-annotate="on"`. Safe to
  keep or remove.
