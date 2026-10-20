"""Ensure sensitive optional fields never appear in public export."""
import json
from pathlib import Path
import runpy
import sys
from bundle import private_bundle, public_bundle

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
records = runpy.run_path(str(ROOT.parent / "test_cross_record.py"))["records"]
PARENT = ROOT.parent
profile = json.loads((PARENT / "fixtures/valid-minimal.json").read_text())
mandatory = json.loads((PARENT / "oecd-mandatory/oecd-mandatory-valid.json").read_text())
optional = json.loads((ROOT / "full.json").read_text())
profile["description"] = mandatory["description"]
profile["review"] = {
    "status": "approved",
    "reviewer": {"type": "human", "id": "alice"},
    "governance_record": {"type": "governance-record", "id": "gr-approval"},
}
profile["disclosure"] = {"classification": "public", "publication_status": "approved_for_release"}
profile["evidence_refs"][0]["sensitivity"] = "public"
mandatory["supporting_materials"][0]["sensitivity"] = "public"
optional["28"]["instructions"] = "SECRET_TEST_REPRODUCTION_STEPS"
optional["29"] = "SECRET_TEST_EXTRA_NOTES"
internal = private_bundle(mandatory, optional)
assert "SECRET_TEST_REPRODUCTION_STEPS" in json.dumps(internal)
exported = public_bundle(profile, mandatory, optional, records)
assert "SECRET_TEST_REPRODUCTION_STEPS" not in json.dumps(exported)
assert "SECRET_TEST_EXTRA_NOTES" not in json.dumps(exported)
assert "optional" not in exported
print("PASS: optional restricted reproduction and additional notes excluded from public export")
