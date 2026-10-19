# GC–OECD.01 — AI incident-reporting interoperability gap matrix

**Date:** 2026-10-19  
**Status:** draft; read-only gap assessment, not an adopted standard or conformance declaration  
**Scope:** OECD Artificial Intelligence Papers No. 34 (February 2025) versus inspected Governance Commons schemas and current Registry SDK declarations  
**Authority:** research only; no changes to existing architecture, schema, normative rules, version declarations, or releases.

## Sources and reproducibility

**OECD primary source:** [Towards a common reporting framework for AI incidents](https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/02/towards-a-common-reporting-framework-for-ai-incidents_8c488fdb/f326d4ac-en.pdf), DOI [10.1787/f326d4ac-en](https://doi.org/10.1787/f326d4ac-en). Criteria numbers, names and mandatory flags are sourced from Table 2.2 (printed pp. 17–18; PDF pp. 17–18) and Annex B, Table B.1 (printed pp. 23–24; PDF pp. 23–24). The OECD distinguishes 29 criteria in eight dimensions, **seven mandatory** (#1, #2, #3, #4, #7, #10, #11) and 22 optional. OECD criteria are non-binding guidance, not a GC conformance specification.

**GC evidence inspected on default branches:**
- [GC agent-event schema](https://github.com/governancecommons/governance-commons/blob/main/schemas/gc-agent-event.schema.json) — event types, summaries, agent identity, timestamps, causal parent, evidence URIs, operational severity and security-event fields.
- [GC compliance-evidence schema](https://github.com/governancecommons/governance-commons/blob/main/schemas/gc-compliance-evidence.schema.json) — evidence bundles, notes, signatures, control frameworks; closed enum excludes OECD.
- [GC conformance-report schema](https://github.com/governancecommons/governance-commons/blob/main/docs/conformance/conformance-report.schema.json) — structural rule outcomes and report metadata; no incident-specific report contract.
- [A7 / Phase B reconciliation](https://github.com/governancecommons/governance-commons/blob/main/docs/reconciliation/a7-phase-b.md) — Matrix → APO → ATP → Registry evidence boundary; runtime and durable evidence remain distinct.
- [Registry README](https://github.com/governancecommons/governance-commons-registry/blob/main/README.md) — Python SDK 0.2.0 supports Governance Record and Agent Dossier validation; npm 0.2.0 does not claim parity.
- [Registry compatibility policy](https://github.com/governancecommons/governance-commons-registry/blob/main/docs/compatibility-policy.md) — no silent schema fallback or implicit spec support.
- [GC DEV-PLAN](https://github.com/governancecommons/governance-commons/blob/main/DEV-PLAN.md) — frozen OSS baseline, RFC-0001 public boundary and adoption-evidence checkpoint.

**Review limitation:** GitHub code search did not expose a searchable Registry implementation tree or all Dossier/Matrix/ONS schemas in this run. No executable SDK tests or incident-specific fixtures were run. Accordingly, the matrix assesses **directly inspected contracts only**. A "gap" means **not evidenced in the inspected surfaces**, not proof that no GC repository contains any related field. "Partial" is a reusable primitive, not demonstrated incident reporting support. **Zero criteria are verified as fully implemented OECD-compatible report fields.**

## Classification

- **Verified:** same OECD meaning, type/cardinality, and applicable constraints demonstrated in inspected implementation. **0**
- **Partial:** related existing GC primitive, but missing incident semantics, mandatory constraints, taxonomy, or validation. **8**
- **Gap / not verified:** no sufficient mapping established from inspected contracts. **21**
- **Out of scope:** none excluded from mapping; optionality is preserved.

## Criterion-by-criterion matrix

| # | OECD dimension | OECD criterion (paraphrased) | OECD | GC evidence / candidate surface | Finding | Gap / caution |
|---:|---|---|:---:|---|---|---|
| 1 | Metadata | Title | M | `gc_summary` | partial | Agent-event summary is not an incident-report title |
| 2 | Metadata | Description of incident | M | `gc_summary` | partial | Generic governance summary; no incident narrative contract |
| 3 | Metadata | AI-system relationship to incident | M | `gc_agent_parent_event_id` | gap | Event ancestry is not OECD causal-role taxonomy |
| 4 | Metadata | Submitter role/affiliation | M | `gc_agent_id` | gap | Agent identity does not describe reporter role, email and affiliation |
| 5 | Metadata | Date of first known occurrence | O | `gc_time_loc` | partial | Emission timestamp is not necessarily first occurrence |
| 6 | Metadata | Countries of occurrence | O | `none` | gap | No country list in reviewed schemas |
| 7 | Metadata | Supporting materials | M | `gc_agent_evidence` | partial | Evidence URI strings exist; incident attachments/URL/upload contract not verified |
| 8 | Metadata | AI-system name and version | O | `gc_agent_id; gc_agent_dossier_version` | partial | Agent ID/version is not necessarily affected AI product identity/version |
| 9 | Metadata | Developer/deployer organisations | O | `none` | gap | No developer/deployer organisation fields in reviewed schemas |
| 10 | Harm | Severity | M | `gc_severity` | gap | GC debug/info/warning/error/critical differs from OECD hazard/incident/disaster scale |
| 11 | Harm | Harm type | M | `none` | gap | No OECD harm taxonomy |
| 12 | Harm | Quantification of harm | O | `none` | gap | No losses, casualties, population or compensation data model |
| 13 | Harm | Unintended/wrongful use linkage | O | `gc_event_type` | gap | Policy-violation event is not an incident-specific misuse attribution |
| 14 | People and planet | Affected stakeholders | O | `none` | gap | No affected-party taxonomy |
| 15 | People and planet | Human/fundamental rights impacts | O | `none` | gap | No incident rights-impact checkbox/details |
| 16 | People and planet | Associated AI principles | O | `none` | gap | No OECD principles incident mapping |
| 17 | Economic context | Industries | O | `none` | gap | No ISIC industry selection |
| 18 | Economic context | Business functions | O | `none` | gap | No OECD business-function taxonomy |
| 19 | Economic context | Critical functions/infrastructure | O | `none` | gap | No critical-infrastructure linkage/category |
| 20 | Economic context | Breadth of deployment | O | `none` | gap | No deployment breadth scale |
| 21 | Data and input | Training-data linkage | O | `none` | gap | No incident training-data cause indicator |
| 22 | AI model | Model linkage | O | `none` | gap | No model-causation checkbox/details |
| 23 | AI model | Usage rights | O | `none` | gap | No affected model/product usage-rights taxonomy |
| 24 | AI model | Multiple AI-system interaction linkage | O | `gc_trace_id; gc_agent_parent_event_id` | partial | Multi-agent traces may link events but do not establish OECD incident relationship |
| 25 | Task and output | AI-system tasks | O | `gc_agent_class` | gap | Agent role enum differs from OECD task taxonomy |
| 26 | Task and output | Maximum autonomy level | O | `none` | gap | No OECD autonomy classification |
| 27 | Other | Actions taken | O | `gc_event_type; gc_agent_evidence` | partial | Action/decision events can support evidence but not OECD response categories |
| 28 | Other | Steps to reproduce | O | `none` | gap | No dedicated incident reproduction field |
| 29 | Other | Additional information | O | `notes (compliance evidence bundle)` | partial | Bundle notes are generic, not a report-level free-text extension |

**Important:** GC `gc_severity` is a logging severity, **not** OECD incident severity. GC event parent IDs are **not** OECD AI-system causal-role classifications. GC agent identity is **not** submitter identity. A dossier version is **not** automatically the version of an AI product involved in an incident.

## Coverage summary

| Assessment | Count | Meaning |
|---|---:|---|
| Source criteria inventoried | 29 / 29 | OECD Table 2.2 / Annex B fully indexed |
| Mandatory source criteria | 7 | #1, #2, #3, #4, #7, #10, #11 |
| Optional source criteria | 22 | Do not promote to mandatory by default |
| Verified full GC compatibility | 0 | No incident-specific validator or fixture demonstrated |
| Partial primitives | 8 | Existing GC structures may help with adapter design |
| Gaps / not verified | 21 | Needs further inspection or an additive profile contract |

**Mandatory readiness:** #1, #2, #7 are partial; #3, #4, #10, #11 are gaps. **0/7 verified fully**. This is a conservative evidence assessment, not a claim of zero reusable capability.

## Compatibility and architecture constraints

1. Keep OECD reporting semantics in a separately versioned optional interoperability profile, not in the existing Governance Record core, Agent Matrix, ONS, or ConformanceReport format.
2. Use the existing GC conformance-report *output boundary* only after a separate incident-profile validator is designed and authorized; do not pretend current validators check OECD fields.
3. Preserve OECD optionality and multi-select/single-select/date/text/checkbox semantics as defined in Annex B, including enumerated vocabularies and "other" explanations.
4. Do not force OECD into `control_frameworks` on existing compliance-evidence bundles: that property has a closed enum and its semantics are different from incident reporting.
5. Separate reporter, affected AI system(s), operator/deployer, reviewer and harmed stakeholder identities; separate observed event time from first known incident occurrence.
6. No OECD endorsement, certification, incident truth, containment enforcement, network isolation, or regulatory compliance is implied.
7. Observe RFC-0001 public boundary, current compatibility holds, and GC's independent adoption-evidence gate before broad implementation.

## Next verification and acceptance work

1. Inspect **actual Registry Governance Record v1.0.0 schema/validator/tests** and **Agent Dossier**, **Agent Matrix**, **ONS**, **ATP**, and **APO** repositories at pinned commits; update each row with exact code locations and any additional evidenced primitives.
2. Produce an optional profile proposal (not yet an accepted GC standard) defining OECD fields, types, enumerations, provenance, missing/unknown handling, evidence sensitivity and versioned mapping.
3. Build a representative valid/invalid incident-report fixture pair; demonstrate all **seven mandatory** fields, optional fields, exact cardinality, and conformance-report output.
4. Test in Python; separately establish npm parity or explicitly document its absence. Validate against the OECD Annex B examples and at least one independent external fixture.
5. Perform a security/privacy review of attachments, reporter contact data, exploit reproduction steps, access control, retention and public redaction.
6. Only after evidence-backed review and maintainer authorization, decide whether to register and publish the compatibility profile.

## Validation of this research record

- Source cross-check: all 29 numbered OECD Table 2.2 / Annex B criteria indexed; eight dimension totals = 9 + 4 + 3 + 4 + 1 + 3 + 2 + 3 = 29.
- Mandatory markers transcribed from primary OECD tables: #1, #2, #3, #4, #7, #10, #11.
- Matrix count: 8 partial + 21 gap + 0 verified = 29.
- GitHub source inspection: completed for the six linked GC documents above; no code modifications.
- Runtime/CI tests: **not run**; this is documentation-only research. No claim of implementation closure.
