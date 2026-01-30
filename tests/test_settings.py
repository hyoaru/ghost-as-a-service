"""
Tests for application settings configuration.
"""

import pytest
from pydantic import ValidationError


def test_settings_loads_from_env(monkeypatch):
    """
    Test that Settings class loads configuration from environment variables.

    Verifies:
        - Settings reads from environment variables correctly
        - All required fields are populated
        - Values match what was set in environment
    """
    # Arrange
    monkeypatch.setenv("POWERTOOLS_SERVICE_NAME", "test-service")
    monkeypatch.setenv("POWERTOOLS_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("POWERTOOLS_INJECT_LOG_CONTEXT", "true")
    monkeypatch.setenv("GOOGLE_API_KEY", "test-api-key-12345")

    # Act
    from app.settings import Settings

    settings = Settings()

    # Assert
    assert settings.POWERTOOLS_SERVICE_NAME == "test-service"
    assert settings.POWERTOOLS_LOG_LEVEL == "DEBUG"
    assert settings.POWERTOOLS_INJECT_LOG_CONTEXT is True
    assert settings.GOOGLE_API_KEY == "test-api-key-12345"


def test_settings_validation_fails_missing_required(monkeypatch):
    """
    Test that Settings validation fails when required fields are missing.

    Verifies:
        - ValidationError is raised when required field is missing
        - Error message indicates which field is missing
    """
    # Arrange - Only set some required fields
    monkeypatch.setenv("POWERTOOLS_SERVICE_NAME", "test-service")
    monkeypatch.setenv("POWERTOOLS_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("POWERTOOLS_INJECT_LOG_CONTEXT", "true")
    # Intentionally omit GOOGLE_API_KEY

    # Act & Assert
    from app.settings import Settings

    with pytest.raises(ValidationError) as exc_info:
        Settings()

    # Verify the error mentions the missing field
    assert "GOOGLE_API_KEY" in str(exc_info.value)


def test_settings_boolean_conversion(monkeypatch):
    """
    Test that Settings correctly converts string boolean values.

    Verifies:
        - String "true"/"false" are converted to boolean
        - Case-insensitive conversion works
    """
    # Arrange - Test False conversion
    monkeypatch.setenv("POWERTOOLS_SERVICE_NAME", "test-service")
    monkeypatch.setenv("POWERTOOLS_LOG_LEVEL", "INFO")
    monkeypatch.setenv("POWERTOOLS_INJECT_LOG_CONTEXT", "False")
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key")

    # Act
    from app.settings import Settings

    settings = Settings()

    # Assert
    assert settings.POWERTOOLS_INJECT_LOG_CONTEXT is False

    # Arrange - Test True conversion
    monkeypatch.setenv("POWERTOOLS_INJECT_LOG_CONTEXT", "true")

    # Act
    settings_true = Settings()

    # Assert
    assert settings_true.POWERTOOLS_INJECT_LOG_CONTEXT is True


def test_settings_case_sensitive(monkeypatch):
    """
    Test that Settings configuration is case-sensitive.

    Verifies:
        - Environment variables must match exact case
        - Lowercase variants don't work
    """
    # Arrange - Use lowercase (wrong case)
    monkeypatch.setenv("powertools_service_name", "test-service")
    monkeypatch.setenv("powertools_log_level", "DEBUG")
    monkeypatch.setenv("powertools_inject_log_context", "true")
    monkeypatch.setenv("google_api_key", "test-key")

    # Act & Assert
    from app.settings import Settings

    with pytest.raises(ValidationError):
        Settings()
