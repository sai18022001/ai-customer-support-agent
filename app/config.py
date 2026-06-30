from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str = ""
    groq_api_key: str = ""
    database_url: str = "sqlite:///./agent.db"
    api_key: str = "dev-api-key-123"
    environment: str = "development"
    log_level: str = "INFO"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
