"""
Service operations for the excuse generator.

This module exports all available service operations.
"""

from app.services.excuse_generator.operations.interface import (
    ExcuseGeneratorOperationABC,
)

__all__ = ["ExcuseGeneratorOperationABC"]
