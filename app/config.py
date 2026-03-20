from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "AniQuote API"
    debug: bool = False
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/aniquote"
    
    # Security
    secret_key: str = "hokkaido"
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
