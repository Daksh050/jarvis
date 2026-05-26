# backend/main.py
from fastapi import FastAPI
from backend.api.routes import router
from backend.core.config import settings

# Initialize the API
app = FastAPI(title=settings.PROJECT_NAME)

# Mount the routes with a clean prefix
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"status": "online", "system": settings.PROJECT_NAME}