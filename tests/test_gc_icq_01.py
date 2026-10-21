"""GC-ICQ standalone gate regression tests."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "specs" / "gc-icq" / "1.0.0"
spec = importlib.util.spec_from_file_location("icq_gate", ROOT / "publication-gate.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
FIXTURES = json.loads((ROOT / "fixtures.json").read_text())

def test_public_approved_q3_passes():
    assert module.may_publish(FIXTURES["valid"][0])

def test_exposed_credential_never_publishes():
    assert not module.may_publish(FIXTURES["valid"][1])

def test_wrong_quadrant_fails_closed():
    assert not module.may_publish(FIXTURES["invalid"][0])

def test_missing_human_approval_fails_closed():
    assert not module.may_publish(FIXTURES["invalid"][1])

def test_sensitive_label_blocks_even_approved():
    r = {**FIXTURES["valid"][0], "dataLabels": ["PERSONAL_DATA"]}
    assert not module.may_publish(r)

def test_q4_exception_does_not_override_publication_gate():
    r = {**FIXTURES["valid"][1], "dataLabels": [],
         "exception": {"authority": "owner", "rationale": "controlled disclosure",
                       "expiresAt": "2099-01-01T00:00:00Z", "mitigations": ["restricted audience"]}}
    assert module.q4_exception_valid(r)
    assert not module.may_publish(r)
