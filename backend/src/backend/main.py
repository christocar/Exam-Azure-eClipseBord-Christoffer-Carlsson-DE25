from fastapi import FastAPI

from backend.data_loader import load_eclipses

app = FastAPI(title="eClipseBord API")

# loaded once at startup, kept in memory
df = load_eclipses()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/eclipses")
def eclipses(min_year: int = 1900, max_year: int = 2100, type: str | None = None):
    result = df[(df["year"] >= min_year) & (df["year"] <= max_year)]

    if type:
        result = result[result["type"] == type]

    return result.to_dict(orient="records")


@app.get("/eclipses/count-by-type")
def count_by_type(min_year: int = 1900, max_year: int = 2100):
    result = df[(df["year"] >= min_year) & (df["year"] <= max_year)]
    counts = result["type"].value_counts()
    return counts.to_dict()