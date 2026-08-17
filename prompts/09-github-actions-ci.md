# PROMPT 9

Please create a production-ready GitHub Actions CI/CD workflow file in `.github/workflows/ci.yml` for testing, building, and publishing the Streamlit projectile motion Docker container.

Requirements:
1. Workflow Triggers:
   - Run on `push` to `main` and `master` branches.
   - Run on `pull_request` targeting `main` and `master` branches.

2. Job 1: Lint & Code Check (`lint-and-check`):
   - Runner: `ubuntu-latest`.
   - Set up Python 3.11 with pip caching.
   - Install dependencies from `requirements.txt` along with `ruff` for linting.
   - Execute syntax check (`python -m py_compile app.py`) and lint check (`ruff check .`).

3. Job 2: Build & Integration Test (`build-and-test`):
   - Depends on `lint-and-check`.
   - Set up Docker Buildx (`docker-setup-buildx` action).
   - Build the container image using GitHub Actions cache (`type=gha`).
   - Run the container in detached mode on port `8501:8501`.
   - Add an automated integration test loop: query `http://localhost:8501/_stcore/health` via `curl` with up to 10 retries (every 3 seconds) to verify Streamlit boots successfully without runtime crashes.
   - Clean up container after test completion.

4. Job 3: Publish to GHCR (`publish`):
   - Depends on `build-and-test`.
   - Run condition: Only on `push` to `main`/`master` (skip for `pull_request`).
   - Authenticate to GitHub Container Registry (`ghcr.io`) using `permissions: packages: write` and `secrets.GITHUB_TOKEN`.
   - Generate tags and labels using `docker/metadata-action` (tagging both `latest` and `sha-${{ github.sha }}`).
   - Build and push the image to `ghcr.io/${{ github.repository }}:latest`.

5. Execution:
   - Create the directory structure `.github/workflows/` if needed and write `ci.yml`.
   - Validate the generated YAML syntax locally to ensure no formatting or indentation errors.
