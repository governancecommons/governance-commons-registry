"""Fail closed if the GC–INCIDENT.08 research manifest claims unsupported readiness."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "independent-fixture-manifest.json").read_text(encoding="utf-8"))
assert manifest["phase"] == "GC-INCIDENT.08"
assert manifest["source_doi"] == "10.1787/f326d4ac-en"
assert manifest["normative"] is False
assert manifest["interoperability_verified"] is False
assert manifest["release_eligible"] is False
assert manifest["independent_author_review"] == "pending"
assert manifest["status"] == "design_baseline"
assert manifest["fixtures"] == []
assert len(set(manifest["blocking_gates"])) == 4
assert {"id", "provenance", "expected_result", "criterion_oracle"} == set(manifest["fixture_contract"]["required"])
assert set(manifest["fixture_contract"]["expected_result_values"]) == {"accept", "reject"}
print("PASS: GC-INCIDENT.08 research-only fixture design gate")
