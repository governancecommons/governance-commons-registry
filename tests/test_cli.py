"""Tests for governance_commons.cli — gc-validate and gc-report (GC-2-A-04)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _write_json(tmp_path: Path, data: object, filename: str = "input.json") -> Path:
    p = tmp_path / filename
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


def _validate(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.argv = ['gc-validate'] + sys.argv[1:];"
         "from governance_commons.cli import validate_cmd; validate_cmd()",
         *args], capture_output=True, text=True,
    )


def _report(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.argv = ['gc-report'] + sys.argv[1:];"
         "from governance_commons.cli import report_cmd; report_cmd()",
         *args], capture_output=True, text=True,
    )


class TestGcValidate:
    def test_exit_0_all_pass(self, tmp_path: Path) -> None:
        f = _write_json(tmp_path, {"checks": [
            {"domain": "python_identifier", "name": "run_intent"},
            {"domain": "governance_cluster", "name": "ONS"},
        ]})
        result = _validate("--spec", "ons", "--profile", "standard", str(f))
        assert result.returncode == 0

    def test_text_output_pass(self, tmp_path: Path) -> None:
        f = _write_json(tmp_path, {"checks": [{"domain": "python_identifier", "name": "run_intent"}]})
        result = _validate("--spec", "ons", "--output", "text", str(f))
        assert "PASS" in result.stdout
        assert "ONS-CASING-001" in result.stdout

    def test_json_output_structure(self, tmp_path: Path) -> None:
        f = _write_json(tmp_path, {"checks": [{"domain": "python_identifier", "name": "run_intent"}]})
        result = _validate("--spec", "ons", "--output", "json", str(f))
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["gc_report_version"] == "1.0.0"
        assert data["spec"] == "ons"
        assert data["conformant"] is True
        assert data["summary"]["passed"] == 1
        assert data["summary"]["failed"] == 0

    def test_exit_1_on_failure(self, tmp_path: Path) -> None:
        f = _write_json(tmp_path, {"checks": [{"domain": "python_identifier", "name": "RunIntent"}]})
        result = _validate("--spec", "ons", str(f))
        assert result.returncode == 1
        assert json.loads(_validate("--spec", "ons", "--output", "json", str(f)).stdout)["conformant"] is False

    def test_exit_2_invalid_subject(self, tmp_path: Path) -> None:
        result = _validate("--spec", "ons", str(tmp_path / "missing.json"))
        assert result.returncode == 2

    def test_exit_2_malformed_subject(self, tmp_path: Path) -> None:
        f = _write_json(tmp_path, {"not_checks": []})
        result = _validate("--spec", "ons", str(f))
        assert result.returncode == 2


class TestGcReport:
    def _saved_report(self, tmp_path: Path, conformant: bool = True) -> Path:
        from governance_commons.report import RuleResult, build_report
        rules = [RuleResult("ONS-CASING-001", "snake_case", "pass" if conformant else "fail",
                            None if conformant else "bad name")]
        r = build_report(spec="ons", spec_version="1.4.0", profile="standard",
                         subject="test.json", generated_at="2026-06-07T00:00:00Z", rules=rules)
        return _write_json(tmp_path, r.to_dict(), "report.json")

    def test_exit_0_conformant_report(self, tmp_path: Path) -> None:
        assert _report(str(self._saved_report(tmp_path))).returncode == 0

    def test_exit_1_nonconformant_report(self, tmp_path: Path) -> None:
        assert _report(str(self._saved_report(tmp_path, conformant=False))).returncode == 1

    def test_text_output_shows_spec(self, tmp_path: Path) -> None:
        result = _report("--output", "text", str(self._saved_report(tmp_path)))
        assert "ons" in result.stdout
        assert "1.4.0" in result.stdout

    def test_json_output_round_trips(self, tmp_path: Path) -> None:
        p = self._saved_report(tmp_path)
        result = _report("--output", "json", str(p))
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["gc_report_version"] == "1.0.0"
        assert data["summary"]["passed"] == 1

    def test_exit_2_missing_file(self, tmp_path: Path) -> None:
        assert _report(str(tmp_path / "missing.json")).returncode == 2

    def test_exit_2_invalid_json(self, tmp_path: Path) -> None:
        p = tmp_path / "bad.json"
        p.write_text("not json", encoding="utf-8")
        assert _report(str(p)).returncode == 2

    def test_exit_2_unsupported_report_version(self, tmp_path: Path) -> None:
        p = self._saved_report(tmp_path)
        data = json.loads(p.read_text(encoding="utf-8"))
        data["gc_report_version"] = "9.9.9"
        p.write_text(json.dumps(data), encoding="utf-8")
        result = _report(str(p))
        assert result.returncode == 2
        assert "report version '9.9.9' is not supported" in result.stderr
