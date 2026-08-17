# Physics Mechanics 101 — Projectile Motion Toolkit

Teaching materials and an interactive dashboard for a unit on 1D/2D kinematics and projectile
motion. The repo has two halves:

- **Document generators** — standalone Python scripts that each produce one polished artifact
  (slide deck, spreadsheets, a Word report, a LaTeX paper).
- **Interactive dashboard** — a Streamlit + Plotly app comparing the ideal (vacuum) projectile
  trajectory against one with quadratic air resistance, numerically integrated with SciPy,
  containerized with Docker, and covered by a pytest suite and GitHub Actions CI/CD.

## Interactive Dashboard

### Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501.

### Run with Docker

```bash
docker compose up --build -d
```

Open http://localhost:8501. `docker-compose.yml` bind-mounts the repo into the container, so
edits to `app.py`/`physics.py` hot-reload without a rebuild. Check container health with:

```bash
docker ps   # STATUS column should show "healthy"
```

### Project layout

- `app.py` — Streamlit UI: sidebar controls, presets, KPI metrics, and the three Plotly tabs
  (trajectory curve, kinematics over time, energy dissipation). Contains no physics math itself.
- `physics.py` — pure, Streamlit-free physics functions:
  - `compute_drag_constant(rho, Cd, radius)` — quadratic drag constant `k = 0.5·ρ·Cd·πr²`
  - `drag_derivatives(t, state, k, m, g)` — the ODE right-hand side for `solve_ivp`
  - `solve_trajectory(...)` — numerically integrates the drag trajectory to ground impact
  - `calculate_vacuum_analytical(...)` — exact closed-form ideal (no-drag) trajectory
- `tests/test_physics.py` — pytest suite covering the vacuum limit, drag-vs-ideal invariants,
  energy conservation/dissipation, trajectory asymmetry, and edge cases (vertical launch,
  launch-from-height, mass sensitivity).

### Tests & linting

```bash
pytest -v                                       # run the test suite
pytest --cov=physics --cov-report=term-missing  # with coverage
ruff check app.py physics.py tests              # lint
```

### CI/CD

`.github/workflows/ci.yml` runs on every push/PR to `main`/`master`:

1. **lint-and-check** — `py_compile`, `ruff check`, `pytest -v`
2. **build-and-test** — builds the Docker image (GitHub Actions layer cache), runs it, and polls
   `/_stcore/health` until Streamlit is confirmed up
3. **publish** — on push to `main`/`master` only: pushes the image to
   `ghcr.io/<owner>/<repo>` tagged `latest` and `sha-<commit>`

## Document Generators

Each script is self-contained and writes its output(s) to the repo root:

| Script | Output |
|---|---|
| `generate_kinematics_pptx.py` | `1D_Kinematics_Intro.pptx` — 10-slide deck on 1D kinematics |
| `generate_projectile_motion_xlsx.py` | `Projectile_Motion.xlsx` — ideal-trajectory workbook with live formulas + chart |
| `generate_projectile_drag_xlsx.py` | `Projectile_Motion_With_Drag.xlsx` — Euler-integration drag vs. ideal comparison workbook |
| `generate_projectile_report_docx.py` | `Projectile_Motion_Report.docx` — Word report with an embedded matplotlib trajectory plot |
| `generate_projectile_paper.py` | `projectile_motion_paper.pdf` (+ `.tex`) — LaTeX academic paper, compiled via `pdflatex` |

Run any of them with the same venv used for the dashboard:

```bash
source venv/bin/activate
python generate_kinematics_pptx.py
```

`generate_projectile_paper.py` additionally requires a system LaTeX install (`pdflatex` on
`PATH`).

There's also `index.html` — a self-contained, dependency-free HTML5 Canvas simulator for
projectile motion with drag, open it directly in a browser (`open index.html`).

See `CLAUDE.md` for further implementation notes (numerical integration conventions, known
gotchas hit during development, and why the physics defaults are cross-checked across every
output format).
