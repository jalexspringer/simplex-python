"""
Error handling for the Simplex chat client.

This module provides structured error handling for the Simplex chat client,
allowing for more specific error details and response context when operations fail.
"""

from typing import Optional

from .response import ChatResponse


class SimplexCommandError(Exception):
    """
    Exception raised for errors in SimplexClient command execution.
    
    Provides details about the specific error and includes the original response
    for further inspection when available.
    """
    
    def __init__(self, message: str, response: Optional[ChatResponse] = None):
        """
        Initialize a new SimplexCommandError.
        
        Args:
            message: Human-readable error description
            response: Optional original response object that triggered the error
        """
        self.message = message
        self.response = response
        super().__init__(message)


class SimplexClientError(Exception):
    """
    Exception raised for client-level errors in SimplexClient.
    
    Used for connection, transport, and general client operation errors.
    """
    pass
