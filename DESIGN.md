# Design

Single-file webapp (`index.html`). Light, photographic, monochrome (cream / dark grey / white). Geist (Google Fonts).

## Theme
Monochrome, restrained. The photo previews carry all the colour; the chrome is neutral. Library = cream canvas. **Editor = same cream as the library** (header, preview, dock, tab menu — `--bg`), separated by 2px (`--div`) `#292929` dividers (the logo colour). Icons and text are dark (`#292929`) on cream. The "accent" is the darkest neutral, used for active/primary states only.

## Color (tokens in `:root`)
- Surfaces: `--bg #EFE9E2` (cream, library) · `--bg2 #f7f7f7` · `--panel #f0f0f0` · `--panel2 #e8e8e8` · editor chrome = `--bg`
- Lines: `--line #e4e4e4` · `--line2 #d2d2d2` · editor dividers `#292929`, 2px (`--div`)
- Text: `--txt #292929` · `--txt2 #595959` · `--txt3 #8c8c8c`
- Accent (dark): `--accent #292929` · `--accent2 #2c2c2c` — used for active / primary only.
- Ink on accent (cream on dark): `--ink #EFE9E2`
- Slider polarity: `--pos #141414` (positive) · `--neg #9a9a9a` (negative)

Rules: accent = actions, current selection, state only (never decoration). Text on accent = `--ink`. No grey text on coloured backgrounds. Editor chrome: no dark bars; hover = `rgba(41,41,41,.08)`, inactive tab = 50% opacity.

## Typography
Geist (fallback Helvetica Neue, Arial). Fixed px scale (product register): 17 (h1) · 16 (h2) · 15 (body/input) · 14 (slider value, foot buttons) · 13 (labels, chips, controls) · 12 (compact controls, raw) · 11 (sub, eyebrow, count) · 10 (badges). Numbers use `font-variant-numeric: tabular-nums`.

## Radius
Aucun arrondi : `border-radius: 0` partout (cartes, boutons, chips, FAB, icônes, sliders). Les variables `--r-*` valent `0`.

## Components
Preset card · filter chip · **editor preset strip** (VSCO-style row of 56px thumbnails, each previewing the look on the user's own photo; active = `--accent` border) · custom slider (track + polarity fill + thumb; bipolar sliders show a signed value, magnitude sliders like Intensité/Grain/Vignettage/Estompé show none) · segmented control · FAB (fav / import / camera) · bottom-sheet/side-drawer editor (cream, `#292929` dividers) · toast. Every interactive element has default / hover / focus-visible / active; `--accent` focus ring (`:focus-visible`).

## Capture
No custom viewfinder — the camera FAB opens the **native OS camera** via `<input type="file" accept="image/*" capture="environment">` (best quality, native aspect, correct orientation). Import uses the same pattern without `capture`. The captured/imported photo opens straight into the editor.

## Crop
"Recadrer" overlays the preview with a draggable/resizable box (corner handles + move), a rule-of-thirds grid, an outside dim, and a ratio chip row (Libre · Original · 1:1 · 4:5 · 5:4 · 3:2 · 2:3 · 16:9 · 9:16) with apply/cancel. The crop is stored normalized to the image and applied in `renderRecipe` (`opts.crop` source-rect) so preview + export match. Cream stroke/handles on the photo; selected ratio = dark-filled chip.

## Motion
150–340ms, ease-out curves. Editor slides in (sheet on mobile, drawer ≥880px). Preview re-renders on `requestAnimationFrame`. Full `prefers-reduced-motion: reduce` fallback (transitions/animations collapsed).

## Layout
Mobile-first. Gallery: `repeat(auto-fill, minmax(158/190px, 1fr))`. Editor: full-screen sheet on mobile, 520px right drawer 880–1023px, full-screen split ≥1024px (photo left, 400px controls panel right: tabs on top, presets as a 4-col grid, tools as a 3-col grid; 440px panel ≥1440px). Gallery columns: 3 · 4 (≥560) · 6 (≥880) · 7 (≥1440) · 8 (≥1800). Safe-area insets respected.

## Preview
The photo sits in a cream field with a small margin (12px mobile, 40px ≥1024px) so cream space breathes around it. Crop mode uses a fixed 30px margin (`PAD` in `imgDispRect`) for handle reach — keep both in sync.
