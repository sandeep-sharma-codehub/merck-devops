from fastapi import FastAPI

from app.routers import data, health

app = FastAPI(
    title="Merck DevOps API",
    description="Python REST API with AWS deployment pipeline",
    version="1.0.0",
)

app.include_router(health.router)
app.include_router(data.router)
