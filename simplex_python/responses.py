from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from .client_errors import SimplexClientError
from enum import Enum


@dataclass
class DynamicResponse:
    """
    A response class that automatically extracts the second key-value pair
    from a response dictionary and assigns it to a data attribute.

    Attributes:
        res_type: The response type string.
        raw_resp: The original raw response dictionary.
        data: The extracted data from the second key-value pair.
    """

    res_type: str
    raw_response: Dict
    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, resp_dict: Dict[str, Any]) -> "DynamicResponse":
        """
        Create a DynamicResponse from a dictionary.

        Args:
            resp_dict: Response dictionary with 'type' and a second key-value pair.

        Returns:
            A DynamicResponse object with the data extracted.
        """
        type_val = resp_dict.get("type", "unknown")
        if "Error" in type_val:
            raise SimplexClientError(
                {"ERROR": f"{type_val} - {resp_dict}"},
            )
        # Find the second key that isn't 'type'
        data_key = next((k for k in resp_dict.keys() if k != "type"), None)
        data_val = resp_dict.get(data_key, {}) if data_key else {}

        return cls(res_type=type_val, raw_response=resp_dict, data=data_val)


# Base response structure - all responses will be parsed into this
@dataclass
class CommandResponse:
    """Base class for all command responses."""

    type: str
    user: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CommandResponse":
        """Create a CommandResponse from a dictionary."""
        if not isinstance(data, dict):
            return CommandResponse(type="unknown")

        response_type = data.get("type", "unknown")

        # For generic/unknown response types, just create a basic response
        return CommandResponse(type=response_type, user=data.get("user"))


# Chat types - used across different domain responses
class ChatInfoType(str, Enum):
    """Type of chat"""

    DIRECT = "direct"
    GROUP = "group"
    CONTACT_REQUEST = "contactRequest"
