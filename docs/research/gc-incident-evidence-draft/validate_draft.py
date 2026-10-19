"""Experimental GC incident-evidence validation. Not a registered GC specification.

Run from repository root:
    python -m pip install 'jsonschema[format]>=4.23'
    python docs/research/gc-incident-evidence-draft/validate_draft.py
"""
from __future__ import annotations

import copy
import json
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def semantic_issues(report: dict, records: dict[str, dict] | None = None) -> list[str]:
    """Check report-local semantics and optional Governance Record references.

    A missing records index is never interpreted as evidence that links resolve.
    A valid reference is not proof of causality, authorization or reviewer independence.
    """
    issues: list[str] = []
    timeline = report["timeline"]
    if parse_timestamp(timeline["reported_at"]) < parse_timestamp(timeline["first_known_at"]):
        issues.append("reported_at precedes first_known_at")
    if "occurred_at" in timeline and parse_timestamp(timeline["first_known_at"]) < parse_timestamp(timeline["occurred_at"]):
        issues.append("first_known_at precedes occurred_at")
    disclosure = report["disclosure"]
    if disclosure["publication_status"] == "approved_for_release":
        if report["review"]["status"] != "approved":
            issues.append("release requires approved review")
        if disclosure["classification"] != "public":
            issues.append("restricted/confidential report cannot be approved for public release")
    links = []
    for action in report["response_actions"]:
        if action["status"] in ("authorized", "in_progress", "completed") and "governance_record" not in action:
            issues.append("active/completed response requires Governance Record reference")
        if "governance_record" in action:
            links.append(action["governance_record"])
    if report["review"]["status"] in ("approved", "rejected"):
        links.append(report["review"]["governance_record"])
    for evidence in report["evidence_refs"]:
        ref = evidence["reference"]
        if evidence["kind"] == "governance_record" and ref["type"] != "governance-record":
            issues.append("governance_record evidence must have governance-record reference type")
        if ref["type"] == "governance-record":
            links.append(ref)
    for ref in links:
        if ref["type"] != "governance-record":
            issues.append("linked Governance Record reference has wrong type")
        elif records is not None:
            record = records.get(ref["id"])
            if record is None:
                issues.append("Governance Record reference cannot be resolved: " + ref["id"])
            elif record.get("record_id") != ref["id"]:
                issues.append("resolved Governance Record ID mismatch: " + ref["id"])
    return issues


def main() -> None:
    schema = load("schema.json")
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    fixtures = [
        ("fixtures/valid-minimal.json", True),
        ("fixtures/invalid-reporter-role.json", False),
        ("fixtures/invalid-review-approval.json", False),
        ("fixtures/invalid-severity-assessment.json", False),
    ]
    valid = load("fixtures/valid-minimal.json")
    cases = []
    for path, expected in fixtures:
        cases.append((path, load(path), expected))
    for label, mutate in [
        ("bad-date", lambda x: x["timeline"].update(reported_at="not-a-date")),
        ("backwards-timeline", lambda x: x["timeline"].update(reported_at="2026-10-18T10:00:00Z")),
        ("release-without-review", lambda x: x["disclosure"].update(classification="public", publication_status="approved_for_release")),
        ("restricted-release", lambda x: (x["disclosure"].update(publication_status="approved_for_release"), x["review"].update(status="approved", reviewer={"type":"human","id":"reviewer"}, governance_record={"type":"governance-record","id":"gr-001"}))),
        ("wrong-evidence-type", lambda x: x["evidence_refs"][0]["reference"].update(type="artifact")),
        ("unresolved-record", lambda x: x["evidence_refs"][0]["reference"].update(id="missing")),
        ("active-action-no-record", lambda x: (x["response_actions"][0].update(status="completed"), x["response_actions"][0].pop("governance_record"))),
    ]:
        candidate = copy.deepcopy(valid)
        mutate(candidate)
        cases.append((label, candidate, False))
    records = {"gr-001": {"record_id": "gr-001"}}
    failures = []
    for label, report, expected in cases:
        schema_errors = list(validator.iter_errors(report))
        semantic_errors = semantic_issues(report, records) if not schema_errors else []
        observed = not (schema_errors or semantic_errors)
        print(f'{"PASS" if observed == expected else "FAIL"} {label}: expected_valid={expected}, observed_valid={observed}; schema={len(schema_errors)} semantic={len(semantic_errors)}')
        if observed != expected:
            failures.append(label)
    if failures:
        raise SystemExit("Validation mismatches: " + ", ".join(failures))
    print(f"All {len(cases)} expectations matched. This is NOT OECD conformance or verified real-world evidence.")


if __name__ == "__main__":
    main()
