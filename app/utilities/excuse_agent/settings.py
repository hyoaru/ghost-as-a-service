"""Configuration settings for the Excuse Agent."""

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Excuse Agent configuration loaded from environment."""

    model_config = SettingsConfigDict(
        env_file=(".env"),
        case_sensitive=True,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    GEMINI_API_KEY: SecretStr = Field(default=..., min_length=1)
