# PROMPT 11

Please configure `pytest-cov` to generate a detailed HTML code coverage report for the physics engine, enforce coverage thresholds, and integrate reporting into the CI/CD pipeline.

Requirements:
1. Coverage Configuration (`pyproject.toml` or `.coveragerc`):
   - Configure coverage settings:
     * Source target: `physics.py` (or `app.py` core calculation module).
     * Enable branch coverage (`branch = true`) to track all conditional execution paths.
     * Exclude test files (`tests/*`), virtual environments (`.venv/*`), and non-calculation UI boilerplate.
     * Set a strict minimum coverage threshold (e.g., `fail_under = 90`).

2. Report Generation Setup:
   - Command to execute: `pytest --cov=. --cov-report=term-missing --cov-report=html:htmlcov tests/`
   - Generate terminal summary highlighting missing line numbers (`term-missing`).
   - Output standalone interactive HTML site inside `htmlcov/`.

3. Workspace Hygiene:
   - Add `.coverage`, `.coverage.*`, `htmlcov/`, and `coverage.xml` to `.gitignore`.

4. CI/CD Integration Update (`.github/workflows/ci.yml`):
   - Update the test step in GitHub Actions to run pytest coverage and generate XML (`--cov-report=xml`).
   - Enforce build failure if physics coverage drops below 90% (`--cov-fail-under=90`).
   - Add an action step to upload `coverage.xml` or `htmlcov/` as a workflow artifact.

5. Execution:
   - Run the test suite with coverage in the terminal.
   - Automatically open the interactive HTML report in macOS Safari/Chrome (`open htmlcov/index.html`).
