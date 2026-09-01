FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY backend/pyproject.toml backend/
COPY frontend/pyproject.toml frontend/

RUN uv sync --package frontend --no-dev --no-install-project

COPY frontend/src frontend/src

RUN uv sync --package frontend --no-dev

EXPOSE 8501

CMD ["uv", "run", "--no-dev", "--no-sync", "streamlit", "run", "frontend/src/frontend/app.py", \
     "--server.port=8501", "--server.address=0.0.0.0"]