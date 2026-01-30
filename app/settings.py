"""
Application settings and configuration management.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Configuration is loaded from .env file and environment variables.
    All field names are case-sensitive.
    """

    model_config = SettingsConfigDict(
        env_file=(".env"),
        case_sensitive=True,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Lambda Powertools Configuration
    POWERTOOLS_SERVICE_NAME: str = Field(
        ..., description="Name of the Lambda service for Powertools logging"
    )
    POWERTOOLS_LOG_LEVEL: str = Field(
        ..., description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
    POWERTOOLS_INJECT_LOG_CONTEXT: bool = Field(
        ..., description="Whether to inject Lambda context into logs"
    )

    # AI Configuration
    GOOGLE_API_KEY: str = Field(..., description="API key for Google AI (Gemini) via PydanticAI")
