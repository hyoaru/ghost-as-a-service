"""
Concrete implementation of ExcuseRepository.

This repository handles interactions with PydanticAI for generating vague excuses.
"""

from typing import Optional

from pydantic_ai import Agent

from app.repositories.excuse_generator.interface import (
    ExcuseRepositoryABC,
    RepositoryOperationABC,
)
from app.settings import Settings

T = type[RepositoryOperationABC]


class ExcuseRepository(ExcuseRepositoryABC):
    """
    Repository for generating vague excuses using PydanticAI.

    This repository creates and manages a PydanticAI Agent configured to
    generate plausible but meaningless excuses using corporate jargon.

    Attributes:
        settings: Application settings including API keys.
        agent: PydanticAI Agent for generating excuses.
    """

    settings: Settings
    agent: Agent

    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize the ExcuseRepository.

        Args:
            settings: Application settings. If None, loads from environment.
        """
        self.settings = settings or Settings()

        # Create PydanticAI Agent with system prompt
        system_prompt = (
            "You are a vague excuse generator. Generate plausible but meaningless "
            "excuses using corporate jargon and technical terms. Be creative but "
            "professional. Keep responses concise (1-2 sentences). Use terms like "
            "'bandwidth', 'technical debt', 'sprint', 'migration', 'infrastructure', "
            "'optimization', etc. to sound busy but vague."
        )

        self.agent = Agent(
            "gemini-1.5-flash",
            system_prompt=system_prompt,
        )

    async def execute(self, operation: RepositoryOperationABC[T]) -> T:
        """
        Execute a repository operation following the Command pattern.

        Args:
            operation: The repository operation to execute.

        Returns:
            T: The result of the operation.
        """
        return await operation.execute(self)
