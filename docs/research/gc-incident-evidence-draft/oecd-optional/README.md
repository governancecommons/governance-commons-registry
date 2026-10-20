# GC–INCIDENT.05: optional OECD research extension

The optional extension includes **22** keyed fields corresponding to OECD criteria #5, #6, #8, #9, #12–#29 (excluding mandatory #10 and #11). All are optional: `{}` is valid. It is independently validated, not inserted into the closed GC incident profile schema or GC Governance Record core.

The field numbers are zero-padded strings (for example `"06"` for countries). This is an **experimental structural data capture design**, not an exact OECD taxonomy, cardinality or conformance mapping. In particular, generic `categories` strings and `assessment` states are not verified OECD vocabularies. A separate source-level audit and fixtures are required before any criterion can be marked verified. The 29-row gap map is deliberately not reclassified.

Privacy: criterion #28 reproduction steps must be marked restricted/confidential; however, **all** optional extension fields are withheld from public export by default. `bundle.py` creates an internal bundle and a public allowlisted view through the existing mandatory adapter. It does not publish, encrypt, authorize access, scrub narratives, verify referenced links or validate reviewer authority. Do not use the internal bundle in a public endpoint.

Run `python docs/research/gc-incident-evidence-draft/oecd-optional/test_optional.py` and `python docs/research/gc-incident-evidence-draft/oecd-optional/test_bundle.py`.

Next acceptance work: verify OECD Annex B exact value sets and cardinalities, establish stable incident-ID binding between profile and adapters, add source-derived valid/invalid fixtures, validate reviewer authorization and disclosure, and document restricted storage/access and retention policy.
