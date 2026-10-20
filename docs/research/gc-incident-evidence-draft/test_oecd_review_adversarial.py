"""Adversarial integrity checks for OECD source-review evidence claims.

Independent of adapter fixtures: intentionally corrupt audit assertions and
ensure the review gate rejects each mutation.
"""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
read = lambda name: json.loads((ROOT / name).read_text(encoding="utf-8"))
mapping = read("oecd-criteria-map.json")
matrix = read("oecd-criterion-review-matrix.json")
source = read("oecd-source-audit.json")
acceptance = read("acceptance-status.json")
FIELDS = ("source_label_verified", "source_mandatory_verified",
          "source_vocabulary_verified", "source_cardinality_verified",
          "source_conditionals_verified")

def issues(candidate, audit, source_audit, status):
    errors = []
    rows = audit.get("criteria", [])
    baseline = candidate.get("criteria", [])
    if len(rows) != 29 or len(baseline) != 29:
        errors.append("criterion count")
    if [r.get("criterion") for r in rows] != list(range(1, 30)):
        errors.append("criterion identity/order")
    for index, row in enumerate(rows):
        if index >= len(baseline):
            break
        original = baseline[index]
        if any(row.get(k) != original.get(k2) for k, k2 in
               (("criterion", "criterion"), ("candidate_path", "candidate_path"),
                ("claimed_mandatory", "mandatory"))):
            errors.append(f"mapping drift {index + 1}")
        if any(type(row.get(flag)) is not bool for flag in FIELDS):
            errors.append(f"invalid verification flag {index + 1}")
        if any(row.get(flag) is True for flag in FIELDS):
            # A positive verification needs an actual primary-source locator,
            # not a candidate label or a self-authored schema reference.
            proof = row.get("primary_source_evidence")
            if not isinstance(proof, dict) or not all(
                isinstance(proof.get(k), str) and proof[k].strip()
                for k in ("document_doi", "page", "source_excerpt", "reviewer")
            ):
                errors.append(f"unsupported verification {index + 1}")
        if row.get("disposition") == "requires_primary_pdf_review" and any(
            row.get(flag) is True for flag in FIELDS
        ):
            errors.append(f"unreviewed criterion marked verified {index + 1}")
    if source_audit.get("interoperability_verified") is not False:
        errors.append("interoperability claim")
    if status.get("release_eligible") is not False:
        errors.append("release eligibility")
    if status.get("oecd_conformant") is not False:
        errors.append("conformance claim")
    return errors

assert not issues(mapping, matrix, source, acceptance)
cases = []
m = copy.deepcopy(matrix); m["criteria"].pop(); cases.append(("missing row", m, source, acceptance))
m = copy.deepcopy(matrix); m["criteria"][0]["criterion"] = 2; cases.append(("duplicate ID", m, source, acceptance))
m = copy.deepcopy(matrix); m["criteria"][0]["candidate_path"] = "fabricated"; cases.append(("mapping drift", m, source, acceptance))
m = copy.deepcopy(matrix); m["criteria"][0]["source_label_verified"] = True; cases.append(("unsupported verification", m, source, acceptance))
m = copy.deepcopy(matrix); m["criteria"][0]["source_cardinality_verified"] = "yes"; cases.append(("nonboolean claim", m, source, acceptance))
s = copy.deepcopy(source); s["interoperability_verified"] = True; cases.append(("false interoperability", matrix, s, acceptance))
a = copy.deepcopy(acceptance); a["oecd_conformant"] = True; cases.append(("false conformance", matrix, source, a))
a = copy.deepcopy(acceptance); a["release_eligible"] = True; cases.append(("false release", matrix, source, a))
for label, m, s, a in cases:
    assert issues(mapping, m, s, a), f"Failed to reject {label}"
    print("PASS rejected:", label)
print(f"PASS: baseline and {len(cases)} adversarial audit mutations")
