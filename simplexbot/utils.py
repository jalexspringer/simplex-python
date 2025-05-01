"""
Utilities for Simplex Python client.

Includes protocol command stringification for parity with the TypeScript client.
"""
from typing import Any, Dict, Optional
import json

def on_off(value: Optional[bool]) -> str:
    return "on" if value else "off"

def maybe(value: Optional[Any]) -> str:
    return f" {value}" if value else ""

def maybe_json(value: Optional[Any]) -> str:
    return f" json {json.dumps(value)}" if value else ""

def auto_accept_str(auto_accept: Optional[Dict[str, Any]]) -> str:
    if not auto_accept:
        return "off"
    msg = auto_accept.get("autoReply")
    incognito = auto_accept.get("acceptIncognito", False)
    return (
        "on"
        + (" incognito=on" if incognito else "")
        + (f" json {json.dumps(msg)}" if msg else "")
    )

def cmd_string(cmd: Dict[str, Any]) -> str:
    """
    Convert a command dict (with a 'type' field) to the protocol string.
    Mirrors the TypeScript cmdString function.
    """
    t = cmd.get("type")
    if t == "showActiveUser":
        return "/u"
    elif t == "showMyAddress":
        return "/show_address"
    elif t == "addressAutoAccept":
        return f"/auto_accept {auto_accept_str(cmd.get('autoAccept'))}"
    elif t == "createActiveUser":
        user = {
            "profile": cmd["profile"],
            "sameServers": cmd.get("sameServers"),
            "pastTimestamp": cmd.get("pastTimestamp"),
        }
        return f"/_create user {json.dumps(user)}"
    elif t == "listUsers":
        return "/users"
    # Add more cases as needed for your protocol
    else:
        raise ValueError(f"Unknown or unimplemented command type: {t}")