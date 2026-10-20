"""Adversarial checks for optional OECD adapter/public-export boundary."""
import copy
import json
from pathlib import Path
import runpy
import sys

from export_adapter import AdapterError, public_export

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
records = runpy.run_path(str(ROOT.parent / "test_cross_record.py"))["records"]
profile = json.loads((ROOT.parent / "fixtures/valid-minimal.json").read_text())
adapter = json.loads((ROOT / "oecd-mandatory-valid.json").read_text())

profile["description"] = adapter["description"]
profile["review"] = {
    "status": "approved",
    "reviewer": {"type": "human", "id": "alice"},
    "governance_record": {"type": "governance-record", "id": "gr-approval"},
}
profile["disclosure"] = {"classification": "public", "publication_status": "approved_for_release"}
profile["evidence_refs"][0]["sensitivity"] = "public"
adapter["supporting_materials"][0]["sensitivity"] = "public"


def reject(change, name):
    p, a = copy.deepcopy(profile), copy.deepcopy(adapter)
    change(p, a)
    try:
        public_export(p, a, records)
    except AdapterError:
        print("PASS rejected", name)
        return
    raise AssertionError("Failed to reject: " + name)


out = public_export(profile, adapter, records)
assert out["incident_id"] == "example-001"
assert "submitter" not in out and "reporter" not in out
assert "email" not in json.dumps(out)
assert "review" not in out
print("PASS public allowlist omits reporter contact and review identities")
reject(lambda p, a: a["supporting_materials"][0].update(sensitivity="restricted"), "restricted adapter material")
reject(lambda p, a: p["evidence_refs"][0].update(sensitivity="confidential"), "confidential profile evidence")
reject(lambda p, a: p["disclosure"].update(classification="restricted"), "restricted profile")
reject(lambda p, a: p["disclosure"].update(publication_status="draft"), "unapproved release")
reject(lambda p, a: p["review"].update(status="pending"), "unapproved review")
reject(lambda p, a: a.update(description="Different incident"), "mismatched description")
reject(lambda p, a: a["submitter"].update(role="deployer"), "mismatched reporter")
reject(lambda p, a: a["severity"].update(categories=["bogus"]), "invalid OECD taxonomy")
reject(lambda p, a: p.update(profile_version="bogus"), "invalid GC draft schema")
reject(lambda p, a: a.update(incident_id="wrong-incident"), "mismatched incident ID")
try:
    public_export(profile, adapter)
except AdapterError:
    print("PASS rejected missing Governance Record index")
else:
    raise AssertionError("Missing records must fail closed")
print("12/12 allowlist and rejection checks passed (structural only).")
