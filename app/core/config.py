"""
pydantic-settings 기반 설정 (CODING_RULES.md 2-3, 폴더 구조와 무관하게 유지).
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    ENV: str = "local"

    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "remedi_user"
    DB_PASSWORD: str = "changeme"
    DB_NAME: str = "remedi_db"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001

    JWT_SECRET_KEY: str = "dev-only-insecure-secret-CHANGE-ME"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 14 * 24 * 60

    MFDS_API_KEY: str = ""

    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    @property
    def sqlalchemy_database_url(self) -> str:
        # SQLAlchemy 유지 (2026-07 재확인) + asyncmy 비동기 드라이버
        return (
            f"mysql+asyncmy://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
