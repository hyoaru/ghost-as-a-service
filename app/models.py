"""
Pydantic models for Lambda event input and response.
"""

from pydantic import BaseModel, Field


class EventModel(BaseModel):
    """
    Model representing the input event for the excuse generator Lambda.
    """

    request: str = Field(
        ..., description="The request or invitation text to generate an excuse for."
    )


class ExcuseResponse(BaseModel):
    """
    Model representing the response from the excuse generator.
    """

    excuse: str = Field(..., description="The generated excuse text")
