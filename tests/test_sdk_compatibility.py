"""GC-SDK.05 compatibility policy tests."""
import json
from pathlib import Path

from governance_commons.versioning import (
    check_registered_spec_compatibility,
    check_spec_compatibility,
    parse_version,
)

FIXTURE = Path(__file__).parent / "fixtures" / "versioning" / "compatibility-cases.json"


def test_fixture_matrix_matches_policy() -> None:
    cases = json.loads(FIXTURE.read_text(encoding="utf-8"))["cases"]
    for case in cases:
        if "current" in case:
            result = check_spec_compatibility(
                case["spec"], case["version"],
                current_version=case["current"],
                minimum_compatible_version=case["minimum"],
            )
        else:
            result = check_registered_spec_compatibility(case["spec"], case["version"])
        assert result.status == case["expected"], (case, result)


def test_current_versions_are_supported() -> None:
    for spec, version in (("ons", "1.4.0"), ("agent-dossier", "1.4.0"), ("governance-record", "1.0.0"), ("capabilities", "0.1")):
        assert check_registered_spec_compatibility(spec, version).status == "supported"


def test_explicit_older_compatibility_range_is_distinct_from_current_support() -> None:
    result = check_spec_compatibility("example", "1.2.0", current_version="1.4.0", minimum_compatible_version="1.2.0")
    assert result.status == "compatible"


def test_repository_does_not_claim_older_schema_support_without_an_explicit_range() -> None:
    assert check_registered_spec_compatibility("governance-record", "0.9.0").status == "unsupported"


def test_future_major_version_is_unsupported() -> None:
    assert check_registered_spec_compatibility("ons", "2.0.0").status == "unsupported"


def test_malformed_version_is_invalid() -> None:
    assert check_registered_spec_compatibility("ons", "1.x.0").status == "invalid"


def test_two_part_capability_version_is_supported() -> None:
    parsed = parse_version("0.1")
    assert parsed is not None
    assert (parsed.major, parsed.minor, parsed.patch) == (0, 1, 0)


def test_unknown_spec_is_not_silently_accepted() -> None:
    assert check_registered_spec_compatibility("unknown", "1.0.0").status == "unsupported"
