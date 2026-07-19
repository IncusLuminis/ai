# Audit: `shared/assets` media inventory

- **Agent:** media-keeper
- **Date:** 2026-07-19
- **Scope:** `/Users/mloktionov/Projects/IncusLuminis/shared/assets` (read-only audit, no files moved/deleted)

## File counts
525 files total (excluding nested `.git`). By type: PNG 151, HTML 82, WebM 54,
Markdown 35, JS 35, CSS 34, JPG 24, XCF (GIMP) 22, GIF 20, TXT 19, Jupyter
notebooks 14, XML 4, Python 3, JSON 2, SVG 1.

Media (images + video + design files) ≈ 271 files; the rest is mostly widget
templates/docs.

## Size
- Total working-tree size: **928 MB**
- Largest offenders (all under `gadgets/`, animated GIFs are the biggest
  single-file hogs):
  1. `gadgets/animations/radar_sweep.gif` — 155 MB
  2. `gadgets/gadgets/oscilloscope_trace_crt.gif` — 127 MB
  3. `gadgets/animations/oscilloscope_trace_crt.gif` — 126 MB
  4. `gadgets/gadgets/odometer_animation_assets.gif` — 96 MB
  5. `gadgets/animations/odometer_animation.gif` — 85 MB
  6. `gadgets/animations/ammo_storage/ammo_storage.webm` — 4.2 MB
  7. `gadgets/animations/hanging_table/hanging_table.webm` — 3.9 MB

## Duplicates
MD5 hash pass on 271 image/video/design files found 12 exact byte-identical
duplicate pairs (~24 files, low total waste). Pattern:
`widgets/sandbox/blogger-hud01-02-dev/screenshots/*` mirrored verbatim in
`widgets/releases/blogger-pilot-hud01-02/screenshots/*` (sandbox→release
promotion left stale copies), plus one shadow PNG duplicated across
`gadgets/gadget_5` and `gadgets/gadget_6`. Also many filename collisions
(`index.html`, `hud01/02-*.html/js`) but those are legitimate per-variant
template repeats, not asset duplication.

## Git / large-binary status
`shared/assets` is its own nested git repo. It has a deliberate `.gitignore`
blocking all raster/video/audio/design binary extensions (png, jpg, gif, webm,
xcf, etc.) with a comment stating "Rendered/binary media lives on the CDN, not
in git." `git ls-files` confirms only 22 tracked files (~48 KB, docs/scaffolding
only) — `widgets/` and `gadgets/` show as fully **untracked** in `git status`.
No Git LFS configured (not needed since binaries are excluded).

**Net:** policy is correctly followed today — no large binaries are actually
committed to git history, though the 928 MB of untracked media sits only on
local disk with no visible CDN sync record checked in this audit.
