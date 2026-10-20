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
