FROM python:3.12-slim

# uv is installed as a binary, no pip needed
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# same as the backend, uv reads the whole workspace so both pyprojects are needed
COPY pyproject.toml uv.lock ./
COPY backend/pyproject.toml backend/
COPY frontend/pyproject.toml frontend/

# --package frontend means only streamlit and its dependencies, no fastapi
RUN uv sync --package frontend --no-dev --no-install-project

COPY frontend/src frontend/src

RUN uv sync --package frontend --no-dev

# no csv here, the frontend gets all its data from the API
EXPOSE 8501

# --server.address is streamlit's version of uvicorn's --host, same reason
# the port is fixed here so it doesn't drift between local, compose and Azure
CMD ["uv", "run", "--no-dev", "--no-sync", "streamlit", "run", "frontend/src/frontend/app.py", \
     "--server.port=8501", "--server.address=0.0.0.0"]