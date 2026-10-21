# GC–INCIDENT.08 — Research merge and independent review handoff

Status: engineering CI passing as of commit 62a1abfeea07f1bf9df5ba93e01eb4366be927b9. This is a **research-only** implementation, not independently verified OECD interoperability.

## Merge scope (engineering)

PR #10 contains an OECD Annex B source inventory, schema tests, synthetic adapter cases, a restricted private interchange envelope, a conservative GC projection, private-source recovery, loss accounting, and fail-closed adversarial tests.

A maintainer may merge the research implementation **without** making any interoperability or conformance claim, provided current CI passes and no unreviewed release-facing claims or production publication paths are introduced. Merging does not alter the independent verification flags.

## Independent review instructions

Source: OECD, *Towards a common reporting framework for AI incidents*, DOI 10.1787/f326d4ac-en, Annex B Table B.1 (29 criteria).

Reviewer should independently:
1. Check all 29 criteria for source label, mandatory marker, answer format, vocabulary, cardinality, and conditional rules; record page and discrepancies.
2. Independently author positive and negative fixtures without copying repository adapter examples or expected outputs.
3. Test criteria 3 (system relationship), 10 (severity), and 11 (harm type) against the classification gap register. Reject unproven GC/OECD category equivalence.
4. Check private information and sensitive supporting materials are not included in the public export.
5. Distinguish private-source recovery from GC-native semantic round-trip; document lost or unmapped meaning.
6. Record reviewer identity, date, reviewed source version, test evidence, discrepancies, and explicit decision.

## Acceptance record template

- Reviewer:
- Affiliation/independence from fixture author:
- Review date:
- Primary source and pages checked:
- Criteria reviewed (1–29):
- Independent fixture identifiers and provenance:
- Tests run and evidence links:
- Mapping discrepancies and unresolved items:
- Public/private data boundary findings:
- Decision: accepted / changes required / rejected
- Human GC maintainer release authorization: pending

## Boundaries

- Do not represent OECD as endorsing, certifying, or formally approving GC.
- Do not change `normative`, `interoperability_verified`, or `release_eligible` to true without attributable review evidence and explicit maintainer authorization.
- The `authorized=True` research API flag is **not** an access-control system.
- The GC projection contains unmapped semantics. Recovering the source from the private envelope is not proof of GC-native interoperability.

## Next workstream

After merging research-only code, open a separate tracked independent-review issue/PR. Attach independently authored fixtures and the completed acceptance record. Human approval is a separate release gate.
