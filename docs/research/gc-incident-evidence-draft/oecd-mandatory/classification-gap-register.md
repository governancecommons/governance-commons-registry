# Classification gap register — GC–INCIDENT.08

Research-only. Source: OECD *Towards a common reporting framework for AI incidents*, DOI 10.1787/f326d4ac-en, Annex B Table B.1. This register is an internal analysis, not independent OECD verification.

| Criterion | Adapter input | GC projection | Finding |
| --- | --- | --- | --- |
| 3, system relationship | system_relationships[].category | affected_systems[].relationship = unknown | Causal contribution is not equivalent to certainty of involvement. |
| 10, severity | severity.categories | severity.status = unassessed | No verified categorical translation into GC severity. |
| 11, harm type | harm_types.categories | harm.status = unknown | Harm type does not independently establish occurrence or assessment. |

The original adapter data is retained only in the restricted private envelope. Recovery from that envelope does not demonstrate semantic equivalence of the GC projection. Independent source review, independently authored fixtures, and human release authorization remain outstanding. Do not merge or publish a claim of interoperability on this evidence alone.
