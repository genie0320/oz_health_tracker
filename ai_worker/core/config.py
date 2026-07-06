from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001


settings = Settings()
