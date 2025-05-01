"""
Message models for Simplex communication.

This module defines the structures for message content types and composed messages
used in the Simplex messaging system.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union


@dataclass(kw_only=True)
class LinkPreview:
    """Preview information for a link.

    Attributes:
        uri: Link URI.
        title: Link title.
        description: Link description.
        image: Link preview image.
    """

    uri: str
    title: str
    description: str
    image: str


@dataclass(kw_only=True)
class MCText:
    """Text message content.

    Attributes:
        type: Message content type ("text").
        text: The text content.
    """

    type: str = "text"
    text: str


@dataclass(kw_only=True)
class MCLink:
    """Link message content.

    Attributes:
        type: Message content type ("link").
        text: The text content.
        preview: Link preview information.
    """

    type: str = "link"
    text: str
    preview: LinkPreview


@dataclass(kw_only=True)
class MCImage:
    """Image message content.

    Attributes:
        type: Message content type ("image").
        text: The text content.
        image: Image data as base64 encoded string.
    """

    type: str = "image"
    text: str
    image: str


@dataclass(kw_only=True)
class MCFile:
    """File message content.

    Attributes:
        type: Message content type ("file").
        text: The file description or name.
    """

    type: str = "file"
    text: str


@dataclass(kw_only=True)
class MCUnknown:
    """Unknown message content type.

    Attributes:
        type: Message content type (unknown string).
        text: The text content.
    """

    type: str
    text: str


# Define the union type for message content
MsgContent = Union[MCText, MCLink, MCImage, MCFile, MCUnknown]


@dataclass(kw_only=True)
class ComposedMessage:
    """Composed message object for sending.

    Attributes:
        msg_content: The message content object.
        file_path: Optional file path to attach.
        quoted_item_id: Optional ID of quoted chat item.
    """

    msg_content: MsgContent
    file_path: Optional[str] = None
    quoted_item_id: Optional[int] = None
