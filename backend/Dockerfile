FROM python:3.12-slim

# uv is installed as a binary, no pip needed
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# copy only the files uv needs to resolve dependencies
# the frontend pyproject is needed too, uv reads the whole workspace
COPY pyproject.toml uv.lock ./
COPY backend/pyproject.toml backend/
COPY frontend/pyproject.toml frontend/

# install dependencies for the backend package only, no dev tools
# this layer is cached as long as uv.lock is unchanged, so code edits don't
# trigger a reinstall of fastapi and pandas
RUN uv sync --package backend --no-dev --no-install-project

# now copy the actual source code
COPY backend/src backend/src

# the csv goes into the image, it's only 1 MB
# in production you would keep data out of the image, e.g. in blob storage
COPY data data

# installs the backend package itself, the layer above did the dependencies
RUN uv sync --package backend --no-dev

# documents the port, doesn't open anything on its own
EXPOSE 8000

# --no-sync stops uv from checking the environment at startup, it's already built
# --host 0.0.0.0 is required, 127.0.0.1 inside a container means the container itself
CMD ["uv", "run", "--no-dev", "--no-sync", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]