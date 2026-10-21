"""Research-only loss analysis for OECD-oriented adapter to public GC view.

This is deliberately not a reversible OECD-to-GC-to-OECD converter.
"""
import copy

RETAINED = ("incident_id", "title", "description", "system_relationships", "severity", "harm_types")
DROPPED = ("submitter",)
TRANSFORMED = ("supporting_materials",)

def analyze(adapter, public_view):
    """Return structural loss findings; reject unsupported round-trip claims."""
    findings = []
    for key in RETAINED:
        if public_view.get(key) != adapter.get(key):
            findings.append({"field": key, "kind": "changed_or_missing"})
    for key in DROPPED:
        if key in public_view:
            findings.append({"field": key, "kind": "privacy_boundary_breached"})
        else:
            findings.append({"field": key, "kind": "intentionally_omitted"})
    expected_materials = [
        {"kind": item["kind"], "reference": item["reference"]}
        for item in adapter["supporting_materials"]
    ]
    if public_view.get("supporting_materials") != expected_materials:
        findings.append({"field": "supporting_materials", "kind": "unexpected_transformation"})
    else:
        findings.append({"field": "supporting_materials.sensitivity", "kind": "intentionally_omitted"})
    return findings

def reconstruct(adapter, public_view):
    """Fail closed: cannot recreate the original OECD-oriented submission."""
    raise ValueError("Lossy public view cannot reconstruct submitter and sensitivity")
