"""
Unit tests for the GenerateVague operation.
"""

from unittest.mock import AsyncMock

import pytest

from app.exceptions import AIServiceError, ConfigurationError, InvalidRequestError
from app.repositories.excuse_generator import ExcuseRepositoryABC, GetVague
from app.services.excuse_generator import ExcuseGeneratorABC
from app.services.excuse_generator.operations import GenerateVague


class TestGenerateVagueInitialization:
    """Test GenerateVague operation initialization."""

    def test_generate_vague_initialization_valid_request(self):
        """Test that GenerateVague can be initialized with a valid request."""
        operation = GenerateVague(request="Can you help me move?")
        assert operation.request == "Can you help me move?"

    def test_generate_vague_initialization_empty_request_raises_error(self):
        """Test that empty request raises InvalidRequestError."""
        with pytest.raises(InvalidRequestError, match="Request cannot be empty"):
            GenerateVague(request="")

    def test_generate_vague_initialization_whitespace_request_raises_error(self):
        """Test that whitespace-only request raises InvalidRequestError."""
        with pytest.raises(InvalidRequestError, match="Request cannot be empty"):
            GenerateVague(request="   \t\n  ")

    def test_generate_vague_initialization_strips_whitespace(self):
        """Test that leading/trailing whitespace is stripped from request."""
        operation = GenerateVague(request="  Can you help me move?  \n")
        assert operation.request == "Can you help me move?"


class TestGenerateVagueExecute:
    """Test GenerateVague operation execution."""

    @pytest.fixture
    def mock_service(self):
        """Create a mock ExcuseGenerator service."""
        service = AsyncMock(spec=ExcuseGeneratorABC)
        service.excuse_repository = AsyncMock(spec=ExcuseRepositoryABC)
        return service

    @pytest.mark.anyio
    async def test_generate_vague_execute_calls_repository(self, mock_service):
        """Test that execute calls repository with GetVague operation."""
        operation = GenerateVague(request="Want to grab coffee?")
        mock_service.excuse_repository.execute.return_value = "I'm swamped with work"
        await operation.execute(mock_service)
        mock_service.excuse_repository.execute.assert_awaited_once()
        call_args = mock_service.excuse_repository.execute.call_args
        assert isinstance(call_args[0][0], GetVague)

    @pytest.mark.anyio
    async def test_generate_vague_execute_returns_excuse(self, mock_service):
        """Test that execute returns the generated excuse string."""
        operation = GenerateVague(request="Want to grab coffee?")
        expected_excuse = (
            "I'd love to, but I'm currently dealing with some technical debt "
            "and need to refactor my bandwidth allocation."
        )
        mock_service.excuse_repository.execute.return_value = expected_excuse
        result = await operation.execute(mock_service)
        assert result == expected_excuse

    @pytest.mark.anyio
    async def test_generate_vague_execute_propagates_ai_errors(self, mock_service):
        """Test that execute propagates AIServiceError from repository."""
        operation = GenerateVague(request="Can you help?")
        mock_service.excuse_repository.execute.side_effect = AIServiceError(
            "AI service unavailable"
        )
        with pytest.raises(AIServiceError, match="AI service unavailable"):
            await operation.execute(mock_service)

    @pytest.mark.anyio
    async def test_generate_vague_execute_propagates_config_errors(self, mock_service):
        """Test that execute propagates ConfigurationError from repository."""
        operation = GenerateVague(request="Are you free?")
        mock_service.excuse_repository.execute.side_effect = ConfigurationError("Missing API key")
        with pytest.raises(ConfigurationError, match="Missing API key"):
            await operation.execute(mock_service)

    @pytest.mark.anyio
    async def test_generate_vague_execute_with_various_requests(self, mock_service):
        """Test execute with different types of requests."""
        requests = [
            "Can you review my code?",
            "Want to join the meeting?",
            "Are you available for lunch?",
        ]
        mock_service.excuse_repository.execute.return_value = "Sorry, I'm busy"

        for req in requests:
            operation = GenerateVague(request=req)
            result = await operation.execute(mock_service)
            assert result == "Sorry, I'm busy"

    @pytest.mark.anyio
    async def test_generate_vague_execute_passes_correct_prompt_to_repository(self, mock_service):
        """Test that the correct prompt is passed to the repository."""
        request_text = "Can you help me move this weekend?"
        operation = GenerateVague(request=request_text)
        mock_service.excuse_repository.execute.return_value = "I'm busy"
        await operation.execute(mock_service)
        call_args = mock_service.excuse_repository.execute.call_args[0][0]
        assert isinstance(call_args, GetVague)
        assert call_args.prompt == request_text
