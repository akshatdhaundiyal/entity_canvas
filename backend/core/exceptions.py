from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class AppException(Exception):
    """Base class for all application specific exceptions"""
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, details: Optional[Any] = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)

class DatabaseConnectionError(AppException):
    def __init__(self, alias: str, details: Optional[Any] = None):
        super().__init__(
            message=f"Could not connect to database with alias: {alias}",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details
        )

class QueryValidationError(AppException):
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )

class ResourceNotFoundError(AppException):
    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            message=f"{resource} with identifier {identifier} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
