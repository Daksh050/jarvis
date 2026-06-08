# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import subprocess
import requests
import time

from backend.api.routes import router

def ensure_ai_engine_running():
    """Pings the Ollama server and starts it silently if it is offline."""
    print("Checking AI Engine status...")
    try:
        requests.get("http://localhost:11434/", timeout=2)
        print("[OK] AI Engine is already online.")
    except requests.exceptions.ConnectionError:
        print("[WAIT] AI Engine offline. Booting local server automatically...")
        subprocess.Popen(
            ["ollama", "serve"], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        time.sleep(3)
        print("[OK] AI Engine successfully started.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_ai_engine_running()
    yield
    print("Shutting down J.A.R.V.I.S. backend...")

app = FastAPI(title="Local_JARVIS", lifespan=lifespan)

# --- THE CORS FIX ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (Swagger, Localhost, frontend apps)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Mount the routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"status": "online", "system": "Local_JARVIS"}