"""Abstract interface for the Excuse Agent."""

from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic_ai import Agent

from .operations.interface import ExcuseAgentOperationABC

T = TypeVar("T")


class ExcuseAgentABC(ABC):
    """Abstract base class defining the Excuse Agent contract.

    Implements the Command Pattern for executing operations against
    the LLM agent.
    """

    agent: Agent

    @abstractmethod
    async def execute(self, operation: ExcuseAgentOperationABC[T]) -> T:
        """Execute an operation.

        Args:
            operation: The operation to execute.

        Returns:
            The result of the operation execution.
        """
        pass
