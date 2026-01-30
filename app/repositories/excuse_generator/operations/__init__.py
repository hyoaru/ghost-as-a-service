"""
Repository operations for the excuse generator.

This module exports all available repository operations.
"""

from .get_vague import GetVague
from .interface import RepositoryOperationABC

__all__ = ["GetVague", "RepositoryOperationABC"]
