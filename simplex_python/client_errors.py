"""
Error handling for the Simplex chat client.

This module provides structured error handling for the Simplex chat client,
allowing for more specific error details and response context when operations fail.
"""

from typing import Optional

from .responses import CommandResponse


class SimplexCommandError(Exception):
    """
    Exception raised for errors in SimplexClient command execution.

    Provides details about the specific error and includes the original response
    for further inspection when available.
    """

    def __init__(self, message: str, response: Optional[CommandResponse] = None):
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


class SimplexConnectionError(SimplexClientError):
    """
    Exception raised for connection errors in SimplexClient.
    
    Provides detailed information about connection issues, including
    suggestions for common problems like server not running.
    """
    
    def __init__(self, message: str, url: str, original_error: Optional[Exception] = None):
        """
        Initialize a new SimplexConnectionError.
        
        Args:
            message: Human-readable error description
            url: The URL that failed to connect
            original_error: The original exception that caused the connection failure
        """
        self.url = url
        self.original_error = original_error
        
        # Build a detailed error message with helpful suggestions
        detailed_message = f"Failed to connect to SimpleX server at {url}: {message}"
        
        # Add common troubleshooting tips
        detailed_message += "\n\nPossible causes:"
        detailed_message += "\n- SimpleX Chat server is not running at the specified address and port"
        detailed_message += "\n- Network connectivity issues"
        detailed_message += "\n- Incorrect host or port in the URL"
        
        detailed_message += "\n\nTroubleshooting steps:"
        detailed_message += "\n1. Verify the SimpleX Chat server is running"
        detailed_message += "\n2. Check the host and port in your connection URL"
        detailed_message += "\n3. Ensure there are no firewall or network restrictions"
        
        if original_error:
            detailed_message += f"\n\nOriginal error: {original_error}"
            
        super().__init__(detailed_message)
