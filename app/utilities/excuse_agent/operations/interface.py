"""Abstract base class for Excuse Agent operations."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

T = TypeVar("T")

if TYPE_CHECKING:
    from ..interface import ExcuseAgentABC


class ExcuseAgentOperationABC(ABC, Generic[T]):
    """Abstract base for operations executed against the Excuse Agent.

    Implementations must define execute() to perform specific tasks
    using the agent.
    """

    @abstractmethod
    async def execute(self, utility: "ExcuseAgentABC") -> T:
        """Execute the operation against the Excuse Agent.

        Args:
            utility: The Excuse Agent instance.

        Returns:
            The operation result.
        """
        pass
