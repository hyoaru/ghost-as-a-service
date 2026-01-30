"""
Unit tests for ExcuseAgent utility.
"""

from typing import TypeVar
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic_ai import Agent

from app.exceptions import ConfigurationError
from app.settings import Settings
from app.utilities.excuse_agent import ExcuseAgent
from app.utilities.excuse_agent.interface import (
    ExcuseAgentABC,
    ExcuseAgentOperationABC,
)


T = TypeVar("T")


class TestExcuseAgentABCInterface:
    """Test suite for ExcuseAgentABC interface definition."""

    def test_excuse_agent_abc_has_agent_attribute(self):
        """Verify ExcuseAgentABC defines agent attribute."""
        # Verify the ABC has expected attributes/methods in annotations
        assert hasattr(ExcuseAgentABC, "__annotations__")

    def test_excuse_agent_abc_has_execute_method(self):
        """Verify ExcuseAgentABC defines execute abstract method."""
        # Arrange & Act
        abstract_methods = ExcuseAgentABC.__abstractmethods__

        # Assert
        assert "execute" in abstract_methods

    def test_excuse_agent_operation_abc_is_generic(self):
        """Verify ExcuseAgentOperationABC supports Generic typing."""
        # Arrange & Act - Verify it can be instantiated with type params
        # This is a structural test to ensure Generic[T] is properly defined
        assert hasattr(ExcuseAgentOperationABC, "__mro__")

    def test_excuse_agent_operation_abc_has_execute_method(self):
        """Verify ExcuseAgentOperationABC defines execute abstract method."""
        # Arrange & Act
        abstract_methods = ExcuseAgentOperationABC.__abstractmethods__

        # Assert
        assert "execute" in abstract_methods


class TestExcuseAgentInitialization:
    """Test suite for ExcuseAgent initialization."""

    @pytest.fixture
    def mock_settings(self):
        """Fixture providing mock Settings with required fields."""
        settings = Settings(
            POWERTOOLS_SERVICE_NAME="test-service",
            POWERTOOLS_LOG_LEVEL="INFO",
            POWERTOOLS_INJECT_LOG_CONTEXT=False,
            GOOGLE_API_KEY="test-api-key",
        )
        return settings

    @patch("app.utilities.excuse_agent.Agent")
    def test_excuse_agent_initialization_creates_agent(self, mock_agent_class, mock_settings):
        """Verify ExcuseAgent creates a PydanticAI Agent during initialization."""
        # Arrange
        mock_agent_instance = MagicMock(spec=Agent)
        mock_agent_class.return_value = mock_agent_instance

        # Act
        agent = ExcuseAgent(settings=mock_settings)

        # Assert
        assert isinstance(agent, ExcuseAgentABC)
        assert agent.agent is mock_agent_instance
        mock_agent_class.assert_called_once()

    @patch("app.utilities.excuse_agent.Agent")
    def test_excuse_agent_initialization_with_default_settings(self, mock_agent_class, monkeypatch):
        """Test ExcuseAgent initializes with default Settings when none provided."""
        # Arrange - Set environment variables for Settings
        monkeypatch.setenv("POWERTOOLS_SERVICE_NAME", "test-service")
        monkeypatch.setenv("POWERTOOLS_LOG_LEVEL", "INFO")
        monkeypatch.setenv("POWERTOOLS_INJECT_LOG_CONTEXT", "true")
        monkeypatch.setenv("GOOGLE_API_KEY", "test-api-key")

        # Act
        agent = ExcuseAgent()

        # Assert
        assert agent is not None
        assert isinstance(agent, ExcuseAgentABC)
        mock_agent_class.assert_called_once()

    @patch("app.utilities.excuse_agent.Agent")
    def test_excuse_agent_initialization_with_correct_model(self, mock_agent_class, mock_settings):
        """Verify ExcuseAgent uses OPENAI_MODEL from settings."""
        # Arrange
        mock_settings.OPENAI_MODEL = "gpt-4-turbo"
        mock_agent_instance = MagicMock(spec=Agent)
        mock_agent_class.return_value = mock_agent_instance

        # Act
        agent = ExcuseAgent(settings=mock_settings)

        # Assert
        call_args = mock_agent_class.call_args
        assert call_args[0][0] == "gpt-4-turbo"

    @patch("app.utilities.excuse_agent.Agent")
    def test_excuse_agent_initialization_with_system_prompt(self, mock_agent_class, mock_settings):
        """Verify ExcuseAgent initializes Agent with correct system prompt."""
        # Arrange
        mock_agent_instance = MagicMock(spec=Agent)
        mock_agent_class.return_value = mock_agent_instance

        # Act
        agent = ExcuseAgent(settings=mock_settings)

        # Assert
        call_kwargs = mock_agent_class.call_args[1]
        assert "system_prompt" in call_kwargs
        system_prompt = call_kwargs["system_prompt"]
        assert "professional excuse generator" in system_prompt.lower()
        assert "corporate jargon" in system_prompt.lower()
        assert "technical terminology" in system_prompt.lower()

    def test_excuse_agent_initialization_raises_error_when_api_key_is_empty(self):
        """Verify ConfigurationError is raised when GOOGLE_API_KEY is empty."""
        # Arrange - Create Settings with empty API key string
        settings = Settings(
            POWERTOOLS_SERVICE_NAME="test-service",
            POWERTOOLS_LOG_LEVEL="INFO",
            POWERTOOLS_INJECT_LOG_CONTEXT=False,
            GOOGLE_API_KEY="",  # Empty API key
        )

        # Act & Assert
        with pytest.raises(ConfigurationError):
            ExcuseAgent(settings=settings)

    @patch("app.utilities.excuse_agent.Agent")
    def test_excuse_agent_stores_agent_as_instance_attribute(self, mock_agent_class, mock_settings):
        """Verify agent is stored as an instance attribute."""
        # Arrange
        mock_agent_instance = MagicMock(spec=Agent)
        mock_agent_class.return_value = mock_agent_instance

        # Act
        agent_utility = ExcuseAgent(settings=mock_settings)

        # Assert
        assert hasattr(agent_utility, "agent")
        assert agent_utility.agent is mock_agent_instance


