from typing import Dict


class ApplicationError(Exception):
    """Base exception for our application"""

    message: str
    extra: Dict[str, any]

    def __init__(self, message, extra=None):
        self.message = message
        self.extra = extra or {}
