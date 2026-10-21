"""Verify conservative projection and private-source round-trip invariants."""
import copy
from export_adapter import load
from semantic_bridge import project, recover, MappingError
from internal_interchange import InterchangeError

adapter = load("oecd-mandatory-valid.json")
timeline = {"first_known_at": "2026-10-19T09:00:00Z", "reported_at": "2026-10-19T10:00:00Z"}
def rejects(fn):
    try:
        fn()
    except (MappingError, InterchangeError):
        return
    raise AssertionError("Expected fail-closed rejection")

rejects(lambda: project(adapter, authorized=True))
rejects(lambda: project(adapter, timeline=timeline))
result = project(adapter, authorized=True, timeline=timeline)
assert result["semantic_equivalence_verified"] is False
assert result["mapping_issues"]
assert result["profile"]["disclosure"]["publication_status"] == "draft"
assert result["profile"]["review"]["status"] == "pending"
assert result["profile"]["affected_systems"][0]["relationship"] == "unknown"
assert recover(result, authorized=True) == adapter
rejects(lambda: recover(result))
for field, value in [("title", "changed"), ("incident_id", "different"), ("description", "changed")]:
    bad = copy.deepcopy(result)
    bad["profile"][field] = value
    rejects(lambda b=bad: recover(b, authorized=True))
bad = copy.deepcopy(result)
bad["semantic_equivalence_verified"] = True
rejects(lambda: recover(bad, authorized=True))
bad = copy.deepcopy(result)
bad["mapping_issues"] = []
rejects(lambda: recover(bad, authorized=True))
for section, key, value in [
    ("severity", "status", "assessed"),
    ("harm", "status", "reported"),
    ("affected_systems", None, "involved"),
    ("disclosure", "publication_status", "approved_for_release"),
    ("review", "status", "approved"),
]:
    bad = copy.deepcopy(result)
    if section == "affected_systems":
        bad["profile"][section][0]["relationship"] = value
    else:
        bad["profile"][section][key] = value
    rejects(lambda b=bad: recover(b, authorized=True))
bad = copy.deepcopy(result)
bad["mapping_issues"] = ["all OECD categories verified"]
rejects(lambda: recover(bad, authorized=True))
print("PASS rejected unsupported classification promotion and loss-accounting tampering")
print("PASS: restricted GC projection, explicit semantic gaps, private source recovery and refusal tests")
print("Source recovery is NOT GC-native semantic round-trip equivalence")
