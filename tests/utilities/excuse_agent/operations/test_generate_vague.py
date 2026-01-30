"""
Unit tests for GenerateVague operation.
"""

import pytest

from app.utilities.excuse_agent.operations.generate_vague import GenerateVague


class TestGenerateVague:
    """Test suite for GenerateVague operation."""

    async def test_execute_generates_excuse(self, excuse_agent):
        """Test GenerateVague.execute generates an excuse string."""
        # Arrange
        operation = GenerateVague(request="Can you help me move this weekend?")
        expected_excuse = "I'm swamped with a critical infrastructure migration."
        excuse_agent.agent.run.return_value.output = expected_excuse

        # Act
        result = await operation.execute(excuse_agent)

        # Assert
        assert result == expected_excuse
        assert isinstance(result, str)

    async def test_execute_calls_agent_with_correct_prompt(self, excuse_agent):
        """Test operation calls agent with the correct prompt."""
        # Arrange
        request = "Want to grab dinner tonight?"
        operation = GenerateVague(request=request)
        excuse_agent.agent.run.return_value.output = "Excuse text"

        # Act
        await operation.execute(excuse_agent)

        # Assert
        excuse_agent.agent.run.assert_awaited_once()
        call_args = excuse_agent.agent.run.call_args
        prompt = call_args[0][0]

        # Verify prompt contains expected keywords
        assert request in prompt
        assert "Technical Fog" in prompt
        assert "vague" in prompt
        assert "jargon" in prompt
        assert "professional" in prompt

    async def test_execute_returns_string_type(self, excuse_agent):
        """Test execute always returns a string."""
        # Arrange
        operation = GenerateVague(request="Join us for game night?")
        excuse_agent.agent.run.return_value.output = "Any excuse"

        # Act
        result = await operation.execute(excuse_agent)

        # Assert
        assert isinstance(result, str)

    async def test_execute_with_empty_response(self, excuse_agent):
        """Test handling when agent returns empty string."""
        # Arrange
        operation = GenerateVague(request="Come to the party?")
        excuse_agent.agent.run.return_value.output = ""

        # Act
        result = await operation.execute(excuse_agent)

        # Assert
        assert result == ""
        assert isinstance(result, str)

    async def test_execute_multiple_times_returns_different_results(self, excuse_agent):
        """Test multiple executions can produce different results."""
        # Arrange
        operation1 = GenerateVague(request="First request")
        operation2 = GenerateVague(request="Second request")
        excuse_agent.agent.run.return_value.output = "First excuse"

        # Act
        result1 = await operation1.execute(excuse_agent)

        excuse_agent.agent.run.return_value.output = "Second excuse"
        result2 = await operation2.execute(excuse_agent)

        # Assert
        assert result1 == "First excuse"
        assert result2 == "Second excuse"
        assert excuse_agent.agent.run.await_count == 2


class TestGenerateVagueErrorHandling:
    """Test suite for GenerateVague error scenarios."""

    async def test_execute_propagates_agent_errors(self, excuse_agent):
        """Test operation propagates errors from agent."""
        # Arrange
        operation = GenerateVague(request="Error test request")
        excuse_agent.agent.run.side_effect = Exception("Model API failed")

        # Act & Assert
        with pytest.raises(Exception, match="Model API failed"):
            await operation.execute(excuse_agent)

    async def test_execute_with_none_utility(self):
        """Test operation fails gracefully with None utility."""
        # Arrange
        operation = GenerateVague(request="None utility test")

        # Act & Assert
        with pytest.raises(AttributeError):
            await operation.execute(None)


class TestGenerateVagueIntegration:
    """Integration tests for GenerateVague with real-like scenarios."""

    async def test_full_workflow_with_excuse_agent(self, excuse_agent):
        """Test complete workflow: create operation, execute, get result."""
        # Arrange
        excuse_agent.agent.run.return_value.output = (
            "Sorry, I'm dealing with a critical DNS propagation issue "
            "and our CDN infrastructure needs immediate attention."
        )

        # Act
        operation = GenerateVague(request="Can you help with the move?")
        result = await excuse_agent.execute(operation)

        # Assert
        assert "critical" in result.lower()
        assert len(result) > 20  # Should be a reasonable length
        excuse_agent.agent.run.assert_awaited_once()

    @pytest.mark.parametrize(
        "mock_response",
        [
            "I'm in the middle of a massive data migration.",
            "My bandwidth is currently throttled by legacy infrastructure issues.",
            "We're experiencing unprecedented technical debt consolidation.",
        ],
    )
    async def test_various_vague_excuses(self, excuse_agent, mock_response):
        """Test operation handles various excuse formats."""
        # Arrange
        operation = GenerateVague(request="Various excuse test")
        excuse_agent.agent.run.return_value.output = mock_response

        # Act
        result = await operation.execute(excuse_agent)

        # Assert
        assert result == mock_response
        assert isinstance(result, str)
