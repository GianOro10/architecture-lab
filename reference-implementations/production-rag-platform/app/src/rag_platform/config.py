from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RAG_", case_sensitive=False)

    service_name: str = "production-rag-platform"
    environment: str = "local"
    max_document_chars: int = 20_000
    max_question_chars: int = 2_000
    default_top_k: int = 3
    maximum_top_k: int = 10


@lru_cache
def get_settings() -> Settings:
    return Settings()
