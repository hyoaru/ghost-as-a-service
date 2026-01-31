"""Excuse Agent utility for generating vague professional excuses.

This module provides a PydanticAI-based agent that generates contextually
appropriate, vague excuses filled with corporate jargon.
"""

from pathlib import Path
from typing import Optional, TypeVar

from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel

from .interface import ExcuseAgentABC
from .operations.interface import ExcuseAgentOperationABC
from .settings import Settings

T = TypeVar("T")

__all__ = ["ExcuseAgent", "ExcuseAgentABC", "Settings"]


class ExcuseAgent(ExcuseAgentABC):
    """Excuse generation agent wrapping PydanticAI with Google Gemini model.

    Initializes with system instructions and manages the LLM interaction
    for generating vague excuses.
    """

    agent: Agent
    instructions: str
    settings: Settings

    def __init__(
        self,
        agent: Optional[Agent] = None,
        settings: Optional[Settings] = None,
    ):
        """Initialize the ExcuseAgent with optional overrides.

        Args:
            agent: Optional PydanticAI Agent instance. If not provided,
                creates a new one with Gemini model.
            settings: Optional Settings instance. If not provided,
                loads from environment.
        """
        with open(Path(__file__).parent / "instructions.txt", "r") as f:
            self.instructions = f.read()

        self.settings = settings or Settings()

        # GoogleModel reads API key from GOOGLE_API_KEY or GEMINI_API_KEY env var
        self.agent = agent or Agent(
            instructions=self.instructions,
            deps_type=None,
            output_type=str,
            model=GoogleModel("gemini-2.5-flash-lite"),
        )

    async def execute(self, operation: ExcuseAgentOperationABC[T]) -> T:
        """Execute an operation using the Excuse Agent.

        Args:
            operation: The operation to execute.

        Returns:
            The result of the operation execution.
        """
        return await operation.execute(self)
