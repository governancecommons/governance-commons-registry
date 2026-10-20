"""Ensure every OECD candidate criterion has an explicit, non-inflated review record."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
read = lambda p: json.loads((ROOT / p).read_text(encoding="utf-8"))
matrix = read("oecd-criterion-review-matrix.json")
mapping = read("oecd-criteria-map.json")
rows = matrix["criteria"]
assert len(rows) == 29
assert [r["criterion"] for r in rows] == list(range(1, 30))
for row, candidate in zip(rows, mapping["criteria"]):
    assert row["criterion"] == candidate["criterion"]
    assert row["candidate_path"] == candidate["candidate_path"]
    assert row["claimed_mandatory"] == candidate["mandatory"]
    for flag in ("source_label_verified", "source_mandatory_verified", "source_vocabulary_verified", "source_cardinality_verified", "source_conditionals_verified"):
        assert isinstance(row[flag], bool)
    if row["disposition"] == "requires_primary_pdf_review":
        assert not any(row[flag] for flag in ("source_label_verified", "source_mandatory_verified", "source_vocabulary_verified", "source_cardinality_verified", "source_conditionals_verified"))
print("PASS: 29 criteria have explicit OECD review status without unsupported verification claims")
