
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    SECRET_KEY: str
    DEBUG: bool = True
    GROQ_TIMEOUT: float
    GROQ_API_KEY: str
    GROQ_MODEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

secrets = Settings()