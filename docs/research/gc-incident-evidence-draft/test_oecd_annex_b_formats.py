"""Annex B source-derived answer-format inventory regression tests (research only)."""
import json
from collections import Counter
from pathlib import Path
root=Path(__file__).resolve().parent
matrix=json.loads((root/"oecd-criterion-review-matrix.json").read_text())
rows=matrix["criteria"]
expected=["open_text","open_text","multi_selection_with_open_text","open_text_and_multi_selection","date","multi_selection","open_text_urls_upload","open_text","open_text","multi_selection","multi_selection","multi_selection","checkbox","multi_selection","checkbox","multi_selection","multi_selection","multi_selection","checkbox","single_choice","checkbox","checkbox","multi_selection","checkbox","multi_selection","single_choice","open_text_and_multi_selection","open_text","open_text"]
assert len(rows)==len(expected)==29
for n,(row,fmt) in enumerate(zip(rows,expected),1):
    assert row["criterion"]==n
    assert row["oecd_answer_format"]==fmt,(n,row["oecd_answer_format"])
    assert row["primary_source_evidence"]["page"]==("23" if n<=12 else "24")
    assert row["source_mandatory_verified"] is True
    assert row["source_label_verified"] is False
    assert row["source_vocabulary_verified"] is False
    assert row["source_cardinality_verified"] is False
    assert row["source_conditionals_verified"] is False
assert {r["criterion"] for r in rows if r["claimed_mandatory"]}=={1,2,3,4,7,10,11}
assert Counter(r["oecd_dimension"] for r in rows)=={"incident_metadata":9,"harm_details":4,"people_and_planet":3,"economic_context":4,"data_and_input":1,"ai_model":3,"task_and_output":2,"other_information":3}
print("PASS: 29 Annex B format/dimension/mandatory records; unverified semantics remain blocked")
