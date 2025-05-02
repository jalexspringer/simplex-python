"""
Base domain client class for the Simplex Chat protocol.
"""

from typing import TYPE_CHECKING, TypeVar, Generic
import logging

from ..enums import ChatResponseType

if TYPE_CHECKING:
    from ..client import SimplexClient
    from ..response import ChatResponse


T = TypeVar('T', bound='BaseDomainClient')
logger = logging.getLogger(__name__)


class BaseDomainClient(Generic[T]):
    """Base class for all domain-specific clients."""
    
    def __init__(self, parent_client: "SimplexClient"):
        """
        Initialize a domain client with reference to parent SimplexClient.
        
        Args:
            parent_client: The parent SimplexClient instance
        """
        self._client = parent_client
        
    async def _process_response(
        self, 
        response: "ChatResponse", 
        expected_type: ChatResponseType,
        error_message: str
    ) -> "ChatResponse":
        """
        Process a command response with error handling.
        
        Args:
            response: The response from the server
            expected_type: The expected response type
            error_message: Error message to use if response type doesn't match
            
        Returns:
            The validated response
            
        Raises:
            SimplexCommandError: If the response type doesn't match expected_type
        """
        from ..errors import SimplexCommandError
        
        if not response:
            logger.error(f"Empty response received for expected type {expected_type}")
            raise SimplexCommandError(f"{error_message}: Empty response", None)
        
        logger.debug(f"Processing response: {response}")
        
        # Handle nested response structure - the actual response may be in a 'resp' field
        if hasattr(response, 'resp'):
            logger.debug("Response has 'resp' attribute")
            actual_resp = response.resp
        else:
            logger.debug("Using response as is")
            actual_resp = response
        
        # Get response type - handle both dictionary and object style responses
        if isinstance(actual_resp, dict):
            response_type = actual_resp.get("type")
            logger.debug(f"Response type from dict: {response_type}")
        else:
            response_type = getattr(actual_resp, "type", None)
            logger.debug(f"Response type from attr: {response_type}")
        
        if response_type != expected_type:
            logger.error(f"Expected response type {expected_type}, got {response_type}")
            
            # Handle error responses
            if response_type == "chatCmdError":
                if isinstance(actual_resp, dict):
                    chat_error = actual_resp.get("chatError", {})
                    error_type = chat_error.get("errorType", {})
                    detailed_type = error_type.get("type", "unknown")
                else:
                    error_info = getattr(actual_resp, "chatError", {})
                    error_type = getattr(error_info, "errorType", {})
                    detailed_type = getattr(error_type, "type", "unknown")
                    
                logger.error(f"Command error: {detailed_type}")
                raise SimplexCommandError(f"{error_message}: {detailed_type}", actual_resp)
            
            raise SimplexCommandError(error_message, actual_resp)
            
        logger.debug(f"Received valid response of type {expected_type}")
        return actual_resp
