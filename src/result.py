"""Result dataclass for operation outcomes."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Result:
    """Represents the outcome of an operation with success/error information."""
    success: bool
    message: str
    error_details: Optional[str] = None
    
    @staticmethod
    def ok(message: str) -> 'Result':
        """Create a successful result."""
        return Result(success=True, message=message)
    
    @staticmethod
    def error(message: str, details: str = None) -> 'Result':
        """Create an error result."""
        return Result(success=False, message=message, error_details=details)
