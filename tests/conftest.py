"""
Pytest configuration and shared fixtures for all tests.
"""

from collections.abc import Generator

import pytest


@pytest.fixture
def sample_request() -> Generator[str, None, None]:
    """
    Common test request used across multiple test suites.

    Returns:
        str: A sample invitation/request text.
    """
    yield "Can you help me move this weekend?"


@pytest.fixture
def sample_excuse() -> Generator[str, None, None]:
    """
    Sample generated excuse for testing.

    Returns:
        str: A sample excuse response.
    """
    yield "Hey! So sorry, I'm actually in the middle of a massive data migration and my bandwidth is currently throttled by some legacy infrastructure issues. Let's circle back in Q3?"


@pytest.fixture
def sample_metadata() -> Generator[dict, None, None]:
    """
    Sample metadata for excuse generation.

    Returns:
        dict: Metadata about excuse generation.
    """
    yield {"model": "gemini-1.5-flash", "tokens": 150}
