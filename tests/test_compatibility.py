"""GC-SDK.05 specification compatibility policy tests."""
from __future__ import annotations

import json
from pathlib import Path

from governance_commons.compatibility import (
    CompatibilityStatus,
    SUPPORTED_SPEC_VERSIONS,
    classify_spec_version,
    compatibility_rule,
)

ROOT = Path(__file__).parent / "fixtures" / "compatibility"


def _fixture(name: str) -> dict[str, str]:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_representative_version_fixtures() -> None:
    for name in (
        "current.json",
        "compatible-older.json",
        "unsupported-future.json",
        "incompatible-older.json",
        "invalid.json",
    ):
        fixture = _fixture(name)
        status = classify_spec_version(fixture["spec"], fixture["declared_version"])
        assert status.value == fixture["expected"], (name, status, fixture)


def test_pre_1_0_minor_is_the_compatibility_boundary() -> None:
    assert classify_spec_version("capabilities", "0.1") is CompatibilityStatus.CURRENT
    assert classify_spec_version("capabilities", "0.1.0") is CompatibilityStatus.CURRENT
    assert classify_spec_version("capabilities", "0.1.1") is CompatibilityStatus.UNSUPPORTED_FUTURE
    assert classify_spec_version("capabilities", "0.0.9") is CompatibilityStatus.INCOMPATIBLE_OLDER
    assert classify_spec_version("capabilities", "0.2.0") is CompatibilityStatus.UNSUPPORTED_FUTURE


def test_stable_specs_allow_older_versions_within_same_major() -> None:
    assert classify_spec_version("ons", "1.3.0") is CompatibilityStatus.COMPATIBLE_OLDER
    assert classify_spec_version("ons", "1.4.0") is CompatibilityStatus.CURRENT
    assert classify_spec_version("ons", "1.4.1") is CompatibilityStatus.UNSUPPORTED_FUTURE
    assert classify_spec_version("ons", "2.0.0") is CompatibilityStatus.UNSUPPORTED_FUTURE
    assert classify_spec_version("ons", "0.9.0") is CompatibilityStatus.INCOMPATIBLE_OLDER


def test_unknown_specs_and_invalid_versions_are_explicit() -> None:
    assert classify_spec_version("not-a-spec", "1.0.0") is CompatibilityStatus.UNKNOWN_SPEC
    assert classify_spec_version("ons", "1.x") is CompatibilityStatus.INVALID
    assert classify_spec_version("ons", "") is CompatibilityStatus.INVALID


def test_compatibility_rule_uses_shared_rule_result_shape() -> None:
    current = compatibility_rule("governance-record", "1.0.0")
    assert current.rule_id == "GC-SDK-COMPAT-001"
    assert current.result == "pass"

    older = compatibility_rule("ons", "1.3.0")
    assert older.result == "skip"
    assert "schema compatibility" in (older.message or "")

    future = compatibility_rule("governance-record", "2.0.0")
    assert future.result == "fail"
    assert "newer" in (future.message or "")


def test_registry_has_one_explicit_current_version_per_supported_spec() -> None:
    assert SUPPORTED_SPEC_VERSIONS == {
        "ons": "1.4.0",
        "capabilities": "0.1",
        "dossier": "1.4.0",
        "governance-record": "1.0.0",
    }
