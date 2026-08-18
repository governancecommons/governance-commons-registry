"""CLI tests for capability validation and discovery."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

from governance_commons.capabilities import CAPABILITY_RELATIVE_PATH


def _contract(root: Path, capability_id: str = "asset.palette.generate") -> Path:
    path = root / CAPABILITY_RELATIVE_PATH
    path.parent.mkdir(parents=True)
    path.write_text(yaml.safe_dump({
        "schema_version": "0.1",
        "component": {
            "id": root.name,
            "name": root.name,
            "type": "cli",
            "status": "active",
        },
        "provides": [{
            "id": capability_id,
            "version": "1.0",
            "stability": "stable",
            "summary": "Test capability.",
        }],
    }), encoding="utf-8")
    return path


def _validate(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.argv = ['gc-validate'] + sys.argv[1:];"
         "from governance_commons.cli import validate_cmd; validate_cmd()",
         *args],
        capture_output=True,
        text=True,
    )


def _discover(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.argv = ['gc-discover'] + sys.argv[1:];"
         "from governance_commons.capabilities_cli import discover_cmd; discover_cmd()",
         *args],
        capture_output=True,
        text=True,
    )


def test_gc_validate_capabilities_text_and_json(tmp_path: Path) -> None:
    path = _contract(tmp_path)
    text_result = _validate("--spec", "capabilities", str(path))
    assert text_result.returncode == 0
    assert "PASS" in text_result.stdout
    assert "GC-CAP-SCHEMA-000" in text_result.stdout

    json_result = _validate("--spec", "capabilities", "--output", "json", str(path))
    assert json_result.returncode == 0
    report = json.loads(json_result.stdout)
    assert report["spec"] == "capabilities"
    assert report["spec_version"] == "0.1"
    assert report["conformant"] is True


def test_gc_validate_capabilities_failure(tmp_path: Path) -> None:
    path = _contract(tmp_path, "invalid.id")
    result = _validate("--spec", "capabilities", "--output", "json", str(path))
    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["conformant"] is False
    assert report["rules"][0]["rule_id"] == "GC-CAP-SCHEMA-001"


def test_gc_discover_query_and_authority_boundary(tmp_path: Path) -> None:
    first = tmp_path / "first-provider"
    second = tmp_path / "second-provider"
    _contract(first)
    _contract(second, "project.scaffold.create")
    result = _discover(
        "--capability", "asset.palette.generate",
        "--output", "json",
        str(second), str(first),
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["authority_evaluated"] is False
    assert payload["execution_authority"] == "not_evaluated"
    assert [provider["component_id"] for provider in payload["providers"]] == [
        "first-provider"
    ]


def test_gc_discover_exits_nonzero_when_any_contract_is_invalid(tmp_path: Path) -> None:
    valid = tmp_path / "valid"
    invalid = tmp_path / "invalid"
    _contract(valid)
    _contract(invalid, "too.many.id.segments")
    result = _discover("--output", "json", str(valid), str(invalid))
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert len(payload["providers"]) == 1
    assert len(payload["invalid_contracts"]) == 1
