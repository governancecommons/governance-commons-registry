"""Verify OECD criteria inventory, mandatory markers and honest draft mapping."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
mapping = json.loads((ROOT / "oecd-criteria-map.json").read_text(encoding="utf-8"))
schema = json.loads((ROOT / "schema.json").read_text(encoding="utf-8"))
rows = mapping["criteria"]
mandatory = {1, 2, 3, 4, 7, 10, 11}
assert len(rows) == 29
assert [r["criterion"] for r in rows] == list(range(1, 30))
assert {r["criterion"] for r in rows if r["mandatory"]} == mandatory
assert mapping["status"] == "research_only_not_conformant"
assert all(r["status"] in {"partial", "gap"} for r in rows)
assert not any(r["status"] == "verified" for r in rows)
assert sum(r["status"] == "partial" for r in rows) == 13
assert sum(r["status"] == "gap" for r in rows) == 16
assert all(r["limitation"] for r in rows)
assert all(r["candidate_path"] is None for r in rows if r["status"] == "gap")
assert all(r["candidate_path"] for r in rows if r["status"] == "partial")
assert schema["properties"]["profile_version"]["const"] == mapping["profile_version"]
assert mapping["source"]["doi"] == "10.1787/f326d4ac-en"
print("PASS: 29 unique ordered criteria, seven mandatory flags, 13 partial, 16 gaps, zero verified.")
print("Mapping inventory only: OECD vocabulary, cardinality, privacy and semantic conformance remain unverified.")
