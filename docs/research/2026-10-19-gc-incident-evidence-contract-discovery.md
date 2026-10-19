# GC Incident Evidence — contract discovery

Date: 2026-10-19
Status: non-normative implementation reconnaissance; not a published profile
Predecessor: [GC–OECD.01](2026-10-19-gc-oecd-01-incident-criteria-gap-matrix.md)

## Directly inspected Registry main sources

- [Governance Record schema](https://github.com/governancecommons/governance-commons-registry/blob/main/governance_commons/schemas/governance-record.schema.json), blob SHA `5ca1346e1cc13753db1fac62b4e83f39b264199c`.
- [Validator](https://github.com/governancecommons/governance-commons-registry/blob/main/governance_commons/governance_records.py), blob SHA `e96b82c15aa8cc1e882ea61249877ac5dac5e7fe`.
- [Existing tests](https://github.com/governancecommons/governance-commons-registry/blob/main/tests/test_governance_records.py), blob SHA `9ed8a6989e2586027e236e9398f56b6b2d90f413`.
- [ATP audit binding](https://github.com/governancecommons/governance-commons-registry/blob/main/governance_commons/interoperability.py), blob SHA `18db39509aaf759f15d936645f0f4bd4661758f8`.
- [CLI](https://github.com/governancecommons/governance-commons-registry/blob/main/governance_commons/cli.py), blob SHA `4e832a28df058f4820344ab526983b428d45f829`.
- [Package exports](https://github.com/governancecommons/governance-commons-registry/blob/main/governance_commons/__init__.py), blob SHA `d3cf3eef1fe422a732fc9f9d59212011a6c1a60d`.

## Existing evidence primitives — confirmed from source

| Requirement | Existing primitive | Limit |
|---|---|---|
| Stable record identity and type | `record_id`, `record_type`, `schema_version=1.0.0` | No `incident` record_type in current enum; do not extend it without governance |
| Subject/actor references | `subject`, `actor` typed references | No reporter/developer/deployer/affected party roles |
| Temporal evidence | `timestamps.created_at/occurred_at/authorized_at/completed_at` | General timestamp strings; not incident discovery, report submission or notification deadlines |
| Evidence links | `relations[].type/target`, `provenance.source/method` | Generic relations; no incident relation vocabulary or attachment handling validation |
| Authority and approval | `authority`, `approval`; `GR-AUTH-001` | Approval of governed action, not independent incident-report approval |
| Revocation | `record_type=revocation`, `GR-AUTH-002/003` | Source validates time and authority identity for specific cases, not full incident containment lifecycle |
| Handoff | `handoff`, `GR-HANDOFF-001` | Governed agent handoff, not transfer of incident-response responsibility |
| Status/context | `lifecycle`, `framework_context`, `governance_context`, `extensions` | Extensible but not a validated incident profile |
| Cross-component audit | `bind_atp_audit_trail` creates provenance records from ATP entries, preserving hash, sequence, participants | Mapping preserves claimed hashes; it does **not** verify the hash chain cryptographically |

The validator uses JSON Schema Draft 2020-12 and then runs semantic rules `GR-AUTH-001`, `GR-AUTH-002`, `GR-AUTH-003`, `GR-HANDOFF-001` on structurally valid data. `gc-validate --spec governance-record` exposes the existing validation surface. The existing test module covers positive/negative fixtures, revoked authority and timing, handoff requirements and ConformanceReport serialization. **Tests were read, not executed.**

## Minimal additive profile boundary — proposed, not implemented

An independently versioned **incident evidence profile** should reference, not redefine, Governance Records. Candidate report envelope: `incident_id`, `profile_version`, `reporter` (with explicit role), `affected_systems` (with developer/deployer roles), `event_timeline`, `incident_description`, `harm_and_severity`, `response_actions`, `evidence_refs`, `review`, `disclosure`, and `oecd_mapping`. All fields and names are **illustrative design candidates**, not registered GC fields.

Candidate typed relationships: `incident_has_governance_record`, `incident_has_evidence`, `incident_affects_system`, `response_authorized_by`, `response_reviewed_by`. Do not infer a causal link or truth of a harm claim merely from an audit link.

The OECD 29 criteria (seven mandatory) must be mapped individually with exact source semantics, absence/unknown rules, confidentiality rules and export behavior. Existing Governance Record evidence can support a report but does not itself establish OECD compliance.

## Implementation and governance cautions

1. `record_type` is a closed enum; a new `incident` value would be a core schema change. Prefer a separate profile document with links to existing records.
2. The Governance Record schema permits additional properties; that is **not** equivalent to profile-level validation. Do not place arbitrary fields in `extensions` and call them conformant incident reports.
3. Existing timestamp fields are strings; semantic validation does not comprehensively check all temporal ordering or all incident lifecycle transitions.
4. The existing approval rule checks active authority and a supplied required approval, but does not prove the correctness of an external approval authority or independent reviewer.
5. The ATP audit binder preserves hash evidence but does not verify signatures, hashes or chain integrity.
6. Maintain the Python/npm feature distinction and independently versioned GC component contracts.

## Validation and next acceptance step

**Completed:** source discovery and field-by-field review of schema, validator, tests, CLI and interoperability binding. The references above are pinned to fetched blob SHAs. No normative file modified.

**Not completed:** checkout-based test execution, OECD profile schema, valid/invalid incident fixtures, privacy/redaction review, independent conformance proof or profile adoption.

**Next:** draft a separate, non-normative profile schema and representative positive/negative fixtures; run Draft 2020-12 validation and test relationship semantics before proposing a governed implementation. No change to the Governance Record schema is required for that experiment.
