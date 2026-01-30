"""Tests for the Lambda handler entry point."""

from unittest.mock import Mock, AsyncMock, patch
import pytest
from aws_lambda_powertools.utilities.typing import LambdaContext

from app import handler, main
from app.models import EventModel


class TestLambdaHandler:
    """Test cases for the Lambda handler function."""

    @pytest.fixture
    def lambda_context(self) -> LambdaContext:
        """Create a mock Lambda context."""
        context = Mock(spec=LambdaContext)
        context.request_id = "test-request-id-12345"
        context.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test"
        return context

    @pytest.fixture
    def valid_event(self) -> dict:
        """Create a valid Lambda event."""
        return {"request": "Can you help me move this weekend?"}

    @patch("app.services.excuse_generator.ExcuseGeneratorService")
    def test_handler_with_valid_event(
        self, mock_service_class, valid_event: dict, lambda_context: LambdaContext
    ):
        """Test handler successfully processes a valid event."""
        # Given: Mocked service returns an excuse
        mock_service = AsyncMock()
        mock_service.execute = AsyncMock(
            return_value="Sorry, I'm in the middle of a massive data migration."
        )
        mock_service_class.return_value = mock_service

        # When: Handler is called with a valid event
        result = handler(valid_event, lambda_context)

        # Then: Result should contain an excuse
        assert "excuse" in result
        assert isinstance(result["excuse"], str)
        assert len(result["excuse"]) > 0

    def test_handler_with_empty_request(self, lambda_context: LambdaContext):
        """Test handler rejects empty request."""
        # Given: An event with empty request
        event = {"request": ""}

        # When: Handler is called
        result = handler(event, lambda_context)

        # Then: Should return error response
        assert "statusCode" in result
        assert result["statusCode"] == 400
        assert "body" in result
        assert "error" in result["body"]

    def test_handler_with_whitespace_request(self, lambda_context: LambdaContext):
        """Test handler rejects whitespace-only request."""
        # Given: An event with whitespace request
        event = {"request": "   "}

        # When: Handler is called
        result = handler(event, lambda_context)

        # Then: Should return error response
        assert "statusCode" in result
        assert result["statusCode"] == 400


class TestMainFunction:
    """Test cases for the main async function."""

    @pytest.fixture
    def lambda_context(self) -> LambdaContext:
        """Create a mock Lambda context."""
        context = Mock(spec=LambdaContext)
        context.request_id = "test-request-id-67890"
        return context

    @pytest.mark.asyncio
    @patch("app.services.excuse_generator.ExcuseGeneratorService")
    async def test_main_with_valid_request(self, mock_service_class, lambda_context: LambdaContext):
        """Test main function processes valid request successfully."""
        # Given: Mocked service returns an excuse
        mock_service = AsyncMock()
        mock_service.execute = AsyncMock(
            return_value="Sorry, I'm experiencing unprecedented technical debt consolidation."
        )
        mock_service_class.return_value = mock_service

        # Given: A valid event model
        event = EventModel(request="Are you free for dinner tonight?")

        # When: Main function is called
        result = await main(event, lambda_context)

        # Then: Should return successful response
        assert "excuse" in result
        assert isinstance(result["excuse"], str)

    @pytest.mark.asyncio
    @patch("app.services.excuse_generator.ExcuseGeneratorService")
    async def test_main_returns_excuse_response_dict(
        self, mock_service_class, lambda_context: LambdaContext
    ):
        """Test main function returns ExcuseResponse as dict."""
        # Given: Mocked service returns an excuse
        mock_service = AsyncMock()
        mock_service.execute = AsyncMock(
            return_value="My bandwidth is currently throttled by legacy infrastructure."
        )
        mock_service_class.return_value = mock_service

        # Given: A valid event model
        event = EventModel(request="Can you review my code?")

        # When: Main function is called
        result = await main(event, lambda_context)

        # Then: Should return dict with excuse
        assert isinstance(result, dict)
        assert "excuse" in result

    @pytest.mark.asyncio
    async def test_main_logs_request(self, lambda_context: LambdaContext, caplog):
        """Test main function logs the incoming request."""
        # Given: A valid event model with mocked service
        with patch("app.services.excuse_generator.ExcuseGeneratorService") as mock_service_class:
            mock_service = AsyncMock()
            mock_service.execute = AsyncMock(return_value="Test excuse")
            mock_service_class.return_value = mock_service

            event = EventModel(request="Want to grab coffee?")

            # When: Main function is called
            await main(event, lambda_context)

            # Then: Should log the request
            assert any(
                "Processing excuse generation request" in record.message
                for record in caplog.records
            )

    @pytest.mark.asyncio
    async def test_main_handles_invalid_request_error(self, lambda_context: LambdaContext):
        """Test main function handles invalid request gracefully."""
        # Given: An event model with empty request (will cause InvalidRequestError)
        event = EventModel(request="")

        # When: Main function is called
        result = await main(event, lambda_context)

        # Then: Should return 400 error response
        assert result["statusCode"] == 400
        assert "error" in result["body"]
        assert result["body"]["error"] == "Invalid request"

    @pytest.mark.asyncio
    @patch("app.services.excuse_generator.ExcuseGeneratorService")
    async def test_main_with_various_requests(
        self, mock_service_class, lambda_context: LambdaContext
    ):
        """Test main function with different request types."""
        # Given: Mocked service returns different excuses
        mock_service = AsyncMock()
        excuses = [
            "Sorry, massive data migration in progress.",
            "Bandwidth throttled by legacy infrastructure.",
            "Experiencing unprecedented technical debt.",
            "Currently optimizing our CI/CD pipeline.",
        ]
        mock_service.execute = AsyncMock(side_effect=excuses)
        mock_service_class.return_value = mock_service

        requests = [
            "Can you help me move this weekend?",
            "Want to grab coffee tomorrow?",
            "Are you free for a quick call?",
            "Can you review my code?",
        ]

        for request_text in requests:
            # Given: A valid event model
            event = EventModel(request=request_text)

            # When: Main function is called
            result = await main(event, lambda_context)

            # Then: Should return successful response with excuse
            assert "excuse" in result
            assert isinstance(result["excuse"], str)
            assert len(result["excuse"]) > 0
