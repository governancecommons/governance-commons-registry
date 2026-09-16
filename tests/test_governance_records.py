"""A5.5 Governance Record structural and semantic conformance tests."""
from __future__ import annotations

import json
from pathlib import Path

from governance_commons.governance_records import validate_governance_record_contract

ROOT = Path(__file__).parent / "fixtures" / "governance-record"


def _files(group: str) -> list[Path]:
    return sorted((ROOT / group).glob("*.json"))


def test_valid_fixtures_are_conformant() -> None:
    for path in _files("valid"):
        report = validate_governance_record_contract(path)
        assert report.conformant, (path.name, report.to_dict())
        assert report.gc_report_version == "1.0.0"
        assert report.spec == "governance-record"


def test_invalid_fixtures_fail_schema() -> None:
    for path in _files("invalid"):
        report = validate_governance_record_contract(path)
        assert not report.conformant, (path.name, report.to_dict())
        assert any(r.rule_id == "GR-SCHEMA-001" and r.result == "fail" for r in report.rules)


def test_unauthorized_action_is_schema_valid_but_governance_invalid() -> None:
    report = validate_governance_record_contract(ROOT / "governance-rules" / "unauthorized-action.json")
    assert report.rules[0].rule_id == "GR-SCHEMA-001"
    assert report.rules[0].result == "pass"
    rule = next(r for r in report.rules if r.rule_id == "GR-AUTH-001")
    assert rule.result == "fail"
    assert not report.conformant


def test_revoked_authority_is_temporal() -> None:
    report = validate_governance_record_contract(ROOT / "governance-rules" / "revoked-authority-action.json")
    assert any(r.rule_id == "GR-SCHEMA-001" and r.result == "pass" for r in report.rules)
    rule = next(r for r in report.rules if r.rule_id == "GR-AUTH-002")
    assert rule.result == "fail"


def test_accepted_handoff_requires_governance_completeness() -> None:
    report = validate_governance_record_contract(ROOT / "governance-rules" / "incomplete-handoff.json")
    assert any(r.rule_id == "GR-SCHEMA-001" and r.result == "pass" for r in report.rules)
    assert next(r for r in report.rules if r.rule_id == "GR-HANDOFF-001").result == "fail"


def test_report_is_machine_readable() -> None:
    report = validate_governance_record_contract(ROOT / "valid" / "authorized-action.json")
    json.dumps(report.to_dict())
