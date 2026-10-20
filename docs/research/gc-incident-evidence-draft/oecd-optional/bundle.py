"""Validate optional research extension without leaking it into public export."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent
schema = json.loads((ROOT / "schema.json").read_text(encoding="utf-8"))
validator = Draft202012Validator(schema, format_checker=FormatChecker())


def validate_optional(extension: dict) -> None:
    errors = list(validator.iter_errors(extension))
    if errors:
        raise ValueError("; ".join(e.message for e in errors))


def private_bundle(mandatory: dict, extension: dict) -> dict:
    """Research-only internal bundle; caller must enforce access controls."""
    validate_optional(extension)
    return {"mandatory": mandatory, "optional": extension}


def public_bundle(profile: dict, mandatory: dict, extension: dict, records: dict[str, dict] | None = None) -> dict:
    """Never export optional fields: their contents are not classified for release."""
    validate_optional(extension)
    from sys import path
    path.insert(0, str(ROOT.parent / "oecd-mandatory"))
    from export_adapter import public_export
    return public_export(profile, mandatory, records)
