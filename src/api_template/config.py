from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    discord_api_secret: str
    log_level: str = "INFO"

    # Add your service-specific settings here, for example:
    # my_setting: str = "default"


@lru_cache
def get_settings() -> Settings:
    return Settings()
