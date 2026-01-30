"""
Unit tests for GetVague repository operation.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.exceptions import AIServiceError, ConfigurationError, InvalidRequestError
from app.repositories.excuse_generator.operations.get_vague import GetVague
from app.settings import Settings


class TestGetVagueInitialization:
    """Test suite for GetVague operation initialization."""

    def test_get_vague_initialization_valid_prompt(self):
        """Test GetVague initializes successfully with valid prompt."""
        # Arrange & Act
        operation = GetVague(prompt="Can you help me move?")

        # Assert
        assert operation is not None
        assert operation.prompt == "Can you help me move?"

    def test_get_vague_initialization_empty_prompt_raises_error(self):
        """Test GetVague raises InvalidRequestError for empty prompt."""
        # Act & Assert
        with pytest.raises(InvalidRequestError, match="Prompt cannot be empty"):
            GetVague(prompt="")

    def test_get_vague_initialization_whitespace_prompt_raises_error(self):
        """Test GetVague raises InvalidRequestError for whitespace-only prompt."""
        # Act & Assert
        with pytest.raises(InvalidRequestError, match="Prompt cannot be empty"):
            GetVague(prompt="   \n\t  ")


class TestGetVagueExecute:
    """Test suite for GetVague execute method."""

    @pytest.fixture
    def mock_settings(self):
        """Fixture providing mock Settings."""
        return Settings(
            POWERTOOLS_SERVICE_NAME="test-service",
            POWERTOOLS_LOG_LEVEL="INFO",
            POWERTOOLS_INJECT_LOG_CONTEXT=False,
            GOOGLE_API_KEY="test-api-key-12345",
        )

    @pytest.fixture
    def mock_repository(self, mock_settings):
        """Fixture providing mock repository with settings."""
        mock_repo = AsyncMock()
        mock_repo.settings = mock_settings
        mock_repo.agent = AsyncMock()
        return mock_repo

    @pytest.mark.anyio
    async def test_get_vague_execute_calls_pydantic_ai_agent(self, mock_repository):
        """Test that execute calls PydanticAI agent.run() with correct parameters."""
        # Arrange
        operation = GetVague(prompt="Can you help me move?")
        mock_result = MagicMock()
        mock_result.data = "I'd love to, but I'm swamped with a critical sprint."
        mock_repository.agent.run.return_value = mock_result

        # Act
        await operation.execute(mock_repository)

        # Assert
        mock_repository.agent.run.assert_awaited_once()
        call_args = mock_repository.agent.run.call_args
        assert call_args[0][0] == "Can you help me move?"
        assert "model_settings" in call_args[1]
        assert call_args[1]["model_settings"]["temperature"] == 0.7

    @pytest.mark.anyio
    async def test_get_vague_execute_returns_excuse_string(self, mock_repository):
        """Test that execute returns the generated excuse string."""
        # Arrange
        operation = GetVague(prompt="Want to grab coffee?")
        expected_excuse = (
            "I'd love to, but I'm currently dealing with some technical debt "
            "in our legacy infrastructure."
        )
        mock_result = MagicMock()
        mock_result.data = expected_excuse
        mock_repository.agent.run.return_value = mock_result

        # Act
        result = await operation.execute(mock_repository)

        # Assert
        assert result == expected_excuse
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.anyio
    async def test_get_vague_execute_handles_ai_errors(self, mock_repository):
        """Test that execute wraps AI exceptions in AIServiceError."""
        # Arrange
        operation = GetVague(prompt="Can you help me?")
        mock_repository.agent.run.side_effect = Exception("AI API failed")

        # Act & Assert
        with pytest.raises(AIServiceError, match="Failed to generate excuse"):
            await operation.execute(mock_repository)

    @pytest.mark.anyio
    async def test_get_vague_execute_missing_api_key_raises_config_error(
        self, mock_repository
    ):
        """Test that execute raises ConfigurationError when API key is missing."""
        # Arrange
        operation = GetVague(prompt="Can you help me?")
        mock_repository.settings.GOOGLE_API_KEY = ""

        # Act & Assert
        with pytest.raises(ConfigurationError, match="API key is not configured"):
            await operation.execute(mock_repository)

    @pytest.mark.anyio
    async def test_get_vague_execute_with_various_prompts(self, mock_repository):
        """Test execute with various prompt types."""
        # Arrange
        prompts = [
            "Can you help me move?",
            "Want to grab coffee tomorrow?",
            "Are you free this weekend?",
        ]
        mock_result = MagicMock()
        mock_result.data = "Generated excuse"
        mock_repository.agent.run.return_value = mock_result

        for prompt in prompts:
            # Act
            operation = GetVague(prompt=prompt)
            result = await operation.execute(mock_repository)

            # Assert
            assert isinstance(result, str)
            assert len(result) > 0

    @pytest.mark.anyio
    async def test_get_vague_execute_uses_correct_temperature(self, mock_repository):
        """Test that execute uses temperature of 0.7 in model settings."""
        # Arrange
        operation = GetVague(prompt="Test prompt")
        mock_result = MagicMock()
        mock_result.data = "Test excuse"
        mock_repository.agent.run.return_value = mock_result

        # Act
        await operation.execute(mock_repository)

        # Assert
        call_args = mock_repository.agent.run.call_args
        model_settings = call_args[1]["model_settings"]
        assert model_settings["temperature"] == 0.7
        assert model_settings["api_key"] == "test-api-key-12345"
