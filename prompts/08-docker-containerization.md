# PROMPT 8

Please create a complete Docker containerization setup for the Streamlit projectile motion dashboard (`app.py`).

Requirements:
1. Requirements File (`requirements.txt`):
   - Include `streamlit`, `plotly`, `numpy`, and `scipy` with compatible version bounds.

2. Dockerfile (`Dockerfile`):
   - Base Image: `python:3.11-slim` (lightweight, security-patched).
   - Set working directory to `/app`.
   - Copy `requirements.txt` and install dependencies with `--no-cache-dir`.
   - Copy application files into the container.
   - Expose port `8501`.
   - Add a `HEALTHCHECK` instruction querying `http://localhost:8501/_stcore/health`.
   - Set CMD to launch Streamlit: `streamlit run app.py --server.port=8501 --server.address=0.0.0.0`.

3. Docker Compose Configuration (`docker-compose.yml`):
   - Service name: `projectile-dashboard`.
   - Build context: current directory (`.`).
   - Port mapping: `8501:8501`.
   - Volume mapping: Mount `.` to `/app` for live code hot-reloading during development.
   - Set environment variables (`PYTHONUNBUFFERED=1`).
   - Restart policy: `unless-stopped`.

4. Docker Ignore (`.dockerignore`):
   - Exclude `.git`, `__pycache__`, `*.pyc`, `.env`, `.venv`, and `venv`.

5. Execution & Testing:
   - Build and start the container using `docker compose up --build -d`.
   - Verify the container health status via `docker ps`.
   - Open `http://localhost:8501` in the default web browser (`open http://localhost:8501` on macOS).
