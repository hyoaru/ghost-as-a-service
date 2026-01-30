"""Configuration settings for the Agent Excuse Repository."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Agent implementation configuration loaded from environment.

    This implementation uses the ExcuseAgent utility to generate
    excuses dynamically via LLM.
    """

    model_config = SettingsConfigDict(
        env_file=(".env"),
        case_sensitive=True,
        env_file_encoding="utf-8",
        extra="ignore",
    )
