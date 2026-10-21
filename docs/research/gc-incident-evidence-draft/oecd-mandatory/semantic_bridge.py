"""Research-only OECD adapter to GC draft projection, with explicit loss accounting.

The private envelope is the source of truth; GC draft cannot encode all OECD fields.
No automatic public release, authority claims or source taxonomy equivalence.
"""
import copy
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from internal_interchange import capture, restore, InterchangeError

ROOT = Path(__file__).resolve().parent
GC_SCHEMA = json.loads((ROOT.parent / "schema.json").read_text())
GC_VALIDATOR = Draft202012Validator(GC_SCHEMA, format_checker=FormatChecker())

class MappingError(ValueError):
    pass

def project(adapter, *, authorized=False, timeline=None):
    if not isinstance(timeline, dict) or set(timeline) != {"first_known_at", "reported_at"}:
        raise MappingError("Verified incident timestamps required; do not synthesize dates")
    envelope = capture(adapter, authorized=authorized)
    incident_id = adapter["incident_id"]
    profile = {
        "profile_version": "0.1.0",
        "incident_id": incident_id,
        "title": adapter["title"],
        "description": adapter["description"],
        "reporter": {
            "identity": {"type": "unverified-submitter", "id": "local:" + incident_id},
            "role": adapter["submitter"]["role"],
            "affiliation": adapter["submitter"]["affiliation"],
        },
        "affected_systems": [{
            "system": {"type": "unverified-ai-system", "id": "local:" + incident_id},
            "relationship": "unknown",
        }],
        "timeline": copy.deepcopy(timeline),
        "harm": {"status": "unknown", "description": "OECD adapter harm categories not mapped"},
        "severity": {"status": "unassessed"},
        "response_actions": [],
        "evidence_refs": [{
            "reference": {"type": "unverified-source", "id": "local:" + incident_id},
            "kind": "other",
            "sensitivity": "restricted",
        }],
        "review": {"status": "pending"},
        "disclosure": {"classification": "restricted", "publication_status": "draft"},
    }
    # This draft schema requires dates. Synthetic placeholders must not be mistaken
    # for actual incident timestamps; expose them as explicit unmapped placeholders.
    issues = [
        "Timestamps are caller-supplied context, not present in mandatory adapter; provenance unverified",
        "OECD causal categories have no verified equivalent in GC involved/suspected/unknown",
        "Submitter identity, evidence linkage, severity and harm classifications unverified",
    ]
    errors = list(GC_VALIDATOR.iter_errors(profile))
    if errors:
        raise MappingError("; ".join(e.message for e in errors))
    return {"profile": profile, "private_envelope": envelope, "mapping_issues": issues,
            "semantic_equivalence_verified": False}

def recover(result, *, authorized=False):
    if result.get("semantic_equivalence_verified") is not False:
        raise MappingError("Unsupported semantic-equivalence assertion")
    if not result.get("mapping_issues"):
        raise MappingError("Mapping loss accounting required")
    profile = result.get("profile")
    if not isinstance(profile, dict) or list(GC_VALIDATOR.iter_errors(profile)):
        raise MappingError("Invalid GC projection")
    envelope = result.get("private_envelope")
    original = restore(envelope, authorized=authorized)
    expected = project(original, authorized=True, timeline=profile["timeline"])
    if profile != expected["profile"]:
        raise MappingError("Projection modified or unsupported classification introduced")
    if result["mapping_issues"] != expected["mapping_issues"]:
        raise MappingError("Mapping loss accounting altered")
    return original
