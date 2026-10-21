"""Fail-closed research gate for independent OECD review evidence."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
read = lambda name: json.loads((ROOT / name).read_text(encoding="utf-8"))

def assess(primary, manifest):
    rows = primary["criteria"]
    blockers = []
    if len(rows) != 29 or [r["criterion"] for r in rows] != list(range(1, 30)):
        blockers.append("29-criterion coverage incomplete")
    if any(r.get("independent_human_review") != "accepted" for r in rows):
        blockers.append("independent source review incomplete")
    if manifest.get("independent_author_review") != "accepted":
        blockers.append("independent fixture authorship not confirmed")
    fixtures = manifest.get("fixtures", [])
    if not fixtures or not all(
        isinstance(f, dict) and
        all(f.get(k) for k in ("id", "provenance", "expected_result", "criterion_oracle"))
        and f["expected_result"] in ("accept", "reject")
        for f in fixtures
    ):
        blockers.append("independently attributed positive/negative fixtures missing")
    if not {f["expected_result"] for f in fixtures if isinstance(f, dict)} >= {"accept", "reject"}:
        blockers.append("positive and negative fixture coverage incomplete")
    if not manifest.get("round_trip_semantic_equivalence_verified", False):
        blockers.append("GC-native semantic equivalence unverified")
    if not manifest.get("human_release_approval", False):
        blockers.append("human release approval missing")
    return {"eligible": not blockers, "blockers": blockers}

if __name__ == "__main__":
    result = assess(read("oecd-annex-b-primary-review.json"), read("independent-fixture-manifest.json"))
    assert not result["eligible"], "Research baseline must not be independently accepted"
    assert "independent source review incomplete" in result["blockers"]
    assert "GC-native semantic equivalence unverified" in result["blockers"]
    print("PASS: independent review gate correctly remains blocked:", "; ".join(result["blockers"]))
