"""Guard OECD source-audit claims independently of profile adapter fixtures."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
read = lambda name: json.loads((ROOT / name).read_text(encoding="utf-8"))
audit = read("oecd-source-audit.json")
mapping = read("oecd-criteria-map.json")
acceptance = read("acceptance-status.json")
optional = read("oecd-optional/schema.json")
assert audit["phase"] == "GC-INCIDENT.07"
assert audit["source"]["doi"] == mapping["source"]["doi"]
assert audit["source"]["published"] == "2025-02-28"
assert any(x["claim"] == "framework_criteria_count" and x["value"] == 29 for x in audit["verified_claims"])
assert len(mapping["criteria"]) == 29
assert sorted(x["criterion"] for x in mapping["criteria"]) == list(range(1, 30))
assert sum(x["mandatory"] is True for x in mapping["criteria"]) == 7
assert set(optional["properties"]) == {str(i).zfill(2) for i in range(1,30) if i not in {1,2,3,4,7,10,11}}
assert audit["interoperability_verified"] is False
assert audit["release_eligible"] is False
assert acceptance["release_eligible"] is False
assert acceptance["oecd_conformant"] is False
assert "controlled_vocabularies" in audit["unverified_claims"]
print("PASS: OECD source evidence, 29-field structural inventory, and non-conformance boundaries")
