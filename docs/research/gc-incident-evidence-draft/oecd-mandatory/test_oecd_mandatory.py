"""Research-only OECD mandatory-field fixture test."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

root = Path(__file__).resolve().parent
schema = json.loads((root / "oecd-mandatory.schema.json").read_text(encoding="utf-8"))
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(schema, format_checker=FormatChecker())
files = sorted(root.glob("oecd-mandatory-*.json"))
files = [f for f in files if f.name != "oecd-mandatory.schema.json"]
assert len(files) == 8
for path in files:
    errors = list(validator.iter_errors(json.loads(path.read_text(encoding="utf-8"))))
    expected_valid = path.name == "oecd-mandatory-valid.json"
    assert (not errors) == expected_valid, f"{path.name}: {[e.message for e in errors]}"
    print("PASS", path.name)
print("8/8 fixture expectations met; research only, not OECD conformance.")
