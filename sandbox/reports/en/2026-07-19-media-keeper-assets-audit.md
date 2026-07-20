# Audit: `shared/assets` media inventory

- **Agent:** media-keeper
- **Date:** 2026-07-19
- **Scope:** `/Users/mloktionov/Projects/IncusLuminis/shared/assets` (read-only audit, no files moved/deleted)

## File counts
558 files total (excluding `.git`). By type: PNG 151, HTML 82, WEBM 54,
Markdown 35, JS 35, CSS 34, JPG 24, XCF (GIMP source) 22, GIF 20, TXT 19,
plus smaller counts of ipynb/json/xml/svg/py.

## Size
~928 MB total. `gadgets/` = 890 MB, `widgets/` = 38 MB.

Largest files:
1. `gadgets/animations/radar_sweep.gif` — ~155 MB
2. `gadgets/gadgets/oscilloscope_trace_crt.gif` — ~127 MB
3. `gadgets/animations/oscilloscope_trace_crt.gif` — ~126 MB
4. `gadgets/gadgets/odometer_animation_assets.gif` — ~96 MB
5. `gadgets/animations/odometer_animation.gif` — ~85 MB
6. Several smaller GIFs and XCF source files in the 5-9 MB range.

## Duplicates
- Confirmed exact (MD5-identical) duplicates: 13 `Screenshot *.png` files
  (~6.9 MB total) present in both
  `widgets/releases/blogger-pilot-hud01-02/screenshots/` and
  `widgets/sandbox/blogger-hud01-02-dev/screenshots/` — a release copy
  duplicating dev sandbox screenshots.
- Naming collisions (**not** byte-identical, different MD5s despite same
  filename) between `gadgets/animations/` and `gadgets/gadgets/`:
  `oscilloscope_trace_crt.gif`, `counter_animation_tubes_decimal.gif`,
  `analog_meter_animation.gif` — worth a look, could be stale variants under
  confusingly matching names rather than true dupes.
- `09-trim_indicator*` files and `table_on_rope.webm` also repeat by name
  across `old/`/variant subfolders but differ in content — appear to be
  intentional version history, not dupes.

## Git / large-binary status
`shared/assets` is its own git repo (remote `IncusLuminis/assets.git`) with
only 22 tiny files tracked (docs/config/`.gitkeep`s). `.gitignore`
explicitly excludes all raster/video/audio/design-project/3D formats, with a
comment stating binary media belongs on the CDN, not git — `gadgets/` and
`widgets/` show fully untracked (`??`) in `git status`. No Git LFS
configured, but none is needed since binaries are correctly kept out of the
committed tree.

**Net:** no violation found — git/large-binary hygiene is good.
