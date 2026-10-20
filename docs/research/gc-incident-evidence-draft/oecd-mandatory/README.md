# OECD incident adapter — experimental research boundary

This optional adapter is not a registered Governance Commons specification, an OECD-certified implementation, or evidence of regulatory compliance. It does not alter GC core or the SDK.

## Implemented and tested

- Seven mandatory reporting fields in `oecd-mandatory.schema.json`, including explicit incident-ID binding.
- Separate 22-field optional extension under `../oecd-optional/`. All optional fields may be absent.
- Structural JSON Schema validation and adversarial fixture tests.
- Incident-ID, title, description, and reporter-role agreement between profile and adapter.
- Public export rejects nonpublic evidence classifications, missing approval declarations, missing or contradictory referenced Governance Records, and invalid schema inputs.
- The public allowlist excludes submitter email, review identities, internal Governance Records, response actions, and all optional fields, including reproduction steps.

## Non-negotiable limitations

**No automatic publication.** The public-export function is a serialization guard only. It does not prove that the reporter consented, the reviewer had genuine authority, the underlying records are authentic, the content is accurate, the URLs are safe, or narrative text has been redacted. A syntactically public URL may still expose private data or unsafe content. This function is not an anonymizer.

`cross_record_issues` performs selected structural and semantic checks; it is **not** the complete canonical GC validator and cannot establish provenance or cryptographic authenticity. Human review and an independently authorized publication process are required.

The field categories and cardinalities are **experimental interpretations**. They have not been independently reconciled against every OECD source-level taxonomy and example. The research mapping must retain its non-conformant status until source-based interoperability fixtures and a documented independent review demonstrate otherwise.

## GC–INCIDENT.06 acceptance decision

**Structural research baseline: accepted, conditional on green CI for the current commit.**
**OECD interoperability conformance: not accepted.**
**Automatic public release: not accepted.**
**Promotion to a normative GC specification: deferred.**

Remaining gates before promotion:
1. Source-audit all 29 OECD criteria, enumerations, cardinalities, and conditional explanations against the OECD primary report and any published annex.
2. Verify review authority and provenance using the canonical GC validator plus authenticated identity and immutable evidence.
3. Implement and test human-approved narrative redaction, URL allowlisting/dereferencing policy, consent, and restricted data retention/access controls.
4. Run independent third-party interoperability fixtures, including adversarial identity, authorization, disclosure, and privacy cases.
5. Obtain explicit maintainer acceptance and independently versioned release approval.

## Commands

```sh
python docs/research/gc-incident-evidence-draft/oecd-mandatory/test_oecd_mandatory.py
python docs/research/gc-incident-evidence-draft/oecd-mandatory/test_export_adapter.py
python docs/research/gc-incident-evidence-draft/oecd-optional/test_optional.py
python docs/research/gc-incident-evidence-draft/oecd-optional/test_bundle.py
```
