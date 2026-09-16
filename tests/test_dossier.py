"""Agent Dossier instance validator tests (structural, v1.4.0 instance schema)."""
from __future__ import annotations

from pathlib import Path

from governance_commons.dossier import validate_dossier_contract

_FIXTURES = Path(__file__).parent / "fixtures" / "dossier"


def test_valid_instance() -> None:
    result = validate_dossier_contract(_FIXTURES / "valid" / "agent-dossier-instance.yaml")
    assert result.valid
    assert result.agent_id == "example-review-agent"
    assert result.issues == ()


def test_valid_instance_with_did_key() -> None:
    result = validate_dossier_contract(_FIXTURES / "valid" / "agent-dossier-instance-did-key.yaml")
    assert result.valid


def test_missing_identity_is_rejected() -> None:
    result = validate_dossier_contract(_FIXTURES / "invalid" / "agent-dossier-instance-missing-identity.yaml")
    assert not result.valid
    assert any("identity" in issue.message for issue in result.issues)


def test_empty_crypto_identity_is_rejected() -> None:
    result = validate_dossier_contract(
        _FIXTURES / "invalid" / "agent-dossier-instance-missing-crypto-identity.yaml"
    )
    assert not result.valid


def test_capability_claim_missing_declared_at_is_rejected() -> None:
    result = validate_dossier_contract(
        _FIXTURES / "invalid" / "agent-dossier-instance-capability-claim-missing-declared-at.yaml"
    )
    assert not result.valid
    assert any("declared_at" in issue.message for issue in result.issues)


def test_nonexistent_file_reports_input_error() -> None:
    result = validate_dossier_contract(_FIXTURES / "does-not-exist.yaml")
    assert not result.valid
    assert result.issues[0].rule_id == "GC-DOSSIER-INPUT-001"
