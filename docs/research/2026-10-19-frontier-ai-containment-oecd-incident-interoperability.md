# Frontier AI containment, oversight, and incident interoperability — discussion record

**Date:** 2026-10-19  
**Lifecycle:** draft (non-normative research and decision record)  
**Scope:** Governance Commons (GC) external adoption exploration  
**Authority:** Records maintainer direction in discussion; does **not** approve a GC standard, change a release, or assert third-party endorsement.

## Context and opportunity

A reported October 2026 international scientific call involving approximately 400 scientists across 34 countries, including Geoffrey Hinton and Yoshua Bengio, proposes stronger frontier-AI security practices: international containment standards, independent oversight, a registry of serious AI security incidents, and isolation of powerful systems during early testing. The exact letter, signatories, proposals, date, and terminology must be verified against primary sources before external publication or normative citation.

The maintainer identified this as a possible legitimate **external entry point for Governance Commons**. The intended posture is to contribute implementable governance evidence and interoperability to an existing safety/standards effort, **not** to establish a competing international authority, claim that GC enforces network isolation, or change GC's mission.

**Explicit maintainer direction:** expand existing GC capabilities through optional application/interoperability profiles; **do not redesign, rescope, or redirect** the GC architecture. Preserve component independence and existing governance authority.

## Why GC may be relevant

The discussion identified a potential gap between recommendations for independent oversight / incident recording and the technical contracts needed to express identity, restrictions, approvals, revocations, validation results, and audit evidence. GC's existing surfaces may help bridge that gap, subject to current implementation verification:

| Existing surface | Potential role; not a new implementation claim |
| --- | --- |
| Agent Dossier | Reference governed AI system/agent identity, declared capabilities and constraints |
| Agent Matrix | Describe delegated authority, routing, trust and permission boundaries |
| Governance Record | Express authorization, decision, revocation, and evidence references where the current schema permits |
| ONS | Consistent identifiers for governed entities and records |
| Conformance Report / validator | Machine-readable structural validation; not proof of actual containment |
| Project Orchestrator Agent | Potential governance-aware review/escalation integration; runtime availability must be checked |

Illustrative scenario: register a system; record proposed containment constraints; require independent human authorization; record testing evidence and exceptions; link incidents, revocations, and follow-up actions. **Physical/logical isolation, lab security, and independent regulator authority remain external controls.** Passing a GC schema check cannot prove air-gapping, containment effectiveness, or safety.

## OECD AI incident-reporting alignment — adopted direction, not completed work

The discussion agreed to **support the OECD's common AI incident-reporting framework as an optional GC compatibility profile**, not replace GC's governance contracts or declare OECD conformance.

Reference: OECD, *Towards a Common Reporting Framework for AI Incidents* (2025), https://www.oecd.org/en/publications/towards-a-common-reporting-framework-for-ai-incidents_f326d4ac-en.html .

The discussion cited **29 criteria across eight dimensions**, with **seven mandatory and 22 optional**. Treat these figures and each criterion's authoritative wording/mandatory status as **source-verification requirements** before mapping or publication. Do not silently make all 29 mandatory.

Proposed acceptance target: 29/29 source criteria accounted for in a traceable mapping, with mandatory/optional semantics, data types, evidence provenance, disclosure constraints, and explicit unsupported fields preserved. Mapping completeness does **not** establish OECD approval, certification, or operational reporting conformance.

Suggested mapping:
- OECD source criteria define incident-reporting content and applicable optionality.
- A versioned **GC–OECD AI Incident Reporting Compatibility Profile** maps those criteria into GC-compatible data without modifying the core.
- Governance Records link incident reports to authorization, review, and evidence when supported.
- Dossiers identify the system; conformance tooling checks the applicable structural profile.
- Any new incident-specific schema, vocabulary, or rules require separate design review and authorization.

## Candidate application profiles (proposals only)

- **GC-CONTAIN:** containment-governance assertions, restrictions, test authorization, exceptions, and links to external isolation evidence.
- **GC-INCIDENT:** incident-reporting interoperability, OECD criterion mapping, incident classification and evidence references.
- **GC-OVERSIGHT:** independent reviewer identity/authority, approval/rejection, conflict-of-interest handling, escalation and review provenance.

These are **working labels**, not reserved identifiers, registered standards, released features, or authority changes. Avoid introducing normative profile identifiers until checked against ONS, registry rules, existing profile taxonomy and maintainer approval.

