"""Governance Record structural and semantic conformance validation."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from importlib import resources
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .report import ConformanceReport, RuleResult, build_report

GOVERNANCE_RECORD_SPEC_VERSION = "1.0.0"

_SCHEMA = json.loads(
    resources.files("governance_commons")
    .joinpath("schemas/governance-record.schema.json")
    .read_text(encoding="utf-8")
)
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
    return [
        RuleResult(
            "GR-SCHEMA-001",
            f"Governance Record schema violation at {_path(list(e.absolute_path))}",
            "fail",
            e.message,
        )
        for e in errors
    ]


def _parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed


def _auth_rule(data: dict[str, Any]) -> RuleResult:
    action = data.get("action")
    if not isinstance(action, dict) or action.get("status") not in {"authorized", "completed"}:
        return RuleResult("GR-AUTH-001", "Required authorization exists before an authorized or completed action", "pass")

    authority = data.get("authority")
    approval = data.get("approval")
    if not isinstance(authority, dict) or authority.get("status") != "active":
        return RuleResult(
            "GR-AUTH-001",
            "Required authorization exists before an authorized or completed action",
            "fail",
            "action is authorized/completed but applicable authority is not active",
        )
    if isinstance(approval, dict) and approval.get("required") is True and approval.get("status") != "approved":
        return RuleResult(
            "GR-AUTH-001",
            "Required authorization exists before an authorized or completed action",
            "fail",
            "required approval is not approved",
        )
    return RuleResult("GR-AUTH-001", "Required authorization exists before an authorized or completed action", "pass")


def _revocation_rule(data: dict[str, Any]) -> RuleResult:
    action = data.get("action")
    authority = data.get("authority")
    if not isinstance(action, dict) or action.get("status") not in {"authorized", "completed"} or not isinstance(authority, dict):
        return RuleResult("GR-AUTH-002", "Revoked authority cannot authorize an action after revocation", "pass")

    timestamps = data.get("timestamps")
    occurred_at = _parse_time(timestamps.get("occurred_at")) if isinstance(timestamps, dict) else None
    revoked_at = _parse_time(authority.get("revoked_at"))
    granted_at = _parse_time(authority.get("granted_at"))

    if authority.get("status") == "revoked":
        if revoked_at is None:
            return RuleResult(
                "GR-AUTH-002",
                "Revoked authority cannot authorize an action after revocation",
                "fail",
                "revoked authority has no valid revoked_at timestamp",
            )
        if occurred_at is None:
            return RuleResult(
                "GR-AUTH-002",
                "Revoked authority cannot authorize an action after revocation",
                "fail",
                "action has no valid occurred_at timestamp for temporal authority evaluation",
            )
        if occurred_at > revoked_at:
            return RuleResult(
                "GR-AUTH-002",
                "Revoked authority cannot authorize an action after revocation",
                "fail",
                "action occurred after authority revocation",
            )

    if granted_at is not None and occurred_at is not None and occurred_at < granted_at:
        return RuleResult(
            "GR-AUTH-002",
            "Revoked authority cannot authorize an action after revocation",
            "fail",
            "action occurred before authority was granted",
        )

    return RuleResult("GR-AUTH-002", "Revoked authority cannot authorize an action after revocation", "pass")


def _handoff_rule(data: dict[str, Any]) -> RuleResult:
    handoff = data.get("handoff")
    if not isinstance(handoff, dict) or handoff.get("status") not in {"accepted", "completed"}:
        return RuleResult(
            "GR-HANDOFF-001",
            "Accepted/completed handoffs contain transfer, scope, authority, and trust-boundary information",
            "pass",
        )

    required = ("from", "to", "scope", "authority_transfer", "trust_boundary", "acceptance")
    missing = [key for key in required if key not in handoff]
    if missing:
        return RuleResult(
            "GR-HANDOFF-001",
            "Accepted/completed handoffs contain transfer, scope, authority, and trust-boundary information",
            "fail",
            f"missing handoff fields: {', '.join(missing)}",
        )

    transfer = handoff.get("authority_transfer")
    boundary = handoff.get("trust_boundary")
    scope = handoff.get("scope")
    acceptance = handoff.get("acceptance")
    if (
        not isinstance(transfer, dict)
        or transfer.get("transferred") is not True
        or not isinstance(transfer.get("authority_ref"), dict)
        or not isinstance(transfer.get("scope"), list)
        or not transfer.get("scope")
        or not isinstance(transfer.get("delegated_by"), dict)
    ):
        return RuleResult(
            "GR-HANDOFF-001",
            "Accepted/completed handoffs contain transfer, scope, authority, and trust-boundary information",
            "fail",
            "authority transfer is incomplete",
        )
    if not isinstance(scope, dict) or not isinstance(scope.get("description"), str) or not scope.get("description").strip():
        return RuleResult(
            "GR-HANDOFF-001",
            "Accepted/completed handoffs contain transfer, scope, authority, and trust-boundary information",
            "fail",
            "handoff scope description is missing",
        )
    if not isinstance(boundary, dict) or not boundary.get("boundary_type") or not isinstance(boundary.get("boundary_ref"), dict):
        return RuleResult(
            "GR-HANDOFF-001",
            "Accepted/completed handoffs contain transfer, scope, authority, and trust-boundary information",
            "fail",
            "trust boundary is incomplete",
        )
    if not isinstance(acceptance, dict) or not isinstance(acceptance.get("accepted_by"), dict) or not _parse_time(acceptance.get("accepted_at")):
        return RuleResult(
            "GR-HANDOFF-001",
            "Accepted/completed handoffs contain transfer, scope, authority, and trust-boundary information",
            "fail",
            "handoff acceptance is incomplete or has an invalid accepted_at timestamp",
        )
    return RuleResult(
        "GR-HANDOFF-001",
        "Accepted/completed handoffs contain transfer, scope, authority, and trust-boundary information",
        "pass",
    )


def validate_governance_record_data(data: Any, *, subject: str = "<memory>", profile: str = "standard") -> ConformanceReport:
    """Validate one Governance Record and return the shared GC conformance report."""
    schema_rules = _schema_rules(data)
    rules = list(schema_rules)
    if schema_rules and all(r.result == "pass" for r in schema_rules) and isinstance(data, dict):
        rules.extend([_auth_rule(data), _revocation_rule(data), _handoff_rule(data)])
    return build_report(
        spec="governance-record",
        spec_version=GOVERNANCE_RECORD_SPEC_VERSION,
        profile=profile,
        subject=subject,
        rules=rules,
    )


def validate_governance_record_contract(path: str | Path, *, profile: str = "standard") -> ConformanceReport:
    source = Path(path)
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except OSError as exc:
        return build_report(
            spec="governance-record",
            spec_version=GOVERNANCE_RECORD_SPEC_VERSION,
            profile=profile,
            subject=str(source),
            rules=[RuleResult("GR-INPUT-001", "Governance Record input is readable JSON", "fail", str(exc))],
        )
    except json.JSONDecodeError as exc:
        return build_report(
            spec="governance-record",
            spec_version=GOVERNANCE_RECORD_SPEC_VERSION,
            profile=profile,
            subject=str(source),
            rules=[RuleResult("GR-INPUT-002", "Governance Record input is valid JSON", "fail", str(exc))],
        )
    return validate_governance_record_data(data, subject=str(source), profile=profile)
