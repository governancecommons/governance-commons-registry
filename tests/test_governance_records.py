"""A5.6 Governance Record reconciliation and hardening tests."""
from __future__ import annotations

import json
from pathlib import Path

from governance_commons.governance_records import validate_governance_record_contract, validate_governance_record_data

ROOT = Path(__file__).parent / "fixtures" / "governance-record"


def _files(group: str) -> list[Path]:
    return sorted((ROOT / group).glob("*.json"))


def test_valid_fixtures_remain_conformant() -> None:
    for path in _files("valid"):
        report = validate_governance_record_contract(path)
        assert report.conformant, (path.name, report.to_dict())
        assert report.gc_report_version == "1.0.0"


def test_schema_invalid_fixtures_do_not_enter_governance_rules() -> None:
    for path in _files("invalid"):
        report = validate_governance_record_contract(path)
        assert not report.conformant, (path.name, report.to_dict())
        assert any(r.rule_id == "GR-SCHEMA-001" and r.result == "fail" for r in report.rules)
        assert not any(r.rule_id.startswith("GR-AUTH-") or r.rule_id == "GR-HANDOFF-001" for r in report.rules)


def test_unauthorized_action_preserves_structural_then_semantic_boundary() -> None:
    report = validate_governance_record_contract(ROOT / "governance-rules" / "unauthorized-action.json")
    assert report.rules[0].rule_id == "GR-SCHEMA-001"
    assert report.rules[0].result == "pass"
    assert next(r for r in report.rules if r.rule_id == "GR-AUTH-001").result == "fail"
    assert not report.conformant


def test_revocation_is_temporal_and_uses_occurrence_time() -> None:
    report = validate_governance_record_contract(ROOT / "governance-rules" / "revoked-authority-action.json")
    assert next(r for r in report.rules if r.rule_id == "GR-AUTH-002").result == "fail"

    before = json.loads((ROOT / "governance-rules" / "revoked-authority-action.json").read_text())
    before["timestamps"]["occurred_at"] = "2026-09-16T16:09:59Z"
    report_before = validate_governance_record_data(before)
    assert next(r for r in report_before.rules if r.rule_id == "GR-AUTH-002").result == "pass"


def test_revoked_authority_without_timestamp_is_not_silently_accepted() -> None:
    data = json.loads((ROOT / "governance-rules" / "revoked-authority-action.json").read_text())
    del data["authority"]["revoked_at"]
    report = validate_governance_record_data(data)
    assert next(r for r in report.rules if r.rule_id == "GR-AUTH-002").result == "fail"


def test_action_before_grant_is_not_authorized() -> None:
    data = json.loads((ROOT / "valid" / "authorized-action.json").read_text())
    data["authority"]["granted_at"] = "2026-09-16T17:00:00Z"
    data["timestamps"]["occurred_at"] = "2026-09-16T16:59:59Z"
    report = validate_governance_record_data(data)
    assert next(r for r in report.rules if r.rule_id == "GR-AUTH-002").result == "fail"


def test_accepted_handoff_requires_nonempty_transfer_scope() -> None:
    data = json.loads((ROOT / "valid" / "orchestrator-handoff.json").read_text())
    data["handoff"]["authority_transfer"]["scope"] = []
    report = validate_governance_record_data(data)
    assert next(r for r in report.rules if r.rule_id == "GR-HANDOFF-001").result == "fail"


def test_accepted_handoff_requires_valid_acceptance_timestamp() -> None:
    data = json.loads((ROOT / "valid" / "orchestrator-handoff.json").read_text())
    data["handoff"]["acceptance"]["accepted_at"] = "not-a-timestamp"
    report = validate_governance_record_data(data)
    assert next(r for r in report.rules if r.rule_id == "GR-HANDOFF-001").result == "fail"


def test_report_remains_machine_readable_and_shared() -> None:
    report = validate_governance_record_contract(ROOT / "valid" / "authorized-action.json")
    payload = report.to_dict()
    json.dumps(payload)
    assert payload["gc_report_version"] == "1.0.0"
    assert payload["spec"] == "governance-record"