## Federated reporting concept

A possible federation rather than one mandatory centralized database:
1. Lab or operator retains detailed local incident and evidence records.
2. Authorized independent reviewer validates a permitted subset and review decision.
3. National/international reporting endpoints exchange a standards-compatible incident envelope.
4. Public disclosure is redacted and appropriately delayed where security, privacy, or legal obligations require.
5. Integrity, signing, provenance, versioning and revocation remain explicit, independently verifiable claims rather than assumed guarantees.

Threat model must address sensitive exploit information, confidentiality, false or duplicate reports, identity spoofing, tampering, compromised reviewers, retention, and cross-border disclosure.

## External engagement and adoption pathway

GC should lead with a small, verifiable demonstration rather than a broad new roadmap or pitch deck:

1. Read-only inspect current GC registry, Governance Record, Dossier, Matrix, ONS, conformance-report and SDK surfaces; distinguish schema/spec from actual runtime.
2. Verify the scientists' primary letter and the full OECD 29-criterion primary source; document citations, definitions and version/date.
3. Produce a criterion-by-criterion mapping: **supported / partially supported / profile extension needed / out of scope**, including mandatory versus optional status and provenance.
4. Build **one representative containment-review plus incident-report example** with machine-readable fixtures, validation output and honest gaps; no fake evidence of actual isolation.
5. Compare the proposed interface with existing standards (OECD, and as relevant NIST AI RMF, ISO/IEC 42001, EU AI Act) without claiming equivalence or endorsement.
6. Publish a concise technical interoperability note and request feedback from researchers, incident-reporting initiatives, standards contributors, and labs.
7. Use external feedback and independent reproducibility as the adoption gate before opening a broad new implementation track.

Potential outreach framing: GC is an open governance infrastructure project exploring machine-readable authorization, oversight and auditability; it has mapped containment and incident-reporting recommendations to existing contracts and seeks technical feedback on a preliminary example. Do not imply endorsement by named scientists, OECD or standards bodies.

## Risks and implementation gaps

- Existing schemas may not cover all OECD fields or incident semantics.
- Independent reviewer authority, separation of duties and conflicts of interest need an explicit trust model.
- Tamper-evident audit and signed evidence claims must be verified end-to-end rather than inferred from schemas.
- Incident classification, cross-registry identity, provenance, version negotiation, correction/retraction and disclosure need design.
- Network isolation and containment are external operational/security controls.
- A conformance pass is not certification, incident truth, safety, enforcement, or international recognition.
- New scope must respect GC's frozen OSS baseline, public-boundary RFC-0001, compatibility holds, and adoption-evidence checkpoint.
- No code, schema, spec, release, website, authority, or approval changes are authorized by this research record.

## Decision ledger

| Topic | Discussion outcome | Status |
| --- | --- | --- |
| Opportunity | Explore the scientific call as a credible GC adoption entry point | exploratory |
| Architecture | Expand through optional profiles; no redesign/rescope/redirect | maintainer direction |
| OECD | Support 29-criterion incident reporting via compatibility mapping; preserve mandatory/optional distinctions | direction; mapping not done |
| Profile names | GC-CONTAIN, GC-INCIDENT, GC-OVERSIGHT | proposed working labels |
| Federation | Evaluate federated registry/exchange and independently reviewed evidence | proposed |
| Engagement | Demonstrate and seek independent feedback before broad build-out | proposed |
| Implementation | Verify existing contracts and primary sources before designing extensions | queued |
| External claims | No OECD/scientist endorsement, containment guarantee or completed implementation claim | constraint |

## Primary sources and follow-up

- OECD publication: https://www.oecd.org/en/publications/towards-a-common-reporting-framework-for-ai-incidents_f326d4ac-en.html
- Scientific letter: primary publication URL, signatories and precise recommendations **to be independently confirmed** before external use.
- Internal implementation baseline: registry README (Python/npm 0.2.0 feature disparity), current component manifests and actual validators.
- Governance boundaries: DEV-ACCORD.03, DEV-ACCORD.06, DEV-ACCORD.10, portfolio PROTECTED.md, and RFC-0001/public-boundary activation gates.

**Record limitations:** This captures the substance, decisions, proposals and caveats of the 2026-10-19 discussion, not a verbatim chat transcript. No criterion-by-criterion OECD mapping, external source validation, runtime proof, CI execution, independent review, or profile acceptance is asserted here.
