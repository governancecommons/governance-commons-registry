"""Research-only OECD optional inventory and privacy-boundary tests."""
import copy
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
schema = json.loads((ROOT / "schema.json").read_text(encoding="utf-8"))
full = json.loads((ROOT / "full.json").read_text(encoding="utf-8"))
invalid = json.loads((ROOT / "invalid-country.json").read_text(encoding="utf-8"))
mapping = json.loads((PARENT / "oecd-criteria-map.json").read_text(encoding="utf-8"))
mandatory = {1, 2, 3, 4, 7, 10, 11}
expected = {f"{r['criterion']:02d}" for r in mapping["criteria"] if not r["mandatory"]}
assert len(expected) == 22
assert {int(n) for n in expected}.isdisjoint(mandatory)
assert set(schema["properties"]) == expected == set(full)
assert schema.get("required", []) == []
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(schema, format_checker=FormatChecker())
assert validator.is_valid({})
assert validator.is_valid(full)
assert not validator.is_valid(invalid)
for field in expected:
    assert validator.is_valid({field: full[field]}), field
    broken = copy.deepcopy(full)
    broken[field] = None
    assert not validator.is_valid(broken), field
unknown = copy.deepcopy(full)
unknown["30"] = "unrecognized"
assert not validator.is_valid(unknown)
assert schema["properties"]["28"]["properties"]["sensitivity"]["enum"] == ["restricted", "confidential"]
print("PASS: all 22 optional criteria, empty and single-field valid, invalid/null/unknown rejected")
print("CAUTION: schema is structural research only; exact OECD classifications not validated.")
