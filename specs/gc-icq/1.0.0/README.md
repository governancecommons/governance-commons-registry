# GC–ICQ.01 — Information Classification Quadrant
**Specification version:** 1.0.0 (proposed; not ratified)

GC–ICQ classifies an information asset using two independent axes: **disclosure impact** (low/high) and **current access posture** (restricted/open). The quadrants are descriptive risk conditions, **not** mutually exclusive information types.

| Quadrant | Impact | Access | Interpretation |
| --- | --- | --- | --- |
| Q1 | high | restricted | High-impact restricted information; apply appropriate safeguards |
| Q2 | low | restricted | Private/internal working information |
| Q3 | low | open | Low-impact publicly accessible information; not necessarily approved |
| Q4 | high | open | Exposure risk; investigate and restrict, or document authorized exception |

## Required labels
Use zero or more `dataLabels`: `PERSONAL_DATA`, `CREDENTIAL`, `EMBARGOED`, `PROPRIETARY`, `SECURITY_FINDING`, `OTHER_SENSITIVE`. These are orthogonal to the quadrant. `CREDENTIAL` requires dedicated secrets storage, rotation when exposed, and cannot be authorized for publication by an exception.

## Publication gate
The quadrant alone never authorizes publication. Publication requires explicit `publication.status=approved`, a human `approvedBy` and `approvalRecordId`, `impact=low`, `access=open`, and no sensitive data labels. A high-impact/open Q4 record is blocked by default. An approved Q4 exception may authorize *controlled disclosure* only (not automatic public publication), and requires an identified authority, rationale, expiry and mitigations. No exception can override credential protections.

## Governance controls
Classify before ingestion or external publication. Reassess upon source changes, new vulnerabilities, access changes, or disclosure events. Maintain an audit trail and review access independently of evidence quality. Redact personal identifiers in public evidence exports. Treat unexpected Q4 as an incident requiring triage. The information owner approves exceptions; a distinct human publication reviewer approves public release.

## Integration
The Registry owns this classification contract. Observatory Core enforces it at publication; Agent Dossier and Matrix may reference its version without transferring ownership of their own schemas. This proposal does not alter existing SDK releases or claim that the policy is deployed.
