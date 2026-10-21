"""Private interchange invariants: lossless research adapter, no implicit publication."""
import copy
import json
from internal_interchange import capture, restore, InterchangeError
from export_adapter import load

source = load("oecd-mandatory-valid.json")
def denied(fn):
    try:
        fn()
    except InterchangeError:
        return
    raise AssertionError("Expected private interchange refusal")

denied(lambda: capture(source))
envelope = capture(source, authorized=True)
assert envelope["classification"] == "restricted"
assert envelope["publication_permitted"] is False
assert envelope["payload"]["submitter"]["email"] == source["submitter"]["email"]
assert envelope["payload"]["supporting_materials"][0]["sensitivity"] == "restricted"
denied(lambda: restore(envelope))
restored = restore(json.loads(json.dumps(envelope)), authorized=True)
assert restored == source, "Private round trip must preserve all adapter fields"
restored["title"] = "mutated"
assert source["title"] != restored["title"]
assert envelope["payload"]["title"] != restored["title"]
source["title"] = "mutated source"
assert envelope["payload"]["title"] != source["title"]
for field, value in [
    ("classification", "public"),
    ("publication_permitted", True),
    ("source_semantics", "verified_oecd_conformance"),
    ("format", "unknown"),
]:
    bad = copy.deepcopy(envelope)
    bad[field] = value
    denied(lambda b=bad: restore(b, authorized=True))
bad = copy.deepcopy(envelope)
bad["payload"]["severity"]["categories"] = ["unrecognized"]
denied(lambda: restore(bad, authorized=True))
bad = copy.deepcopy(envelope)
bad["extra"] = "unexpected"
denied(lambda: restore(bad, authorized=True))
bad = copy.deepcopy(envelope)
bad.pop("payload")
denied(lambda: restore(bad, authorized=True))
print("PASS: private research adapter interchange preserves all fields and refuses unsafe envelopes")
print("NOT OECD-to-GC-to-OECD interoperability; caller must implement real access control")