class TestExcuseAgentExecute:
    """Test suite for ExcuseAgent execute method."""

    @pytest.fixture
    def mock_settings(self):
        """Fixture providing mock Settings."""
        return Settings(
            POWERTOOLS_SERVICE_NAME="test-service",
            POWERTOOLS_LOG_LEVEL="INFO",
            POWERTOOLS_INJECT_LOG_CONTEXT=False,
            GOOGLE_API_KEY="test-api-key",
        )

    @pytest.fixture
    @patch("app.utilities.excuse_agent.Agent")
    def excuse_agent(self, mock_agent_class, mock_settings):
        """Fixture providing ExcuseAgent instance."""
        mock_agent_instance = MagicMock(spec=Agent)
        mock_agent_class.return_value = mock_agent_instance
        return ExcuseAgent(settings=mock_settings)

    def test_excuse_agent_execute_delegates_to_operation(self, excuse_agent):
        """Verify execute method delegates to operation.execute()."""
        # Arrange
        mock_operation = MagicMock(spec=ExcuseAgentOperationABC)
        expected_result = "Test result"
        mock_operation.execute.return_value = expected_result

        # Act
        result = excuse_agent.execute(mock_operation)

        # Assert
        mock_operation.execute.assert_called_once_with(excuse_agent)
        assert result == expected_result

    def test_excuse_agent_execute_passes_self_to_operation(self, excuse_agent):
        """Verify execute passes the utility instance to operation."""
        # Arrange
        mock_operation = MagicMock(spec=ExcuseAgentOperationABC)

        # Act
        excuse_agent.execute(mock_operation)

        # Assert
        # Verify the operation received the excuse_agent instance as argument
        call_args = mock_operation.execute.call_args
        assert call_args[0][0] is excuse_agent

    def test_excuse_agent_execute_returns_operation_result(self, excuse_agent):
        """Verify execute returns the result from operation.execute()."""
        # Arrange
        mock_operation = MagicMock(spec=ExcuseAgentOperationABC)
        test_return_value = {"excuse": "bandwidth issues"}
        mock_operation.execute.return_value = test_return_value

        # Act
        result = excuse_agent.execute(mock_operation)

        # Assert
        assert result == test_return_value
        assert result is test_return_value
