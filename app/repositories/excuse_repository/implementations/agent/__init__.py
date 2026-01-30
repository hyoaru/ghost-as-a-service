"""Agent-based implementation of the Excuse Repository.

This implementation uses the ExcuseAgent utility to dynamically generate
excuses via LLM on demand.
"""

from typing import Optional, TypeVar

from app.utilities.excuse_agent import ExcuseAgent

from ...interface import ExcuseRepositoryABC, ExcuseRepositoryOperationABC
from .settings import Settings

T = TypeVar("T")


class AgentExcuseRepository(ExcuseRepositoryABC):
    """Agent-based excuse repository using LLM for dynamic generation.

    This repository implementation leverages the ExcuseAgent utility
    to generate contextually appropriate excuses in real-time.
    """

    def __init__(
        self,
        excuse_agent: Optional[ExcuseAgent] = None,
        settings: Optional[Settings] = None,
    ):
        """Initialize the agent-based repository.

        Args:
            excuse_agent: Optional ExcuseAgent instance. If not provided,
                creates a new one with default configuration.
            settings: Optional Settings instance. If not provided,
                loads from environment.
        """
        self.excuse_agent = excuse_agent or ExcuseAgent()
        self.settings = settings or Settings()

    async def execute(self, operation: ExcuseRepositoryOperationABC[T]) -> T:
        """Execute a repository operation.

        Args:
            operation: The operation to execute.

        Returns:
            The result of the operation execution.
        """
        return await operation.execute(self)
