# GC–INCIDENT.09 — Claude pre-independent-review scan package

**Status:** Prepared for external Claude review; **not submitted to Claude**, and no Claude findings have been received. This is a research-only adversarial scan, not OECD endorsement, certification, or independent human verification.

## Scope and primary source

- OECD (2025), *Towards a common reporting framework for AI incidents*, DOI: https://doi.org/10.1787/f326d4ac-en
- Primary PDF: https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/02/towards-a-common-reporting-framework-for-ai-incidents_8c488fdb/f326d4ac-en.pdf
- Inspect Annex B Table B.1 directly; do not accept GC's existing inventory as authoritative.
- Repository: https://github.com/governancecommons/governance-commons-registry
- Review branch/PR: `gc-incident-09-independent-verification`, https://github.com/governancecommons/governance-commons-registry/pull/12
- Independent human verification tracking: https://github.com/governancecommons/governance-commons-registry/issues/11

## Files to supply Claude (read-only)

1. `docs/research/gc-incident-evidence-draft/oecd-annex-b-primary-review.json`
2. `docs/research/gc-incident-evidence-draft/oecd-criteria-map.json`
3. `docs/research/gc-incident-evidence-draft/oecd-criterion-review-matrix.json`
4. `docs/research/gc-incident-evidence-draft/independent-fixture-manifest.json`
5. `docs/research/gc-incident-evidence-draft/oecd-mandatory/classification-gap-register.md`
6. `docs/research/gc-incident-evidence-draft/oecd-mandatory/semantic_bridge.py`
7. `docs/research/gc-incident-evidence-draft/oecd-mandatory/internal_interchange.py`
8. `docs/research/gc-incident-evidence-draft/oecd-mandatory/round_trip_probe.py`
9. `docs/research/gc-incident-evidence-draft/gc-incident-09-acceptance.py`
10. `docs/research/gc-incident-evidence-draft/test_gc_incident_09_acceptance.py`
11. `docs/research/gc-incident-evidence-draft/GC-INCIDENT-08-review-handoff.md`
12. `docs/research/gc-incident-evidence-draft/gc-incident-09-reviewer-evidence-guide.md`

Include relevant schema, fixture, test, and workflow files referenced by the above. Avoid sharing private incident records, personal data, credentials, or unredacted restricted evidence.

## Prompt to run in Claude

You are an adversarial external AI reviewer of Governance Commons' *research-only* OECD AI incident reporting adapter. Do not assume existing code, mapping tables, tests, or prior review claims are correct. Read the OECD primary source, especially Annex B Table B.1, and compare each of its 29 criteria against the provided repository artifacts.

Tasks:
1. Independently enumerate criteria 1–29: mandatory status, source label, input format, controlled vocabulary, cardinality, and conditional applicability. Distinguish direct source evidence from interpretation. Flag every unsupported assertion and cite OECD page/table/criterion.
2. Inspect criteria 3, 10 and 11 for false equivalence between OECD relationship, severity, harm type and GC status fields. Propose safe, explicit loss accounting.
3. Trace all data flows through private interchange, GC projection, recovery, and public export. Identify any privacy leakage, unauthorized publication, forged authorization, or semantic reconstruction claim.
4. Audit the acceptance gate adversarially. In particular, determine whether fabricated reviewer names, fabricated evidence references, nonexistent fixture paths, nonexecuted tests, or self-review can satisfy it. Recommend verifiable evidence checks without pretending software can prove reviewer independence.
5. Suggest negative and boundary tests, distinguishing AI-suggested cases from independently human-authored fixtures. Do not mark your suggestions as independent fixtures.
6. Find misleading documentation, release-facing claims, stale version or commit references, and missing CI coverage.

Output a **finding register** with IDs, severity (critical/high/medium/low), affected file and line/field, OECD citation when relevant, reproduction or verification steps, expected vs actual behavior, confidence, and recommended fix. Explicitly list what you could not access or verify. Finish with `research readiness` and `interoperability claim readiness` as **separate** decisions. Do not issue certification, release authorization, or human-review approval.

## Preservation and triage

Save the complete unedited Claude response with model/version, run date, exact inputs or commit SHA, and access limitations. Create a separate triage record for each finding: confirmed, rejected with evidence, or unresolved. Give the independent reviewer the original Claude output and triage, but require independent verification of every claim.

## Mandatory guardrails

Current flags: `normative=false`, `interoperability_verified=false`, `release_eligible=false`. The `authorized=True` API parameter is not access control. Private-envelope source recovery is not GC-native semantic equivalence. A green CI run cannot prove independence or OECD interoperability.
