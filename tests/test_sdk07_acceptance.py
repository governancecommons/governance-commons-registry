"""GC-SDK.07 acceptance gate for Capability Contract v0.1 adoption."""
from __future__ import annotations

from pathlib import Path

from governance_commons.capabilities import (
    CAPABILITY_CONTRACT_VERSION,
    CAPABILITY_RELATIVE_PATH,
    discover_capabilities,
    validate_capability_contract,
)

ROOT = Path(__file__).parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "capability-adoption"


def test_registry_declares_canonical_capability_contract() -> None:
    path = ROOT / CAPABILITY_RELATIVE_PATH
    result = validate_capability_contract(path)
    assert result.valid, result.to_dict()
    assert result.component_id == "governance-commons-registry"
    assert CAPABILITY_CONTRACT_VERSION == "0.1"


def test_adopter_profiles_cover_provider_consumer_and_hybrid_usage() -> None:
    expected = {"provider.yaml", "consumer.yaml", "provider-consumer.yaml", "invalid-conflict.yaml"}
    actual = {path.name for path in FIXTURES.glob("*.yaml")}
    assert actual == expected

    for filename in sorted(expected - {"invalid-conflict.yaml"}):
        result = validate_capability_contract(FIXTURES / filename)
        assert result.valid, (filename, result.to_dict())


def test_invalid_adoption_is_rejected_by_semantic_boundary() -> None:
    result = validate_capability_contract(FIXTURES / "invalid-conflict.yaml")
    assert not result.valid
    assert [issue.rule_id for issue in result.issues] == ["GC-CAP-SEMANTIC-002"]


def test_discovery_resolves_multiple_adopters_without_authority_evaluation() -> None:
    result = discover_capabilities(
        [FIXTURES / "provider.yaml", FIXTURES / "provider-consumer.yaml"],
        "asset.palette.generate",
    )
    assert result.valid
    assert [provider["component_id"] for provider in result.providers] == [
        "example-hybrid",
        "example-provider",
    ]
    assert result.to_dict()["authority_evaluated"] is False
    assert result.to_dict()["execution_authority"] == "not_evaluated"


def test_discovery_can_scan_canonical_registry_contract() -> None:
    result = discover_capabilities([ROOT], "governance.contract.validate")
    assert result.valid
    assert [provider["component_id"] for provider in result.providers] == [
        "governance-commons-registry"
    ]
    assert result.providers[0]["validation_status"] == "valid"
