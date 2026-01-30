"""
Excuse agent utility for generating creative excuses using PydanticAI.

This utility wraps the PydanticAI Agent and provides a clean interface
for generating plausible-sounding excuses with corporate jargon.
"""

from typing import Optional

from pydantic_ai import Agent

from app.exceptions import ConfigurationError
from app.settings import Settings
from app.utilities.excuse_agent.interface import (
    ExcuseAgentABC,
    ExcuseAgentOperationABC,
)

T = type[ExcuseAgentOperationABC]


class ExcuseAgent(ExcuseAgentABC):
    """
    Concrete implementation of ExcuseAgentABC.

    This utility creates and manages a PydanticAI Agent configured to
    generate plausible but meaningless excuses using corporate jargon
    and technical terminology.

    This is a Type A Infrastructure (Stateful) utility that maintains
    the agent instance and delegates operations to it.

    Attributes:
        agent: PydanticAI Agent for generating excuses.
        settings: Application settings including API keys and model configuration.
    """

    agent: Agent
    settings: Settings

    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize the ExcuseAgent.

        Creates a PydanticAI Agent with a system prompt configured to
        generate creative, vague excuses using corporate terminology.

        Args:
            settings: Application settings. If None, loads from environment.

        Raises:
            ConfigurationError: If GOOGLE_API_KEY is missing or empty from settings.
        """
        self.settings = settings or Settings()

        # Verify required API key is configured
        if not self.settings.GOOGLE_API_KEY:
            raise ConfigurationError(
                "GOOGLE_API_KEY is required but not configured. "
                "Please set the GOOGLE_API_KEY environment variable."
            )

        # Create PydanticAI Agent with system prompt
        system_prompt = (
            "You are a professional excuse generator. Your job is to create vague, "
            "plausible-sounding excuses that blend corporate jargon with technical "
            "terminology. The excuses should sound busy and important but be completely "
            "meaningless upon close inspection.\n\n"
            "Requirements:\n"
            "- Keep responses concise (1-3 sentences)\n"
            "- Mix business and technical terms naturally\n"
            "- Sound apologetic but professional\n"
            "- Avoid specific commitments\n"
            "- Make it sound urgent but vague"
        )

        # Get model from settings
        model = self.settings.OPENAI_MODEL

        self.agent = Agent(
            model,
            system_prompt=system_prompt,
        )

    def execute(self, operation: ExcuseAgentOperationABC[T]) -> T:
        """
        Execute an operation against this agent utility.

        Following the Type A Infrastructure pattern, this passes self to the
        operation so it can access the agent and other resources.

        Args:
            operation: The operation to execute.

        Returns:
            T: The result of the operation.
        """
        return operation.execute(self)


__all__ = ["ExcuseAgent", "ExcuseAgentABC", "ExcuseAgentOperationABC"]
