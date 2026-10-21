"""Fail-closed research gate for independently attributed OECD review evidence.

Checks evidence structure and consistency, not authenticity of reviewer identity
or correctness of the primary-source interpretation. Those require human review.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
read = lambda name: json.loads((ROOT / name).read_text(encoding="utf-8"))

def filled(value):
    return isinstance(value, str) and bool(value.strip()) and value.strip().lower() not in {
        "pending", "tbd", "none", "n/a", "review pending", "reviewer evidence pending"
    }

def evidence(item, keys):
    return isinstance(item, dict) and all(filled(item.get(k)) for k in keys)

def assess(primary, manifest):
    blockers = []
    rows = primary.get("criteria", [])
    if len(rows) != 29 or [r.get("criterion") for r in rows] != list(range(1, 30)):
        blockers.append("29-criterion coverage incomplete")
    source_evidence = manifest.get("source_review_evidence", [])
    if not isinstance(source_evidence, list):
        source_evidence = []
    source_by_id = {e.get("criterion"): e for e in source_evidence if isinstance(e, dict)}
    if (any(r.get("independent_human_review") != "accepted" for r in rows)
        or len(source_by_id) != 29
        or any(not evidence(source_by_id.get(n), (
            "reviewer", "review_date", "source_page", "source_label",
            "answer_format", "vocabulary_review", "cardinality_review",
            "conditional_review", "evidence_reference"
        )) for n in range(1, 30))
        or any(source_by_id.get(r.get("criterion"), {}).get("answer_format") != r.get("answer_format")
               or str(source_by_id.get(r.get("criterion"), {}).get("source_page")) != str(r.get("page"))
               for r in rows)):
        blockers.append("independent source review evidence incomplete or inconsistent")
    author = manifest.get("independent_author_evidence")
    if manifest.get("independent_author_review") != "accepted" or not evidence(
        author, ("author", "affiliation", "authored_at", "independence_statement", "evidence_reference")
    ):
        blockers.append("independent fixture authorship evidence missing")
    fixtures = manifest.get("fixtures", [])
    if not isinstance(fixtures, list):
        fixtures = []
    fixture_ids = [f.get("id") for f in fixtures if isinstance(f, dict)]
    if (not fixtures or len(fixture_ids) != len(fixtures) or len(set(fixture_ids)) != len(fixtures)
        or not all(isinstance(f, dict) and
                   evidence(f, ("id", "provenance", "criterion_oracle", "fixture_path", "execution_evidence"))
                   and f.get("expected_result") in ("accept", "reject")
                   and isinstance(f.get("criteria_covered"), list)
                   and all(isinstance(n, int) and 1 <= n <= 29 for n in f["criteria_covered"])
                   and f["criteria_covered"] for f in fixtures)):
        blockers.append("independent fixture provenance, oracle, execution or coverage incomplete")
    if {f.get("expected_result") for f in fixtures if isinstance(f, dict)} != {"accept", "reject"}:
        blockers.append("positive and negative fixture coverage incomplete")
    roundtrip = manifest.get("round_trip_evidence")
    if (manifest.get("round_trip_semantic_equivalence_verified") is not True
        or not evidence(roundtrip, (
            "reviewer", "review_date", "test_command", "test_results_reference",
            "mapped_fields", "unmapped_fields", "loss_accounting", "decision"
        ))):
        blockers.append("GC-native semantic equivalence evidence missing")
    approval = manifest.get("release_approval_evidence")
    if (manifest.get("human_release_approval") is not True
        or not evidence(approval, ("approver", "approval_date", "governance_record_reference", "scope"))):
        blockers.append("attributable human release approval missing")
    return {"eligible": not blockers, "blockers": blockers}

if __name__ == "__main__":
    result = assess(read("oecd-annex-b-primary-review.json"), read("independent-fixture-manifest.json"))
    assert not result["eligible"], "Research baseline must not be independently accepted"
    assert "independent source review evidence incomplete or inconsistent" in result["blockers"]
    assert "GC-native semantic equivalence evidence missing" in result["blockers"]
    print("PASS: independent review gate remains blocked:", "; ".join(result["blockers"]))
