"""Adversarial checks: status changes alone never constitute independent evidence."""
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
authored = copy.deepcopy(manifest)
authored["independent_author_review"] = "accepted"
authored["round_trip_semantic_equivalence_verified"] = True
authored["human_release_approval"] = True
authored["fixtures"] = [
    {"id": "external-positive", "provenance": "reviewer evidence pending",
     "expected_result": "accept", "criterion_oracle": "review pending"},
    {"id": "external-negative", "provenance": "reviewer evidence pending",
     "expected_result": "reject", "criterion_oracle": "review pending"},
]
result = mod.assess(reviewed, authored)
assert not result["eligible"]
assert len(result["blockers"]) >= 4

# Plausible but unsupported approval objects must not bypass the evidence contract.
authored["release_approval_evidence"] = {"approver": "pending", "approval_date": "pending",
                                         "governance_record_reference": "pending", "scope": "pending"}
assert "attributable human release approval missing" in mod.assess(reviewed, authored)["blockers"]

# A source inventory that loses a criterion cannot be independently accepted.
short = copy.deepcopy(reviewed)
short["criteria"] = short["criteria"][:-1]
assert "29-criterion coverage incomplete" in mod.assess(short, authored)["blockers"]

# Duplicate fixture IDs are invalid even if their metadata is otherwise present.
authored["fixtures"][1]["id"] = authored["fixtures"][0]["id"]
assert "independent fixture provenance, oracle, execution or coverage incomplete" in mod.assess(reviewed, authored)["blockers"]
print("PASS: forged status flags, placeholder evidence, missing criteria and duplicate fixtures rejected")
