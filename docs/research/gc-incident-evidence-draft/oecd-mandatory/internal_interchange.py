"""Research-only private interchange envelope; no storage, transport or publication.

Access control MUST be enforced by a caller. This module cannot grant access.
"""
from __future__ import annotations
import copy
import json
from jsonschema import Draft202012Validator, FormatChecker
from pathlib import Path

SCHEMA = json.loads((Path(__file__).resolve().parent / "oecd-mandatory.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
VERSION = "research-private-interchange/0.1"

class InterchangeError(ValueError):
    pass

def _check(document):
    errors = list(VALIDATOR.iter_errors(document))
    if errors:
        raise InterchangeError("Invalid adapter document: " + "; ".join(e.message for e in errors))

def capture(adapter: dict, *, authorized: bool = False) -> dict:
    """Copy a validated source into a private, non-public envelope."""
    if authorized is not True:
        raise InterchangeError("Explicit caller authorization required")
    _check(adapter)
    return {
        "format": VERSION,
        "classification": "restricted",
        "publication_permitted": False,
        "source_semantics": "oecd_mandatory_research_adapter",
        "payload": copy.deepcopy(adapter),
    }

def restore(envelope: dict, *, authorized: bool = False) -> dict:
    """Restore exactly the research adapter document, never a public export."""
    if authorized is not True:
        raise InterchangeError("Explicit caller authorization required")
    if not isinstance(envelope, dict) or set(envelope) != {
        "format", "classification", "publication_permitted", "source_semantics", "payload"
    }:
        raise InterchangeError("Unknown or incomplete private envelope")
    if (envelope["format"] != VERSION or envelope["classification"] != "restricted"
        or envelope["publication_permitted"] is not False
        or envelope["source_semantics"] != "oecd_mandatory_research_adapter"):
        raise InterchangeError("Private envelope boundary mismatch")
    _check(envelope["payload"])
    return copy.deepcopy(envelope["payload"])
