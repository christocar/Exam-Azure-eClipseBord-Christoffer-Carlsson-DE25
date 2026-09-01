from fastapi import FastAPI

from backend.data_loader import load_eclipses

app = FastAPI(title="eClipseBord API")

# loaded once at startup, kept in memory
# the dataset is small enough that each request is just a filter
df = load_eclipses()


# used to check that the container is alive, especially in Azure
@app.get("/health")
def health():
    return {"status": "ok"}


# the parameters below become query params automatically, e.g. /eclipses?min_year=2000
# FastAPI also validates the types, so min_year=abc gives a 422 without any code from me
@app.get("/eclipses")
def eclipses(min_year: int = 1900, max_year: int = 2100, type: str | None = None):
    result = df[(df["year"] >= min_year) & (df["year"] <= max_year)]

    if type:
        result = result[result["type"] == type]

    return result.to_dict(orient="records")


# aggregating here instead of in the frontend, no reason to send 2600 rows
# just to count them
@app.get("/eclipses/count-by-type")
def count_by_type(min_year: int = 1900, max_year: int = 2100):
    result = df[(df["year"] >= min_year) & (df["year"] <= max_year)]
    counts = result["type"].value_counts()
    return counts.to_dict()