"""
Tests for Pydantic models.
"""

import pytest
from pydantic import ValidationError


def test_event_model_validation_success():
    """
    Test that EventModel validates successfully with valid data.

    Verifies:
        - EventModel accepts valid request string
        - All fields are accessible
        - Data is stored correctly
    """
    # Arrange
    request_text = "Can you help me move this weekend?"

    # Act
    from app.models import EventModel

    event = EventModel(request=request_text)

    # Assert
    assert event.request == request_text
    assert isinstance(event.request, str)


def test_event_model_validation_failure():
    """
    Test that EventModel validation fails with invalid data.

    Verifies:
        - ValidationError is raised when required field is missing
        - Error message indicates the problem
    """
    # Arrange & Act & Assert
    from app.models import EventModel

    with pytest.raises(ValidationError) as exc_info:
        EventModel()  # Missing required 'request' field

    # Verify error mentions the missing field
    assert "request" in str(exc_info.value)


def test_event_model_empty_string_allowed():
    """
    Test that EventModel allows empty strings (validation done elsewhere).

    Verifies:
        - Empty string is accepted by Pydantic model
        - Business logic validation is separate concern
    """
    # Arrange & Act
    from app.models import EventModel

    event = EventModel(request="")

    # Assert
    assert event.request == ""


def test_excuse_response_model_success(sample_excuse, sample_metadata):
    """
    Test that ExcuseResponse model validates successfully with valid data.

    Verifies:
        - ExcuseResponse accepts excuse text
        - Metadata is optional and defaults to empty dict
        - All fields are accessible
    """
    # Arrange & Act
    from app.models import ExcuseResponse

    response = ExcuseResponse(excuse=sample_excuse, metadata=sample_metadata)

    # Assert
    assert response.excuse == sample_excuse
    assert response.metadata == sample_metadata
    assert isinstance(response.excuse, str)
    assert isinstance(response.metadata, dict)


def test_excuse_response_model_default_metadata():
    """
    Test that ExcuseResponse uses empty dict as default metadata.

    Verifies:
        - Metadata field is optional
        - Default value is empty dict
        - Default is not shared between instances
    """
    # Arrange
    excuse_text = "I'm in the middle of a data migration."

    # Act
    from app.models import ExcuseResponse

    response1 = ExcuseResponse(excuse=excuse_text)
    response2 = ExcuseResponse(excuse=excuse_text)

    # Assert
    assert response1.metadata == {}
    assert response2.metadata == {}

    # Verify they are different objects (no shared mutable default)
    response1.metadata["test"] = "value"
    assert "test" not in response2.metadata


def test_excuse_response_model_validation_failure():
    """
    Test that ExcuseResponse validation fails when excuse is missing.

    Verifies:
        - ValidationError is raised when required field is missing
        - Error message indicates the problem
    """
    # Arrange & Act & Assert
    from app.models import ExcuseResponse

    with pytest.raises(ValidationError) as exc_info:
        ExcuseResponse(metadata={"model": "test"})  # Missing required 'excuse'

    # Verify error mentions the missing field
    assert "excuse" in str(exc_info.value)


def test_excuse_response_model_to_dict(sample_excuse, sample_metadata):
    """
    Test that ExcuseResponse can be converted to dictionary.

    Verifies:
        - model_dump() returns dictionary
        - All fields are included in output
        - Values are correct
    """
    # Arrange
    from app.models import ExcuseResponse

    response = ExcuseResponse(excuse=sample_excuse, metadata=sample_metadata)

    # Act
    response_dict = response.model_dump()

    # Assert
    assert isinstance(response_dict, dict)
    assert response_dict["excuse"] == sample_excuse
    assert response_dict["metadata"] == sample_metadata


def test_excuse_response_model_from_dict(sample_excuse, sample_metadata):
    """
    Test that ExcuseResponse can be created from dictionary.

    Verifies:
        - model_validate() creates instance from dict
        - All fields are correctly populated
    """
    # Arrange
    from app.models import ExcuseResponse

    data = {"excuse": sample_excuse, "metadata": sample_metadata}

    # Act
    response = ExcuseResponse.model_validate(data)

    # Assert
    assert response.excuse == sample_excuse
    assert response.metadata == sample_metadata
