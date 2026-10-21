"""Cross-check primary-source Annex B inventory against repository mapping."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
read=lambda n:json.loads((ROOT/n).read_text(encoding="utf-8"))
primary=read("oecd-annex-b-primary-review.json")
mapping=read("oecd-criteria-map.json")
matrix=read("oecd-criterion-review-matrix.json")
rows=primary["criteria"]
assert len(rows)==29
assert [r["criterion"] for r in rows]==list(range(1,30))
assert sum(r["mandatory"] for r in rows)==7
assert len(matrix["criteria"])==29
for i,row in enumerate(rows):
    assert row["mandatory"] is mapping["criteria"][i]["mandatory"]
    assert row["mandatory"] is matrix["criteria"][i]["claimed_mandatory"]
    assert row["answer_format"]==matrix["criteria"][i]["oecd_answer_format"], (i+1,row["answer_format"],matrix["criteria"][i]["oecd_answer_format"])
    assert row["dimension"]==matrix["criteria"][i]["oecd_dimension"], i+1
    assert row["independent_human_review"]=="pending"
assert {r["criterion"] for r in rows if r["mandatory"]}=={1,2,3,4,7,10,11}
assert primary["doi"]=="10.1787/f326d4ac-en"
print("PASS: primary OECD Annex B structural inventory cross-checked; independent review pending")
