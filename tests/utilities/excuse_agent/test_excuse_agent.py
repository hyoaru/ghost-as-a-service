"""
Unit tests for ExcuseAgent utility.
"""

import pytest

from app.utilities.excuse_agent import ExcuseAgent
from app.utilities.excuse_agent.operations.generate_vague import GenerateVague


class TestExcuseAgentInitialization:
    """Test suite for ExcuseAgent initialization."""

    def test_initialization_with_defaults(self, mock_settings):
        """Test ExcuseAgent initializes with default agent when none provided."""
        # Act
        agent = ExcuseAgent(settings=mock_settings)

        # Assert
        assert agent.agent is not None
        assert agent.settings == mock_settings
        assert agent.instructions is not None
        assert len(agent.instructions) > 0

    def test_initialization_with_custom_agent(self, mock_agent, mock_settings):
        """Test ExcuseAgent initializes with provided agent."""
        # Act
        agent = ExcuseAgent(agent=mock_agent, settings=mock_settings)

        # Assert
        assert agent.agent == mock_agent
        assert agent.settings == mock_settings

    def test_instructions_loaded_from_file(self, mock_agent, mock_settings):
        """Test system instructions are loaded from instructions.md."""
        # Act
        agent = ExcuseAgent(agent=mock_agent, settings=mock_settings)

        # Assert
        assert "Excuse Architect" in agent.instructions
        assert "Objective" in agent.instructions
        assert len(agent.instructions) > 100


class TestExcuseAgentExecution:
    """Test suite for ExcuseAgent execute method."""

    async def test_execute_delegates_to_operation(self, excuse_agent):
        """Test execute method properly delegates to operation."""
        # Arrange
        operation = GenerateVague(request="Test request")
        expected_output = "Test excuse generated successfully"
        excuse_agent.agent.run.return_value.output = expected_output

        # Act
        result = await excuse_agent.execute(operation)

        # Assert
        assert result == expected_output
        excuse_agent.agent.run.assert_awaited_once()

    async def test_execute_passes_self_to_operation(self, excuse_agent, mocker):
        """Test execute passes utility instance to operation."""
        # Arrange
        operation = GenerateVague(request="Self test request")
        spy = mocker.spy(operation, "execute")

        # Act
        await excuse_agent.execute(operation)

        # Assert
        spy.assert_awaited_once_with(excuse_agent)

    async def test_execute_with_multiple_operations(self, excuse_agent):
        """Test execute handles multiple sequential operations."""
        # Arrange
        operation1 = GenerateVague(request="First request")
        operation2 = GenerateVague(request="Second request")
        excuse_agent.agent.run.return_value.output = "First excuse"

        # Act
        result1 = await excuse_agent.execute(operation1)

        excuse_agent.agent.run.return_value.output = "Second excuse"
        result2 = await excuse_agent.execute(operation2)

        # Assert
        assert result1 == "First excuse"
        assert result2 == "Second excuse"
        assert excuse_agent.agent.run.await_count == 2


class TestExcuseAgentErrorHandling:
    """Test suite for error handling scenarios."""

    async def test_execute_propagates_agent_errors(self, excuse_agent):
        """Test execute propagates errors from agent.run."""
        # Arrange
        operation = GenerateVague(request="Error test")
        excuse_agent.agent.run.side_effect = Exception("API error")

        # Act & Assert
        with pytest.raises(Exception, match="API error"):
            await excuse_agent.execute(operation)

    async def test_execute_with_invalid_operation(self, excuse_agent):
        """Test execute handles invalid operation gracefully."""
        # Arrange
        invalid_operation = None

        # Act & Assert
        with pytest.raises(AttributeError):
            await excuse_agent.execute(invalid_operation)
