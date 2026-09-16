"""Governance Record structural and semantic conformance validation."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from importlib import resources
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .report import ConformanceReport, RuleResult, build_report

GOVERNANCE_RECORD_SPEC_VERSION = "1.0.0"

_SCHEMA = json.loads(resources.files("governance_commons").joinpath("schemas/governance-record.schema.json").read_text(encoding="utf-8"))
Draft202012Validator.check_schema(_SCHEMA)
_VALIDATOR = Draft202012Validator(_SCHEMA)


@dataclass(frozen=True)
class GovernanceRecordValidation:
    data: Any
    valid: bool
    issues: tuple[RuleResult, ...]


def _path(parts: list[object]) -> str:
    out = "$"
    for part in parts:
        out += f"[{part}]" if isinstance(part, int) else f".{part}"
    return out


def _schema_rules(data: Any) -> list[RuleResult]:
    errors = sorted(_VALIDATOR.iter_errors(data), key=lambda e: (list(e.absolute_path), e.message))
    if not errors:
        return [RuleResult("GR-SCHEMA-001", "Governance Record conforms to the v1.0.0 JSON Schema", "pass")]
    return [RuleResult("GR-SCHEMA-001", f"Governance Record schema violation at {_path(list(e.absolute_path))}", "fail", e.message) for e in errors]


def _parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _auth_rule(data: dict[str, Any]) -> RuleResult:
    action = data.get("action")
    if not isinstance(action, dict) or action.get("status") not in {"authorized", "completed"}:
        return RuleResult("GR-AUTH-001", "Required authorization exists before an authorized or completed action", "pass")
    authority = data.get("authority")
    approval = data.get("approval")
    if not isinstance(authority, dict) or authority.get("status") != "active":
        return RuleResult("GR-AUTH-001", "Required authorization exists before an authorized or completed action", "fail", "action is authorized/completed but applicable authority is not active")
    if isinstance(approval, dict) and approval.get("required") is True and approval.get("status") != "approved":
        return RuleResult("GR-AUTH-001", "Required authorization exists before an authorized or completed action", "fail", "required approval is not approved")
    return RuleResult("GR-AUTH-001", "Required authorization exists before an authorized or completed action", "pass")


def _revocation_rule(data: dict[str, Any]) -> RuleResult:
    action = data.get("action")
    authority = data.get("authority")
    if not isinstance(action, dict) or not isinstance(authority, dict):
        return RuleResult("GR-AUTH-002", "Revoked authority cannot authorize an action after revocation", "pass")
    revoked_at = _parse_time(authority.get("revoked_at"))
    occurred_at = _parse_time((data.get("timestamps") or {}).get("occurred_at")) if isinstance(data.get("timestamps"), dict) else None
    if authority.get("status") == "revoked" and revoked_at and occurred_at and occurred_at > revoked_at:
        return RuleResult("GR-AUTH-002", "Revoked authority cannot authorize an action after revocation", "fail", "action occurred after authority revocation")
    return RuleResult("GR-AUTH-002", "Revoked authority cannot authorize an action after revocation", "pass")


def _handoff_rule(data: dict[str, Any]) -> RuleResult:
    handoff = data.get("handoff")
    if not isinstance(handoff, dict) or handoff.get("status") not in {"accepted", "completed"}:
        return RuleResult("GR-HANDOFF-001", "Accepted/completed handoffs contain transfer, scope, authority, and trust-boundary information", "pass")
    required = ("from", "to", "scope", "authority_transfer", "trust_boundary", "acceptance")
    missing = [key for key in required if key not in handoff]
    if missing:
        return RuleResult("GR-HANDOFF-001", "Accepted/completed handoffs contain transfer, scope, authority, and trust-boundary information", "fail", f"missing handoff fields: {', '.join(missing)}")
    transfer = handoff.get("authority_transfer")
    boundary = handoff.get("trust_boundary")
    if not isinstance(transfer, dict) or not transfer.get("transferred") or not transfer.get("authority_ref") or not transfer.get("scope") or not transfer.get("delegated_by"):
        return RuleResult("GR-HANDOFF-001", "Accepted/completed handoffs contain transfer, scope, authority, and trust-boundary information", "fail", "authority transfer is incomplete")
    if not isinstance(boundary, dict) or not boundary.get("boundary_type") or not boundary.get("boundary_ref"):
        return RuleResult("GR-HANDOFF-001", "Accepted/completed handoffs contain transfer, scope, authority, and trust-boundary information", "fail", "trust boundary is incomplete")
    return RuleResult("GR-HANDOFF-001", "Accepted/completed handoffs contain transfer, scope, authority, and trust-boundary information", "pass")


def validate_governance_record_data(data: Any, *, subject: str = "<memory>", profile: str = "standard") -> ConformanceReport:
    """Validate one Governance Record and return the shared GC conformance report."""
    schema_rules = _schema_rules(data)
    rules = list(schema_rules)
    if schema_rules and all(r.result == "pass" for r in schema_rules) and isinstance(data, dict):
        rules.extend([_auth_rule(data), _revocation_rule(data), _handoff_rule(data)])
    return build_report(spec="governance-record", spec_version=GOVERNANCE_RECORD_SPEC_VERSION, profile=profile, subject=subject, rules=rules)


def validate_governance_record_contract(path: str | Path, *, profile: str = "standard") -> ConformanceReport:
    source = Path(path)
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except OSError as exc:
        return build_report(spec="governance-record", spec_version=GOVERNANCE_RECORD_SPEC_VERSION, profile=profile, subject=str(source), rules=[RuleResult("GR-INPUT-001", "Governance Record input is readable JSON", "fail", str(exc))])
    except json.JSONDecodeError as exc:
        return build_report(spec="governance-record", spec_version=GOVERNANCE_RECORD_SPEC_VERSION, profile=profile, subject=str(source), rules=[RuleResult("GR-INPUT-002", "Governance Record input is valid JSON", "fail", str(exc))])
    return validate_governance_record_data(data, subject=str(source), profile=profile)
