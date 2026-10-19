# GC Incident Evidence draft — validation and next acceptance gate

Date: 2026-10-19
Status: non-normative experimental profile, not adopted or released

## Artifacts

- [Draft schema](schema.json)
- [Valid minimal fixture](fixtures/valid-minimal.json)
- [Invalid reporter role](fixtures/invalid-reporter-role.json)
- [Invalid review approval](fixtures/invalid-review-approval.json)
- [Invalid severity assessment](fixtures/invalid-severity-assessment.json)

## Checks performed

All five JSON files were fetched back from GitHub main and parsed. A targeted independent structural checker evaluated required fields, object/array/string types, additionalProperties, minimum string/array sizes, constants, enums, local $ref and the three conditional required-field cases. This checker is **not** a full JSON Schema Draft 2020-12 implementation.

| Fixture | Expected | Observed | Details |
|---|---|---|---|
| valid-minimal | pass | pass | no detected structural violations |
| invalid-reporter-role | fail | fail | reporter.role required |
| invalid-review-approval | fail | fail | approved review requires reviewer and governance_record |
| invalid-severity-assessment | fail | fail | assessed severity requires classification and rationale |

**Result: 4/4 expected outcomes under the targeted checker.**

## Not validated

- Full Draft 2020-12 meta-schema and reference implementation conformance; format:date-time enforcement.
- Cross-document resolution: referenced Governance Records may not exist, may be revoked, or may not authorize the stated action.
- Temporal ordering, causal assertions, source authenticity, hash-chain verification, confidentiality/redaction and release authorization.
- OECD 29-criterion reporting completeness and all seven mandatory OECD criteria.
- Existing Registry pytest/CI and Python/npm SDK integration.

## Next task — validation gate and profile semantics

1. Add an executable Draft 2020-12 test harness in an isolated research directory, exercising all fixtures with format checking.
2. Add negative fixtures for invalid dates, wrong reference types, unapproved disclosure, inconsistent response/evidence links and invalid timeline ordering.
3. Design and test cross-document link resolution against real Governance Record fixtures. Do not equate the existence of a link with verification of incident causality.
4. Produce an explicit mapping for each OECD criterion, preserving mandatory/optional markers and evidence provenance.
5. Submit a governance review before proposing any normative profile or SDK integration.

No core schema, validator, architecture, version, release or registered standard changed.
