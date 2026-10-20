"""Fail closed on experimental incident profile release assertions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
status = json.loads((ROOT / "acceptance-status.json").read_text(encoding="utf-8"))
mapping = json.loads((ROOT / "oecd-criteria-map.json").read_text(encoding="utf-8"))
optional = json.loads((ROOT / "oecd-optional/schema.json").read_text(encoding="utf-8"))
mandatory = json.loads((ROOT / "oecd-mandatory/oecd-mandatory.schema.json").read_text(encoding="utf-8"))
assert status["version"] == "0.1.0"
assert status["decision"] == "research_baseline_only"
assert status["normative"] is False
assert status["oecd_conformant"] is False
assert status["automatic_publication_permitted"] is False
assert status["release_eligible"] is False
assert status["criteria"] == {"total": 29, "mandatory": 7, "optional": 22}
assert len(mapping["criteria"]) == 29
assert sum(bool(row["mandatory"]) for row in mapping["criteria"]) == 7
assert len(optional["properties"]) == 22
assert "incident_id" in mandatory["required"]
assert all(value in {"implemented", "implemented_noncryptographic", "implemented_partial_semantics", "open"} for value in status["gates"].values())
assert any(value == "open" for value in status["gates"].values())
print("PASS: research-only acceptance; promotion and publication remain blocked")
