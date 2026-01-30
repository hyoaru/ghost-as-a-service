"""
Unit tests for ExcuseAgent Settings.
"""

import os

import pytest
from pydantic import ValidationError

from app.utilities.excuse_agent.settings import Settings


class TestSettings:
    """Test suite for Settings configuration."""

    def test_settings_loads_from_environment(self):
        """Test Settings loads GEMINI_API_KEY from environment."""
        # Arrange
        os.environ["GEMINI_API_KEY"] = "test_key_123"

        # Act
        settings = Settings()

        # Assert
        assert settings.GEMINI_API_KEY.get_secret_value() == "test_key_123"

        # Cleanup
        os.environ.pop("GEMINI_API_KEY")

    def test_settings_requires_api_key(self, monkeypatch):
        """Test Settings raises error when API key is missing."""
        # Arrange - ensure no API key in environment
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)

        # Act & Assert
        with pytest.raises(ValidationError):
            Settings(_env_file=None)

    def test_settings_rejects_empty_api_key(self):
        """Test Settings rejects empty API key."""
        # Arrange
        os.environ["GEMINI_API_KEY"] = ""

        # Act & Assert
        with pytest.raises(ValidationError):
            Settings()

        # Cleanup
        os.environ.pop("GEMINI_API_KEY", None)

    def test_settings_api_key_is_secret(self):
        """Test API key is stored as SecretStr."""
        # Arrange
        os.environ["GEMINI_API_KEY"] = "secret_key"
        settings = Settings()

        # Act - convert to string should show masked value
        api_key_repr = str(settings.GEMINI_API_KEY)

        # Assert
        assert "**********" in api_key_repr or "SecretStr" in api_key_repr
        assert "secret_key" not in api_key_repr

        # Cleanup
        os.environ.pop("GEMINI_API_KEY")

    def test_settings_ignores_extra_env_vars(self):
        """Test Settings ignores unrelated environment variables."""
        # Arrange
        os.environ["GEMINI_API_KEY"] = "test_key"
        os.environ["RANDOM_VAR"] = "should_be_ignored"

        # Act
        settings = Settings()

        # Assert - should not raise error due to extra var
        assert settings.GEMINI_API_KEY.get_secret_value() == "test_key"
        assert not hasattr(settings, "RANDOM_VAR")

        # Cleanup
        os.environ.pop("GEMINI_API_KEY")
        os.environ.pop("RANDOM_VAR")
