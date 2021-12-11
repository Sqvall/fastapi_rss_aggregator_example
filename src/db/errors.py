class EntityDoesNotExist(Exception):
    """Raised when entity was not found in database."""


class EntityAlreadyExist(Exception):
    """Raised when entity was already exist in database."""
