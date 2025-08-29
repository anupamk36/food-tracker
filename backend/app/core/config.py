from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field("HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    database_url: str = Field(..., env="DATABASE_URL")
    # allow comma-separated env like: http://localhost:5173,http://127.0.0.1:5173
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:5173"], env="CORS_ORIGINS")
    openai_api_key: str | None = Field(default=None, env="OPENAI_API_KEY")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
