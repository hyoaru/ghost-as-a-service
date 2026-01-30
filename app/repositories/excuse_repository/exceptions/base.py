"""Base exception for Excuse Repository errors."""


class ExcuseRepositoryException(Exception):
    """Base exception for all Excuse Repository errors.

    All repository-specific exceptions should inherit from this class
    to isolate data access errors from other system errors.
    """

    pass
