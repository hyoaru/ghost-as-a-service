"""
Abstract base classes for the excuse agent utility infrastructure.

This module defines the interface that the ExcuseAgent utility must implement,
following the Type A Infrastructure (Stateful) pattern for PydanticAI Agent wrapper.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic_ai import Agent

T = TypeVar("T")


class ExcuseAgentOperationABC(ABC, Generic[T]):
    """
    Abstract base class for excuse agent operations.

    Operations encapsulate the logic to execute against the excuse agent utility,
    allowing for modular and testable code. This follows the Command pattern.

    Type Parameters:
        T: The return type of the operation.
    """

    @abstractmethod
    def execute(self, utility: "ExcuseAgentABC") -> T:
        """
        Execute the operation against the given excuse agent utility.

        Args:
            utility: The ExcuseAgent instance to execute against.

        Returns:
            T: The result of the operation.
        """
        pass


class ExcuseAgentABC(ABC):
    """
    Abstract base class for excuse agent utility.

    This is a Type A Infrastructure (Stateful) utility that wraps the
    PydanticAI Agent and delegates operations to it. The agent maintains
    state (the PydanticAI Agent instance and its configuration).

    Attributes:
        agent: The underlying PydanticAI Agent instance.
    """

    agent: Agent

    @abstractmethod
    def execute(self, operation: ExcuseAgentOperationABC[T]) -> T:
        """
        Execute an operation following the Command pattern.

        Per Type A Infrastructure pattern, this passes self to the operation
        so it can access the agent and other infrastructure resources.

        Args:
            operation: The operation to execute.

        Returns:
            T: The result of the operation.
        """
        pass
