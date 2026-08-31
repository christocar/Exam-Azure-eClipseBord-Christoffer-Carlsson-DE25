from fastapi import FastAPI

app = FastAPI(title="eClipseBord API")


@app.get("/health")
def health():
    return {"status": "ok"}