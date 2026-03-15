from fastapi import FastAPI

from app.routers import package, psr, timeline, analytics

app = FastAPI(
    title="APP TEST FOR AI",
    version="1.0.0",
)


@app.get("/")
def health_check():
    return {"status": "OK"}


app.include_router(package.router)
app.include_router(psr.router)
app.include_router(timeline.router)
app.include_router(analytics.router)
