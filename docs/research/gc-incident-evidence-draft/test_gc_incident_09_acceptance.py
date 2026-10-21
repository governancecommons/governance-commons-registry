"""Mutation tests for GC-INCIDENT.09 reviewer gate."""
import copy
import importlib.util
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("acceptance", ROOT / "gc-incident-09-acceptance.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
primary = json.loads((ROOT / "oecd-annex-b-primary-review.json").read_text())
manifest = json.loads((ROOT / "independent-fixture-manifest.json").read_text())
baseline = mod.assess(primary, manifest)
assert not baseline["eligible"]
assert len(baseline["blockers"]) >= 4
reviewed = copy.deepcopy(primary)
for row in reviewed["criteria"]:
    row["independent_human_review"] = "accepted"
assert not mod.assess(reviewed, manifest)["eligible"]
authored = copy.deepcopy(manifest)
authored["independent_author_review"] = "accepted"
authored["fixtures"] = [
    {"id": "external-positive", "provenance": "reviewer evidence pending", "expected_result": "accept", "criterion_oracle": "review pending"},
    {"id": "external-negative", "provenance": "reviewer evidence pending", "expected_result": "reject", "criterion_oracle": "review pending"},
]
assert not mod.assess(reviewed, authored)["eligible"]
authored["round_trip_semantic_equivalence_verified"] = True
assert not mod.assess(reviewed, authored)["eligible"]
authored["human_release_approval"] = True
assert mod.assess(reviewed, authored)["eligible"]
authored["fixtures"] = authored["fixtures"][:1]
assert not mod.assess(reviewed, authored)["eligible"]
print("PASS: reviewer acceptance gate blocks missing evidence and only clears complete declared fields")
