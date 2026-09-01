# eClipseBord

A fullstack dashboard for exploring NASA's five millennium catalog of solar eclipses.
Built as a lab for the Azure course in Data Engineering at Stockholms Tekniska Institut (DE25).

The stack is FastAPI + Streamlit, containerized with Docker and deployed to Azure
with infrastructure defined in Terraform.

## Architecture

The application runs as two separate services. The frontend never reads the CSV
directly — all data goes through the API.

```
┌──────────────┐        HTTP        ┌──────────────┐
│   Frontend   │ ─────────────────► │   Backend    │ ──► solar.csv
│  (Streamlit) │                    │  (FastAPI)   │
└──────────────┘                    └──────────────┘
```

The same code runs in three environments. The only thing that changes is how the
frontend finds the backend, which is controlled by the `API_URL` environment variable:

| Environment | API_URL |
|---|---|
| Local | `http://localhost:8000` |
| Docker Compose | `http://backend:8000` (container name as hostname) |
| Azure | `https://app-eclipsebord-backend-chr01.azurewebsites.net` |

In the code this is a single line:

```python
API_URL = os.getenv("API_URL", "http://localhost:8000")
```

### Azure resources

All resources are defined in `infra/` and created with Terraform:

- **Resource Group** — container for everything else
- **Container Registry (ACR)** — stores the two Docker images
- **App Service Plan (B1, Linux)** — shared by both web apps
- **Linux Web App × 2** — one for the backend, one for the frontend

Region is `denmarkeast`, one of four regions unlocked for my student subscription.

## Project structure

```
.
├── backend/            # FastAPI service
│   ├── Dockerfile
│   └── src/backend/
│       ├── main.py         # API endpoints
│       └── data_loader.py  # reads and cleans the CSV
├── frontend/           # Streamlit dashboard
│   ├── Dockerfile
│   └── src/frontend/
│       └── app.py
├── data/               # solar.csv
├── notebooks/          # EDA
├── infra/              # Terraform
├── docker-compose.yml
├── pyproject.toml      # uv workspace root
└── uv.lock             # one lockfile for both packages
```

The project uses a **uv workspace**. Backend and frontend are separate packages
with their own dependencies, but they share a single lockfile. Jupyter and pandas
for the EDA are dev dependencies in the root and are excluded from the Docker images.

## Running locally

```bash
uv sync
```

Backend (from the repo root — the CSV path is relative to it):

```bash
uv run uvicorn backend.main:app --reload
```

Frontend, in a second terminal:

```bash
uv run streamlit run frontend/src/frontend/app.py
```

The dashboard is at `http://localhost:8501`, the API docs at `http://localhost:8000/docs`.

## Running with Docker

```bash
docker compose up --build
```

Same URLs. Compose puts both containers on a shared network, which is what makes
`http://backend:8000` resolve.

## Deploying to Azure

Requires Azure CLI, Terraform and Docker. Log in first:

```bash
az login
export ARM_SUBSCRIPTION_ID="<your-subscription-id>"
```

The subscription ID is passed as an environment variable so it stays out of the repo.

### 1. Create the infrastructure

```bash
cd infra
terraform init
terraform apply
```

The web apps are created before the images exist in the registry, so they will not
start yet. That is expected.

### 2. Push the images

```bash
cd ..
az acr login --name acreclipsebordchr01

docker build -f backend/Dockerfile -t eclipsebord-backend .
docker build -f frontend/Dockerfile -t eclipsebord-frontend .

docker tag eclipsebord-backend acreclipsebordchr01.azurecr.io/eclipsebord-backend:v1
docker tag eclipsebord-frontend acreclipsebordchr01.azurecr.io/eclipsebord-frontend:v1

docker push acreclipsebordchr01.azurecr.io/eclipsebord-backend:v1
docker push acreclipsebordchr01.azurecr.io/eclipsebord-frontend:v1
```

Note that both builds run from the repo root. The build context has to be the root
because `uv.lock` lives there.

### 3. Restart the web apps

```bash
az webapp restart --name app-eclipsebord-backend-chr01 --resource-group rg-eclipsebord
az webapp restart --name app-eclipsebord-frontend-chr01 --resource-group rg-eclipsebord
```

Verify the backend at `/health` before checking the frontend. The first request
after a restart can take a couple of minutes while Azure pulls the image.

### Tearing it down

```bash
cd infra
terraform destroy
```

This removes everything including the registry, so the images have to be pushed
again on the next deploy. Being able to tear down and rebuild in minutes is the
main practical benefit of defining the infrastructure in code.

### Notes on the setup

- `WEBSITES_PORT` tells Azure which port the container listens on (8000 for the
  backend, 8501 for the frontend). Without it Azure assumes port 80 and gets no response.
- Both containers bind to `0.0.0.0`, not `127.0.0.1`. Inside a container, localhost
  means the container itself and nothing can reach it from the outside.
- The registry credentials are read from the ACR resource by Terraform, so no
  password is written in the code. A cleaner approach would be managed identity,
  where the web app gets its own identity in Azure and is granted the `AcrPull` role.

## Dataset

NASA's five millennium catalog of solar eclipses, covering 11898 eclipses between
1999 BC and AD 3000. The lunar eclipse dataset was not used — the lab is about the
solar eclipse of August 12, 2026.

A short EDA is in `notebooks/eda.ipynb`. Two findings shaped the backend:

**Dates.** Years before Christ are stored as negative numbers (`-1999 June 12`),
which pandas cannot parse as dates. The year is extracted as an integer instead.
Month and day are irrelevant when the range spans 5000 years.

**Eclipse types.** The `Eclipse Type` column has 19 distinct codes, but they group
into four main types by their first letter: T (total), A (annular), P (partial) and
H (hybrid). The suffixes are NASA's notation for special cases such as eclipses at
sunrise or sunset. The dashboard groups on the first letter — 19 categories would
make a filter unusable.

`Path Width` and `Central Duration` are empty in exactly the 4200 partial eclipses,
since a partial eclipse has no central line. Not missing data, but data that does
not apply. Both columns are excluded from the API.

## LLM usage

Claude was used as a tutor throughout this lab: for explanations, for reviewing
decisions, and for hinting at possible solutions when stuck. 

Debugging was done by me, with the model as a sounding board — including a port
conflict caused by a container left running from a previous exercise, and the B1
quota being unavailable in `norwayeast`.