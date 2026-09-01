FROM python:3.12-slim

# uv is installed as a binary, no pip needed
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# copy only the files uv needs to resolve dependencies
COPY pyproject.toml uv.lock ./
COPY backend/pyproject.toml backend/
COPY frontend/pyproject.toml frontend/

# install dependencies for the backend package only, no dev tools
RUN uv sync --package backend --no-dev --no-install-project

# now copy the actual source code
COPY backend/src backend/src
COPY data data

RUN uv sync --package backend --no-dev

EXPOSE 8000

CMD ["uv", "run", "--no-dev", "--no-sync", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]