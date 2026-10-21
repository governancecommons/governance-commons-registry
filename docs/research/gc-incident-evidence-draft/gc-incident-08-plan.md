# GC–INCIDENT.08 — Independent OECD interoperability verification

Status: research-only; not normative, certified, or release eligible.

## Primary-source audit
Verify each of the 29 Annex B Table B.1 criteria against OECD DOI 10.1787/f326d4ac-en, recording exact wording, page, answer format, vocabulary, cardinality and conditional semantics. Distinguish repository transcription from independent reviewer confirmation. Do not promote any verification flag without attributable evidence.

## Independent fixture contract
Fixtures must be authored independently of GC's existing examples and adapter outputs. Every fixture must declare provenance, an expected outcome, and an explicit criterion-level oracle. Cover valid and invalid cases, missing mandatory fields, unsupported enumerations, multiple selections, conditional questions, redaction and unknown values.

## Round-trip gate
For verified fields only, compare OECD → GC → OECD using semantic equivalence and explicit loss accounting. Unknown or unmapped data must be reported, never silently discarded. Negative fixtures must be rejected for the expected reason.

## Release boundary
A passing structural fixture gate is not evidence of independent OECD interoperability. Maintain normative=false, interoperability_verified=false, oecd_conformant=false, release_eligible=false and require human review before any publication.
