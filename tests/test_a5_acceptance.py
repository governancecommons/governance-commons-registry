"""A5 acceptance gate for the Governance Record contract and rule boundary."""
from __future__ import annotations

from pathlib import Path

from governance_commons.governance_records import validate_governance_record_contract

ROOT = Path(__file__).parent / "fixtures" / "governance-record"

VALID_RECORD_TYPES = {
    "observation.json",
    "intent.json",
    "decision.json",
    "human-approval.json",
    "authorized-action.json",
    "dispatch.json",
    "orchestrator-handoff.json",
    "escalation.json",
    "validation.json",
    "conformance.json",
    "certification.json",
    "registration.json",
    "revocation.json",
    "provenance.json",
}

INVALID_RECORDS = {
    "unknown-record-type.json",
    "wrong-schema-version.json",
    "missing-approval.json",
    "incomplete-handoff.json",
    "missing-action.json",
    "malformed-reference.json",
}


def test_a5_acceptance_covers_all_representative_fixtures() -> None:
    actual = {path.name for path in (ROOT / "valid").glob("*.json")}
    assert actual == VALID_RECORD_TYPES
    assert {path.name for path in (ROOT / "invalid").glob("*.json")} == INVALID_RECORDS


def test_a5_valid_fixtures_are_schema_and_governance_conformant() -> None:
    for path in sorted((ROOT / "valid").glob("*.json")):
        report = validate_governance_record_contract(path)
        assert report.conformant, (path.name, report.to_dict())
        assert report.gc_report_version == "1.0.0"
        assert report.spec == "governance-record"
        assert report.spec_version == "1.0.0"
        assert report.conformance_level == "standard"


def test_a5_structurally_invalid_fixtures_are_rejected_before_semantic_rules() -> None:
    for path in sorted((ROOT / "invalid").glob("*.json")):
        report = validate_governance_record_contract(path)
        assert not report.conformant, (path.name, report.to_dict())
        assert report.rules[0].rule_id == "GR-SCHEMA-001"
        assert report.rules[0].result == "fail"
        assert all(
            rule.rule_id == "GR-SCHEMA-001" for rule in report.rules
        )


def test_a5_governance_rule_fixtures_separate_structure_from_semantics() -> None:
    expected_failures = {
        "unauthorized-action.json": "GR-AUTH-001",
        "revoked-authority-action.json": "GR-AUTH-002",
        "incomplete-handoff.json": "GR-HANDOFF-001",
    }
    for filename, rule_id in expected_failures.items():
        path = ROOT / "governance-rules" / filename
        report = validate_governance_record_contract(path)
        assert not report.rules[0].result == "fail", (filename, report.to_dict())
        assert report.rules[0].rule_id == "GR-SCHEMA-001"
        assert report.rules[0].result == "pass"
        assert next(rule for rule in report.rules if rule.rule_id == rule_id).result == "fail"
        assert not report.conformant


def test_a5_shared_conformance_report_boundary_is_preserved() -> None:
    report = validate_governance_record_contract(ROOT / "valid" / "authorized-action.json")
    payload = report.to_dict()
    assert payload["gc_report_version"] == "1.0.0"
    assert set(payload) >= {
        "gc_report_version",
        "spec",
        "spec_version",
        "profile",
        "subject",
        "generated_at",
        "rules",
        "summary",
        "conformant",
        "conformance_level",
    }
    assert "conformance_report" not in payload
