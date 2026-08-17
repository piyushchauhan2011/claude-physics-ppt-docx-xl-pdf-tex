# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A collection of standalone Python scripts that each generate one polished document/artifact for a
"Physics Mechanics 101" teaching unit on 1D/2D kinematics and projectile motion. There is no application,
server, package, or test suite — each script is a one-shot generator: run it, it writes its output file(s)
to the repo root, done.

| Script | Output | Library |
|---|---|---|
| `generate_kinematics_pptx.py` | `1D_Kinematics_Intro.pptx` | `python-pptx` |
| `generate_projectile_motion_xlsx.py` | `Projectile_Motion.xlsx` | `openpyxl` |
| `generate_projectile_drag_xlsx.py` | `Projectile_Motion_With_Drag.xlsx` | `openpyxl` |
| `generate_projectile_report_docx.py` | `Projectile_Motion_Report.docx` | `python-docx` + `matplotlib` |
| `generate_projectile_paper.py` | `projectile_motion_paper.pdf` (+ `.tex`) | `matplotlib`/`numpy` + LaTeX |
| `index.html` | (itself — a standalone interactive web app) | none (vanilla JS) |

## Commands

### Environment

A venv already exists at `./venv` (Python 3.14.6, created via `python3 -m venv venv`) with every dependency
these scripts need: `python-pptx`, `openpyxl`, `python-docx`, `matplotlib`, `numpy`. Activate it before
running any generator script:

```bash
source venv/bin/activate
```

If a package is missing, install into the venv (not system Python):

```bash
pip install python-pptx openpyxl python-docx matplotlib
```

There is no `requirements.txt` — the venv is the source of truth for installed versions.

### Running a generator

Each script is self-contained and takes no arguments; it just writes its output file(s) into the repo root:

```bash
python generate_kinematics_pptx.py
python generate_projectile_motion_xlsx.py
python generate_projectile_drag_xlsx.py
python generate_projectile_report_docx.py
python generate_projectile_paper.py
```

Re-running a script overwrites its corresponding output file(s) in place.

### LaTeX / PDF pipeline

`generate_projectile_paper.py` also requires a system LaTeX install (`pdflatex` on `PATH` — this machine has
TeX Live 2026 at `/Library/TeX/texbin`). The script writes figures + `.tex` source into a scratch
`paper_build/` directory, shells out to `pdflatex` **twice** via `subprocess` (the second pass resolves
`\ref`/`\eqref` cross-references), copies the final `.pdf`/`.tex` to the repo root, then deletes
`paper_build/` entirely. If you edit the LaTeX template string inside the script, keep both `pdflatex`
invocations — a single pass leaves references as `??`.

### The web app (`index.html`)

Single self-contained file (HTML+CSS+JS inline, no build step, no external dependencies) — open it directly:

```bash
open index.html
```

For automated browser testing (e.g. Playwright), `file://` URLs are blocked — serve it over HTTP instead:

```bash
python3 -m http.server 8934
# then navigate to http://localhost:8934/index.html
```

## Architecture notes

**No shared code between generators.** Each script duplicates its own color palette, styling helpers, and
physics constants rather than importing from a common module — this is intentional for these one-shot
scripts (each was written independently to be run once and read top-to-bottom), not an oversight to "fix" by
extracting a shared library unless asked.

**Consistent visual language across formats.** All generators use the same dark-navy/teal/gold palette
(`#0B1F3A` navy, `#2EC4B6` teal, `#F2A63D` gold) so the pptx, xlsx, docx, PDF, and HTML outputs read as one
series. If asked to add a new deliverable to this set, match this palette rather than introducing a new one.

**Consistent physics defaults across deliverables.** The canonical example values (`v0 = 25 m/s`,
`theta = 45°`, `g = 9.81 m/s²`) recur in every output — e.g. `H_max ≈ 15.93 m`, `R_max ≈ 63.71 m`,
`t_total ≈ 3.60 s` for the no-drag case, and `R ≈ 45 m` for the drag case with `m = 0.25 kg`, `r = 0.05 m`,
`Cd = 0.47`, `rho = 1.225 kg/m³`. These numbers are cross-checked against each other across the pptx/xlsx/
docx/pdf files; if you change a default in one generator, the others will no longer numerically agree unless
updated too.

**Excel formula generation pattern** (`generate_projectile_motion_xlsx.py`,
`generate_projectile_drag_xlsx.py`): these scripts write live Excel formulas as strings (e.g.
`f"=$B$3*COS(RADIANS($B$4))*A{r}"`), not precomputed values — `openpyxl` never evaluates formulas, so a
Python-side simulation (mirroring the exact Euler-integration formulas that get written to cells) is run
first purely to determine how many table rows are needed, then the same physics is re-expressed as
row-by-row Excel formulas referencing absolute input cells (`$B$3`, `$B$4`, ...). Keep row-sizing logic and
the actual formula strings in sync if you change the physics.

**Euler integration convention:** the drag simulations (Excel workbook, and `index.html`'s JS physics) all
use the same semi-implicit Euler step ordering: acceleration is computed from the *current* velocity, then
position is updated using the *old* velocity, then velocity is updated using the *old* acceleration. Keep
this ordering consistent if modifying any of the numerical integrators — it's what the earlier
Excel-vs-Python cross-checks in this repo's history were validated against.

**`index.html` physics/render split:** the drag trajectory is integrated numerically (fixed 1/240s timestep,
frame-rate-independent via an accumulator) while the parallel "ideal vacuum" reference trail is computed
analytically from a shared master clock (`sim.t`) rather than integrated — this lets the two trails land at
different times (drag always lands first or at the same time) while staying perfectly in sync. The view's
auto-fit scale is derived once from the *ideal* trajectory's predicted range/height (a guaranteed upper
bound on the drag trajectory, since quadratic drag only removes energy), so it never needs to rescale
mid-flight.

## Gotchas encountered in this repo's history

- **Excel slider/cell precision:** when writing numeric input cells with `openpyxl`, don't rely on a
  `number_format` string alone to fix rounding — check the actual value written matches the intended default.
- **HTML range-input `step` values must evenly divide the default `value`**, or the browser silently snaps
  the on-load display to the nearest valid step (e.g. a default of `9.81` with `step="0.1"` renders as
  `9.8`). Pick a step size that divides every physically-meaningful default exactly.
- **LaTeX + `hyperref` color options** (`colorlinks=true, linkcolor=blue!50!black`) require `\usepackage{xcolor}`
  explicitly — `hyperref`'s default `color` package doesn't support the `!`-mixing syntax and fails with
  `Undefined color`.
- **matplotlib + Arial:** subscripted Unicode characters like `v₀` are missing from Arial and trigger a
  "Glyph missing" warning; use plain ASCII (`v0`) in plot labels instead, reserving LaTeX-style math
  (`$v_0$`, rendered via `mathtext.fontset: "cm"`) for the LaTeX-adjacent figures in `generate_projectile_paper.py`.
