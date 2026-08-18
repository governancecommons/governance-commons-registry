"""Capability Contract v0.1 validator and discovery tests."""
from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from governance_commons.capabilities import (
    CAPABILITY_RELATIVE_PATH,
    discover_capabilities,
    validate_capability_contract,
    validate_capability_data,
)


def _minimal() -> dict:
    return {
        "schema_version": "0.1",
        "component": {
            "id": "example-component",
            "name": "Example Component",
            "type": "application",
            "status": "active",
        },
        "provides": [],
    }


def _provided(capability_id: str = "asset.palette.generate") -> dict:
    data = _minimal()
    data["provides"] = [{
        "id": capability_id,
        "version": "1.0",
        "stability": "stable",
        "summary": "Generate a deterministic palette.",
        "interfaces": ["cli.asset.palette.generate"],
    }]
    return data


def _write_contract(root: Path, data: dict, *, raw: str | None = None) -> Path:
    path = root / CAPABILITY_RELATIVE_PATH
    path.parent.mkdir(parents=True)
    path.write_text(raw if raw is not None else yaml.safe_dump(data), encoding="utf-8")
    return path


def test_valid_minimal_pure_consumer_and_complete_contracts() -> None:
    minimal = _minimal()
    assert validate_capability_data(minimal).valid

    consumer = _minimal()
    consumer["consumes"] = [{
        "id": "governance.artifact.validate",
        "requirement": "required",
        "version": ">=1.0",
    }]
    assert validate_capability_data(consumer).valid

    complete = _provided()
    complete["component"]["version"] = "1.2.3"
    complete["prohibits"] = [{
        "capability": "release.package.publish",
        "reason": "Publishing belongs to the release workflow.",
    }]
    complete["metadata"] = {"repository": "owner/example"}
    assert validate_capability_data(complete).valid


@pytest.mark.parametrize("capability_id", [
    "a.b.c",
    "asset-pipeline.image_asset.convert-file",
    "governance.artifact.validate",
])
def test_valid_capability_id_grammar(capability_id: str) -> None:
    assert validate_capability_data(_provided(capability_id)).valid


@pytest.mark.parametrize("capability_id", [
    "a.b",
    "a.b.c.d",
    "Asset.image.convert",
    "asset..convert",
    "asset.-image.convert",
    "asset.image_.convert",
])
def test_invalid_capability_id_grammar(capability_id: str) -> None:
    result = validate_capability_data(_provided(capability_id))
    assert not result.valid
    assert any(issue.rule_id == "GC-CAP-SCHEMA-001" for issue in result.issues)


@pytest.mark.parametrize("version", ["1.0", "1.0.0", ">=1.0", "<=2.3.4", "^1.2", "~1.2.3"])
def test_valid_consumed_version_requirements(version: str) -> None:
    data = _minimal()
    data["consumes"] = [{
        "id": "asset.image.convert",
        "requirement": "optional",
        "version": version,
    }]
    assert validate_capability_data(data).valid


@pytest.mark.parametrize("version", ["1", "latest", ">=1.0 <2.0", "1.2.3.4", "1.*"])
def test_invalid_consumed_version_requirements(version: str) -> None:
    data = _minimal()
    data["consumes"] = [{
        "id": "asset.image.convert",
        "requirement": "optional",
        "version": version,
    }]
    assert not validate_capability_data(data).valid


def test_yaml_numeric_coercion_is_rejected(tmp_path: Path) -> None:
    raw = """schema_version: 0.1
component:
  id: example
  name: Example
  type: cli
  version: 1.0
  status: active
provides: []
"""
    path = _write_contract(tmp_path, {}, raw=raw)
    result = validate_capability_contract(path)
    assert not result.valid
    issue_paths = {issue.path for issue in result.issues}
    assert "$.schema_version" in issue_paths
    assert "$.component.version" in issue_paths


def test_schema_defaults_do_not_mutate_input() -> None:
    data = _minimal()
    original = copy.deepcopy(data)
    assert validate_capability_data(data).valid
    assert data == original
    assert "consumes" not in data
    assert "prohibits" not in data


def test_semantic_duplicate_provided_id() -> None:
    data = _provided()
    data["provides"].append(copy.deepcopy(data["provides"][0]))
    result = validate_capability_data(data)
    assert [issue.rule_id for issue in result.issues] == ["GC-CAP-SEMANTIC-001"]


def test_semantic_provided_prohibited_conflict() -> None:
    data = _provided()
    data["prohibits"] = [{
        "capability": "asset.palette.generate",
        "reason": "Intentional conflict fixture.",
    }]
    result = validate_capability_data(data)
    assert [issue.rule_id for issue in result.issues] == ["GC-CAP-SEMANTIC-002"]


def test_semantic_duplicate_interface_reference() -> None:
    data = _provided()
    data["provides"][0]["interfaces"].append("cli.asset.palette.generate")
    result = validate_capability_data(data)
    assert [issue.rule_id for issue in result.issues] == ["GC-CAP-SEMANTIC-003"]


def test_invalid_yaml_is_reported(tmp_path: Path) -> None:
    path = _write_contract(tmp_path, {}, raw="component: [\n")
    result = validate_capability_contract(path)
    assert not result.valid
    assert result.issues[0].rule_id == "GC-CAP-INPUT-002"


def test_discovery_zero_one_and_multiple_providers(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    assert discover_capabilities([empty], "asset.palette.generate").scanned_contracts == 0

    first = tmp_path / "first"
    first_data = _provided()
    first_data["component"]["id"] = "first-provider"
    first_data["metadata"] = {"repository": "owner/first"}
    _write_contract(first, first_data)

    second = tmp_path / "second"
    second_data = _provided()
    second_data["component"]["id"] = "second-provider"
    second_data["provides"][0]["version"] = "2.0"
    _write_contract(second, second_data)

    one = discover_capabilities([first], "asset.palette.generate")
    assert one.valid
    assert [provider["component_id"] for provider in one.providers] == ["first-provider"]

    multiple = discover_capabilities([second, first], "asset.palette.generate")
    assert multiple.valid
    assert [provider["component_id"] for provider in multiple.providers] == [
        "first-provider", "second-provider"
    ]
    assert multiple.to_dict()["authority_evaluated"] is False
    assert multiple.to_dict()["execution_authority"] == "not_evaluated"


def test_discovery_reports_invalid_contract_deterministically(tmp_path: Path) -> None:
    valid_root = tmp_path / "valid"
    invalid_root = tmp_path / "invalid"
    _write_contract(valid_root, _provided())
    invalid = _provided("too.many.id.segments")
    _write_contract(invalid_root, invalid)

    result = discover_capabilities([invalid_root, valid_root])
    assert not result.valid
    assert len(result.providers) == 1
    assert len(result.invalid_contracts) == 1
    assert result.invalid_contracts[0].issues[0].path == "$.provides[0].id"


def test_unrelated_roots_do_not_interfere(tmp_path: Path) -> None:
    provider = tmp_path / "provider"
    unrelated = tmp_path / "unrelated"
    _write_contract(provider, _provided())
    unrelated.mkdir()
    result = discover_capabilities([unrelated, provider], "asset.palette.generate")
    assert len(result.providers) == 1
    assert result.scanned_contracts == 1
