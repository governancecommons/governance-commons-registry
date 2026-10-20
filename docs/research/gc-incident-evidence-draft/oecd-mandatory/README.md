# OECD incident adapter — research boundary

This is an **experimental**, optional, separately stored OECD mandatory-field adapter, not a registered GC specification or OECD conformance claim. It does not alter Governance Record or GC SDK APIs.

## Validation and export

- `test_oecd_mandatory.py`: structural acceptance/rejection fixtures for the seven mandatory fields.
- `test_export_adapter.py`: checks schema validity, title/description/reporter consistency, release/review flags, evidence sensitivity, and a narrow public output allowlist.
- `export_adapter.py`: deliberately does not include reporter email, affiliation, reviewer identity, internal response actions or unrestricted Governance Record links in its public output.

**Security limitation:** A public flag is a declaration, not proof of authorization. This adapter does not independently verify review Governance Records, reporter consent, the sensitivity of content *inside* narratives, malicious links, URL destination safety, referenced evidence contents, identity authenticity, or redaction adequacy. It must not be wired directly to public publishing without separate human review and access controls. Public supporting URLs may disclose information via their targets. The adapter is not an anonymizer.

**Data integrity limitation:** The two documents are linked by title, description and reporter role for this research demonstration, not a durable cryptographic or incident-ID binding. A future version must introduce explicit identity linkage, stronger consistency checks, and governance-record authorization verification.

## Deferred work

The remaining 22 optional OECD criteria, exact source vocabulary/cardinality review, OECD source-based acceptance fixtures, restricted/private export, and production disclosure policy are not implemented. Keep the original `oecd-criteria-map.json` classifications unchanged until verified with evidence.

## GC–INCIDENT.06 hardening (experimental)

The mandatory adapter now requires `incident_id` and rejects a mismatch with the GC incident profile. Public export requires a supplied Governance Record index and runs `cross_record_issues` against referenced response, review and evidence records; a missing or contradictory approval record fails closed. The optional bundle passes this index through to the same guard.

**Important:** These are in-repository structural and semantic checks, not cryptographic proof, verified human authority, safe-publication approval, or OECD taxonomy conformance. `cross_record_issues` mirrors selected core rules rather than invoking the complete canonical semantic validator. The public export still contains incident narrative and supporting URLs; human content review and link-safety checks remain required. This output must not be automatically published.

The source-derived audit of OECD enumerations and cardinalities, immutable cross-document identity, consent, reviewer independence, external fixtures, and retention/access controls remain open acceptance blockers.
