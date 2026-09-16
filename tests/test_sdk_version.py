from pathlib import Path
import re

import governance_commons

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = "0.2.0"


def test_python_sdk_version_is_0_2_0() -> None:
    assert governance_commons.__version__ == EXPECTED
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert re.search(r'^version\s*=\s*"0\.2\.0"\s*$', pyproject, re.MULTILINE)


def test_python_sdk_0_2_exports_current_public_surfaces() -> None:
    expected = {
        "validate_name",
        "validate_capability_contract",
        "discover_capabilities",
        "classify_spec_version",
        "validate_governance_record_contract",
    }
    namespace = governance_commons.__dict__
    assert expected <= namespace.keys()


def test_sdk_0_2_does_not_claim_typescript_contract_parity() -> None:
    package = (ROOT / "package.json").read_text(encoding="utf-8")
    assert '"version": "0.2.0"' in package
    assert '"./ons"' in package
    assert '"./report"' in package
    assert '"./capabilities"' not in package
    assert '"./governance-record"' not in package
