"""Experimental validated adapter binding and fail-closed public export.

No network retrieval, evidence dereferencing, publication or GC core mutation.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent
PROFILE_ROOT = ROOT.parent


class AdapterError(ValueError):
    pass


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def validate_pair(profile: dict, adapter: dict) -> None:
    for schema_path, document in (
        (PROFILE_ROOT / "schema.json", profile),
        (ROOT / "oecd-mandatory.schema.json", adapter),
    ):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(document))
        if errors:
            raise AdapterError(f"{schema_path.name}: " + "; ".join(e.message for e in errors))
    if profile["title"] != adapter["title"] or profile["description"] != adapter["description"]:
        raise AdapterError("Incident title/description mismatch")
    if profile["reporter"]["role"] != adapter["submitter"]["role"]:
        raise AdapterError("Reporter role mismatch")
    if not profile["affected_systems"]:
        raise AdapterError("Missing incident-system linkage")
    if not profile["evidence_refs"]:
        raise AdapterError("Missing incident evidence linkage")
    if profile["disclosure"]["classification"] != "public" or profile["disclosure"]["publication_status"] != "approved_for_release":
        raise AdapterError("Public export requires public classification and approved release")
    if profile["review"]["status"] != "approved":
        raise AdapterError("Public export requires approved review")
    if any(item["sensitivity"] != "public" for item in adapter["supporting_materials"]):
        raise AdapterError("Nonpublic supporting materials cannot be exported")
    if any(item["sensitivity"] != "public" for item in profile["evidence_refs"]):
        raise AdapterError("Nonpublic profile evidence cannot be exported")


def public_export(profile: dict, adapter: dict) -> dict:
    """Return a narrow allowlisted public view; do not export submitter PII.

    This is a serialization guard, NOT evidence of authorization, consent,
    verified redaction, approved Governance Records, or safe URL targets.
    """
    validate_pair(profile, adapter)
    return {
        "profile_version": profile["profile_version"],
        "incident_id": profile["incident_id"],
        "title": adapter["title"],
        "description": adapter["description"],
        "system_relationships": copy.deepcopy(adapter["system_relationships"]),
        "severity": copy.deepcopy(adapter["severity"]),
        "harm_types": copy.deepcopy(adapter["harm_types"]),
        "supporting_materials": [
            {"kind": item["kind"], "reference": item["reference"]}
            for item in adapter["supporting_materials"]
        ],
        "disclosure": {"classification": "public", "publication_status": "approved_for_release"},
    }
