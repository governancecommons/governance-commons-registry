"""Exercise semantic preservation and explicit information-loss boundaries."""
import copy
from export_adapter import load
from round_trip_probe import analyze, reconstruct

adapter = load("oecd-mandatory-valid.json")
view = {
    "incident_id": adapter["incident_id"],
    "title": adapter["title"],
    "description": adapter["description"],
    "system_relationships": copy.deepcopy(adapter["system_relationships"]),
    "severity": copy.deepcopy(adapter["severity"]),
    "harm_types": copy.deepcopy(adapter["harm_types"]),
    "supporting_materials": [
        {"kind": m["kind"], "reference": m["reference"]}
        for m in adapter["supporting_materials"]
    ],
}
findings = analyze(adapter, view)
assert {f["kind"] for f in findings} == {"intentionally_omitted"}
assert {f["field"] for f in findings} == {"submitter", "supporting_materials.sensitivity"}
for key in ("system_relationships", "severity", "harm_types"):
    changed = copy.deepcopy(view)
    changed[key] = [] if key == "system_relationships" else {"categories": ["other"]}
    assert {"field": key, "kind": "changed_or_missing"} in analyze(adapter, changed)
changed = copy.deepcopy(view)
changed["submitter"] = copy.deepcopy(adapter["submitter"])
assert {"field": "submitter", "kind": "privacy_boundary_breached"} in analyze(adapter, changed)
changed = copy.deepcopy(view)
changed["supporting_materials"] = []
assert {"field": "supporting_materials", "kind": "unexpected_transformation"} in analyze(adapter, changed)
try:
    reconstruct(adapter, view)
except ValueError:
    pass
else:
    raise AssertionError("Lossy reconstruction must fail closed")
print("PASS: retained fields, intentional losses, tampering and reconstruction refusal")
print("NOT a verified OECD -> GC -> OECD round trip")
