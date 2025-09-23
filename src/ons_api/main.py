from fastapi import FastAPI
from .api.routes import router as ons_router

app = FastAPI(
    title="ONS EAR API",
    description="Extract data from ONS and check information from GCP"
)

app.include_router(ons_router, prefix="/api/v1")

@app.get("health", tags=["Health Check"])
def health_check():
    return {"status": "ok"}