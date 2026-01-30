"""Configuration settings for the Prepopulated Excuse Repository."""

from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Prepopulated implementation configuration loaded from environment.

    This implementation uses a predefined list of excuses to return
    without making external API calls.
    """

    model_config = SettingsConfigDict(
        env_file=(".env"),
        case_sensitive=True,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PREPOPULATED_EXCUSES: List[str] = Field(
        default=[
            "Sorry, I'm neck-deep in a critical data migration and my bandwidth is throttled by legacy infrastructure issues. Let's circle back in Q3?",
            "I'd love to, but I'm currently fire-fighting some cascading microservice failures. The technical debt is real right now.",
            "Unfortunately, I'm blocked by a dependency chain issue that's impacting our entire deployment pipeline. Rain check?",
            "I'm swamped with an emergency sprint to patch some critical vulnerabilities in our production environment. Let me ping you next quarter.",
            "Can't make it - I'm deep in the weeds troubleshooting a distributed systems nightmare with cross-region replication lag.",
            "I'm stuck in back-to-back syncs with stakeholders about our infrastructure roadmap. Maybe we can revisit this in the next planning cycle?",
            "Sorry, I'm currently deprecating some legacy endpoints and the refactoring effort is consuming all my cycles right now.",
            "I'm underwater with a massive schema migration that's blocking half the engineering org. Let's touch base after we ship this.",
            "Unfortunately, I'm being pulled into an all-hands-on-deck situation to resolve some cascading failures in our observability stack.",
            "I'd love to help, but I'm currently architecting a solution for our scalability bottlenecks and it's taking up all my bandwidth.",
        ],
        description="List of prepopulated excuses to return",
    )
