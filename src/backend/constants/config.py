
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):

    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    CORS_ORIGINS: List[str] = ["https://zoroai.streamlit.app", "http://localhost:8501"]
    DEBUG: bool = False
    SECRET_KEY: str
    OPEN_ROUTER_MODEL: str
    OPEN_ROUTER_API_KEY: str
    ADMIN_EMAIL: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    # NEEDED IF RUNNING PROJECT LOCALLY
    # ZORO_API_BASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

secrets = Settings()
