from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth as auth_router, meals as meals_router
from app.db import engine, Base
import os

# Create DB tables if not present (simple)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

origins = [settings.CORS_ORIGINS] if isinstance(settings.CORS_ORIGINS, str) else settings.CORS_ORIGINS
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
app.include_router(meals_router.router, prefix="/api/meals", tags=["meals"])

@app.get("/")
def root():
    return {"status": "ok"}
