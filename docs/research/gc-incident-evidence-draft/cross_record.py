"""Experimental cross-record integrity checks; fail closed, no normative GC claims."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = json.loads((ROOT / "governance_commons/schemas/governance-record.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())


def timestamp(value):
    if not isinstance(value, str):
        return None
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return result if result.tzinfo is not None else None
    except ValueError:
        return None


def issues_for_record(record):
    """Mirror applicable GR-AUTH-001/002 checks, plus fail-closed time handling."""
    problems = []
    if list(VALIDATOR.iter_errors(record)):
        return ["linked Governance Record violates core JSON Schema"]
    action = record.get("action")
    if not isinstance(action, dict) or action.get("status") not in {"authorized", "completed"}:
        return problems
    authority = record.get("authority", {})
    if authority.get("status") != "active":
        problems.append("action authority not active")
    approval = record.get("approval")
    if isinstance(approval, dict) and approval.get("required") and approval.get("status") != "approved":
        problems.append("required approval not approved")
    occurred = timestamp(record.get("timestamps", {}).get("occurred_at"))
    if occurred is None:
        problems.append("action occurred_at invalid or missing timezone")
    granted = timestamp(authority.get("granted_at")) if authority.get("granted_at") else None
    revoked = timestamp(authority.get("revoked_at")) if authority.get("revoked_at") else None
    if authority.get("granted_at") and granted is None:
        problems.append("authority granted_at invalid")
    if authority.get("revoked_at") and revoked is None:
        problems.append("authority revoked_at invalid")
    if occurred is not None and granted is not None and occurred < granted:
        problems.append("action predates authority grant")
    if occurred is not None and revoked is not None and occurred > revoked:
        problems.append("action after revocation")
    return problems


def cross_record_issues(report, records):
    """Resolve and inspect evidence and claimed approvals. Not proof of provenance."""
    problems = []
    def resolve(ref, expected_type, context):
        if ref.get("type") != "governance-record":
            problems.append(context + ": incorrect reference type")
            return None
        record = records.get(ref.get("id"))
        if record is None:
            problems.append(context + ": unresolved Governance Record")
            return None
        if record.get("record_id") != ref.get("id"):
            problems.append(context + ": record ID mismatch")
            return None
        if record.get("record_type") != expected_type and expected_type is not None:
            problems.append(context + ": unexpected Governance Record type")
        problems.extend(context + ": " + p for p in issues_for_record(record))
        return record

    for i, action in enumerate(report["response_actions"]):
        status = action["status"]
        if status in {"authorized", "in_progress", "completed"}:
            ref = action.get("governance_record")
            if ref is None:
                problems.append(f"response[{i}]: missing action Governance Record")
                continue
            record = resolve(ref, "action", f"response[{i}]")
            if record is None:
                continue
            if record.get("action", {}).get("status") not in {"authorized", "completed"}:
                problems.append(f"response[{i}]: action not authorized or completed")
            if status == "completed" and record.get("action", {}).get("status") != "completed":
                problems.append(f"response[{i}]: completion not evidenced")
            subject = record.get("subject")
            if subject != {"type": "incident", "id": report["incident_id"]}:
                problems.append(f"response[{i}]: action subject does not match incident")
    review = report["review"]
    if review["status"] in {"approved", "rejected"}:
        record = resolve(review["governance_record"], "approval", "review")
        if record is not None:
            approval = record.get("approval", {})
            expected = review["status"]
            if approval.get("status") != expected:
                problems.append("review: approval status mismatch")
            if approval.get("approver") != review["reviewer"]:
                problems.append("review: reviewer identity mismatch")
            if record.get("subject") != {"type": "incident", "id": report["incident_id"]}:
                problems.append("review: approval subject mismatch")
    for i, evidence in enumerate(report["evidence_refs"]):
        if evidence["kind"] == "governance_record":
            resolve(evidence["reference"], None, f"evidence[{i}]")
    return problems
