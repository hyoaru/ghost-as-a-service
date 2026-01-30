"""
Excuse generator repository module.

This module provides the repository layer for generating vague excuses
using PydanticAI and Google Gemini.
"""

from .excuse_repository import ExcuseRepository
from .interface import ExcuseRepositoryABC
from .operations import GetVague

__all__ = ["ExcuseRepository", "ExcuseRepositoryABC", "GetVague"]
