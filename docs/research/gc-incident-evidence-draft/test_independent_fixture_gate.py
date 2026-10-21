"""Research-only fixture oracle checks; adversarial mutations must fail closed."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "independent-fixture-manifest.json").read_text(encoding="utf-8"))
REQUIRED = {"id", "provenance", "expected_result", "criterion_oracle"}
BLOCKERS = {"independent_source_label_review", "independent_fixture_authorship",
            "round_trip_semantic_equivalence", "human_release_approval"}

def issues(m):
    errors = []
    if m.get("phase") != "GC-INCIDENT.08" or m.get("source_doi") != "10.1787/f326d4ac-en":
        errors.append("source identity")
    if any(m.get(k) is not False for k in ("normative", "interoperability_verified", "release_eligible")):
        errors.append("unsupported release or interoperability claim")
    if m.get("independent_author_review") != "pending" or m.get("status") != "design_baseline":
        errors.append("unreviewed status promotion")
    if set(m.get("blocking_gates", [])) != BLOCKERS or len(m.get("blocking_gates", [])) != len(BLOCKERS):
        errors.append("missing blocker")
    contract = m.get("fixture_contract", {})
    if set(contract.get("required", [])) != REQUIRED or set(contract.get("expected_result_values", [])) != {"accept", "reject"}:
        errors.append("fixture contract")
    if contract.get("criterion_oracle_status") != "pending_independent_source_verification":
        errors.append("unsupported source oracle")
    fixtures = m.get("fixtures")
    if not isinstance(fixtures, list):
        errors.append("fixture list")
    elif fixtures:
        errors.append("unreviewed fixtures cannot be accepted as independent")
    return errors

assert not issues(manifest), issues(manifest)
mutations = [
    ("false interoperability", "interoperability_verified", True),
    ("false release", "release_eligible", True),
    ("false normative", "normative", True),
    ("false independent review", "independent_author_review", "complete"),
    ("premature readiness", "status", "verified"),
    ("unreviewed fixture", "fixtures", [{"id": "fabricated"}]),
    ("missing blockers", "blocking_gates", ["human_release_approval"]),
]
for label, key, value in mutations:
    candidate = copy.deepcopy(manifest)
    candidate[key] = value
    assert issues(candidate), "Failed to reject " + label
    print("PASS rejected:", label)
print(f"PASS: baseline and {len(mutations)} adversarial research claims")
