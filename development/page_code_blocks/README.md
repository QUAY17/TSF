# Squarespace page code blocks

Each page of The Spinner Foundation site is **one self-contained Code Block**: the full page
markup + one namespaced `<style>`. This keeps Squarespace from overriding the design and lets the
nuanced bits work (sticky blurred nav, full-bleed bands, `:has()` section rhythm) because the
whole page renders in a single document context.

| File | Purpose |
|---|---|
| `_tsf-core.css` | Canonical design system, scoped under `.tsf`. Ported from `design/designer_styleguides/assets/styles.css` (exact OKLCH tokens). Embedded verbatim in each page's `<style>`. |
| `home.html` | Paste-ready homepage Code Block. |

Everything is namespaced under a single `.tsf` wrapper, type properties are hardened with
`!important` (so SS's native `h1/p/a` styles can't win), and `.tsf` uses a `100vw` breakout to
escape Squarespace's max-width content column.

---

## Ship to client preview — quickstart

1. **Upload the 8 images** (table below) into Squarespace and copy each hosted URL.
2. In `home.html`, **paste those URLs over the local `../../…` paths**: 5 in the IMAGE SOURCES
   block at the top of `<style>`, and 3 on the `<img src>` of the Rowdy ×2 + family-quote photos.
3. New page → **Blank Section** (Fill Screen off, top/bottom padding 0, width Full) → add **one
   Code Block** → paste all of `home.html`.
4. **Settings → Advanced → Code Injection (Header)** → paste the hide-chrome snippet (below) so
   Squarespace's native header/footer don't show.
5. **View on Preview**, then share the preview / password-protected link with the client.

The loud crimson `.ph` pills mark data still owed by the client (founding year, counts, totals —
see `CLIENT-QUESTIONS.md`). Fine to leave them loud for a preview, or fill known values first.

## Deploy a page (homepage)

1. **Add a blank section.** On the page, add a **Blank Section**. In its settings:
   Fill Screen **off**, top **and** bottom padding **0**, section width **Full**.
2. **Add one Code Block** into that section and paste the entire contents of `home.html`.
3. **Save, then view on Preview** (not the editor). The sticky nav and `backdrop-filter` blur
   do not render inside the SS editor canvas — that's expected; they appear on the live/preview page.

## Hide Squarespace's native header & footer

The design's own nav and footer live inside the code block, so hide SS's:

- **Settings → Advanced → Code Injection → Header**, add:
  ```html
  <style>
    /* Hide Squarespace's native header + footer on the custom-coded pages */
    #header, .header, #footer-sections, .sqs-announcement-bar-dropzone { display: none !important; }
    /* Let the code block reach the very top (kill the section's default top inset) */
    .page-section:first-child { padding-top: 0 !important; }
  </style>
  ```
- **Confirm the selectors against your live DOM.** Malone/7.1 markup varies by version — open the
  live page, inspect the header/footer wrappers, and adjust the selectors if the IDs differ
  (e.g. `header.header-announcement-bar-wrapper`, `#siteWrapper > header`). This snippet goes in
  **Code Injection**, which is separate from Design → Custom CSS (that field stays empty per the
  project rule).
- If you want the native header on the *other* pages but not here, scope the hide rule to this
  page's collection/page ID instead of site-wide.

## Swap in Squarespace-hosted images (7 files)

Local repo paths render now for design review. Before launch, host the images in Squarespace and
replace the paths:

1. Upload via **Design → Custom CSS → Manage Custom Files** (gives a stable
   `https://static1.squarespace.com/static/.../file.jpg` URL per file), or the file/asset uploader.
2. In `home.html`, the **5 background images** are centralized in the `IMAGE SOURCES` block at the
   top of `<style>` — replace each `url('../../design/...')` with the SS URL.
3. The **3 `<img>` photos** (Rowdy ×2, family-quote) are swapped on their `src=""` attributes in the
   markup (search `../../design/`).

| Where | Source file |
|---|---|
| `--logo-nav` | `wordmark-light.png` |
| `--logo-foot` | `wordmark-dark.png` |
| `--logo-v` (mobile masthead) | `branding_new_logos/tsf-ruled-v.png` (tight-cropped ruled-V) |
| `--img-hero` | `photos/cas-2.jpg` |
| `--img-mission` | `photos/family-7226.jpg` |
| `<img>` feature top | `photos/rowdy-2.jpg` |
| `<img>` feature lower | `photos/rowdy-1.jpg` |
| `<img>` family quote | `photos/family-quote-cropped.jpg` |

Footer social icons use placeholder `href="#"` (TikTok/Instagram/Facebook/X/Pinterest) — paste the
client's live profile URLs.

## Before launch — resolve placeholders

The loud crimson `.ph` pills mark client data still needed (tracked in `CLIENT-QUESTIONS.md`):
founding `[YEAR]`, partner counts `[#]`, gift `$[TOTAL]`, and the 501(c)(3) line. To resolve each:
drop in the real value **and** remove the wrapping `<span class="ph">…</span>` — the text then
reverts to the normal, unhighlighted style.

## Known SS watch-items (verify on Preview)

- **Sticky nav:** `position: sticky` needs no ancestor (SS section / `.sqs-block`) to clip overflow
  or set a transform. If the nav doesn't pin, set the host section to allow overflow, or move the
  `<header class="nav">` into its own code block at the top of the page.
- **Full-bleed width:** the `100vw` breakout assumes the block is horizontally centered. If a band
  doesn't reach edge-to-edge, confirm the section width is **Full** and padding is **0**.
- **Dangling `#donate`:** the mockup has no on-page donate band, so the Donate button and footer
  "Make a Donation" point at `mailto:` for now — revisit when the donate flow is decided.

---

## Superseded

`development/desktop_code_blocks/` holds the earlier **per-section** blocks. Once `home.html` is
confirmed in Squarespace, those can be archived. Note `hero-code-block.html` there is an obsolete
duplicate of `01-hero.html` (same `.tsf-hero` class, hardcoded year) — safe to delete.
