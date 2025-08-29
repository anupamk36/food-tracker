from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api import auth, meals, users
from pathlib import Path
import os

app = FastAPI(title="Food Tracker API", version="1.0.0")

origins = [o.strip() for o in settings.cors_origins if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded files
UPLOAD_DIR = Path(os.environ.get("UPLOAD_DIR", "uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(meals.router, prefix="/api/meals", tags=["meals"])
app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.get("/api/health")
def health():
    return {"status": "ok"}
