"""Synthetic adapter boundary tests; not independent OECD certification."""
import copy
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

root = Path(__file__).resolve().parent
schema = json.loads((root / "oecd-mandatory/oecd-mandatory.schema.json").read_text())
validator = Draft202012Validator(schema, format_checker=FormatChecker())
base = json.loads((root / "oecd-mandatory/oecd-mandatory-valid.json").read_text())
base["title"] = "Synthetic irrigation controller incident"
base["description"] = "A simulated controller opened a valve during maintenance."
base["incident_id"] = "synthetic-irrigation-001"
base["system_relationships"][0]["explanation"] = "Potential control contribution."
base["supporting_materials"][0]["reference"] = "https://example.org/synthetic-log"

def valid(document):
    return not list(validator.iter_errors(document))

assert valid(base)
cases = [
    ("missing relationship", lambda d: d.pop("system_relationships"), False),
    ("missing materials", lambda d: d.update(supporting_materials=[]), False),
    ("unknown relationship", lambda d: d["system_relationships"][0].update(category="unknown"), False),
    ("invalid email", lambda d: d["submitter"].update(email="invalid"), False),
    ("duplicate severity", lambda d: d["severity"].update(categories=["hazard", "hazard"]), False),
    ("other without explanation", lambda d: d["harm_types"].update(categories=["other"]), False),
    ("other with explanation", lambda d: d["harm_types"].update(categories=["other"], other_explanation="Synthetic impact"), True),
    ("multiple harm types", lambda d: d["harm_types"].update(categories=["physical", "economic_property"]), True),
]
for name, mutation, expected in cases:
    candidate = copy.deepcopy(base)
    mutation(candidate)
    assert valid(candidate) is expected, name
    print("PASS", name)
print("PASS synthetic adapter validation only; independent OECD verification remains pending")
