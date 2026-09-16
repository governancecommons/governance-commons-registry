# DEV-PLAN — Governance Commons SDK

**AUTHORITY LEVEL: AL:1**  
**Status:** active  
**Updated:** 2026-09-16

## Purpose

`governance-commons-registry` is the code-level reference implementation repo
for Governance Commons standards. It provides specification validators,
capability discovery, and the shared machine-readable ConformanceReport contract.

The registry intentionally keeps specification responsibilities separate. The
current contract relationships and authority boundaries are normative in
[`docs/architecture/contract-boundaries.md`](docs/architecture/contract-boundaries.md).
The workflow/lifecycle relationship is normative in
[`docs/architecture/workflow-lifecycle.md`](docs/architecture/workflow-lifecycle.md).
The explicit workflow-to-record bridge is normative in
[`docs/architecture/workflow-governance-record-mapping.md`](docs/architecture/workflow-governance-record-mapping.md).
The cross-spec implementation reconciliation is normative guidance in
[`docs/architecture/ecosystem-conformance-reconciliation.md`](docs/architecture/ecosystem-conformance-reconciliation.md).

## Current Surface

| Surface | Status | Evidence |
| --- | --- | --- |
| Python package `governance-commons` | Implemented | `governance_commons/`, `pyproject.toml` |
| npm package `governance-commons` | Implemented | `src/`, `package.json` |
| Shared ConformanceReport v1.0.0 | Implemented | `governance_commons/report.py`, `src/report.ts`, schema |
| ONS validation | Implemented | Python + TypeScript |
| Capability Contract v0.1 validation | Implemented in Python | `governance_commons/capabilities.py`, bundled schema |
| Capability provider discovery | Implemented in Python | `gc-discover` |
| Capability Contract v0.1 adopter pattern | Implemented | `.governance/contracts/capabilities.yaml`, `docs/capability-adoption.md` |
| Capability Contract adoption acceptance gate | Implemented | `tests/test_sdk07_acceptance.py`, `tests/fixtures/capability-adoption/` |
| Agent Dossier instance validation v1.4.0 | Implemented in Python, structural | `governance_commons/dossier.py`, bundled schema |
| Governance Record v1.0.0 schema validation | Implemented in Python | `governance_commons/governance_records.py`, bundled schema |
| Governance Record semantic governance rules | Implemented in Python | authorization, temporal authority, handoff/trust-boundary rules |
| Governance Record representative fixtures | Implemented | `tests/fixtures/governance-record/` |
| A5 Governance Record acceptance gate | Implemented | `tests/test_a5_acceptance.py` |
| Cross-platform clean-artifact CI | Implemented | `.github/workflows/` |
| Python/TypeScript adopter examples | Implemented | `examples/` |
| Specification compatibility policy | Implemented | `governance_commons/compatibility.py`, `docs/compatibility-policy.md` |
| Package/release workflow gate | Implemented | `tests/release_acceptance.py`, `.github/workflows/main.yml`, `.github/workflows/publish-js.yml` |
| TypeScript parity for Dossier/Capability/Governance Record | Not yet implemented | Deliberate current asymmetry |
| Agent Matrix validator | Not implemented in this repo | Separate contract/workstream |
| Project Orchestrator validator | Not implemented in this repo | Separate contract/workstream |

## Contract authority boundaries

The registry follows these rules:

- **ONS** owns naming and identifier conformance; it does not grant authority.
- **Capability Contract** owns capability declarations and discovery semantics;
  declaration/discovery does not grant execution permission.
- **Agent Dossier** owns agent identity/profile structure; dossier validity does
  not authorize an agent to act.
- **Governance Record** owns durable governed-event records and governance-rule
  evaluation, including authority, approval, action, handoff, revocation, and
  validation relationships.
- **ConformanceReport v1.0.0** owns the shared validation-result output format;
  it reports results but does not grant authority or mutate the subject.

Structural validity and governance validity remain separate. A record may be
JSON-Schema-valid and still fail a semantic governance rule.

## Workflow/lifecycle boundary

GC does not define a competing execution lifecycle. POKEE, TBV, eco, LASSO, or
another compatible workflow may execute work and emit governance-significant
events. Governance Record captures those events; governance rules evaluate the
applicable authority/evidence; ConformanceReport remains the shared validation
output boundary.

The normative lifecycle reconciliation is documented in
`docs/architecture/workflow-lifecycle.md`. It establishes that workflow state,
record type, and governance status remain distinct, that timestamps and
relations provide event linkage, and that the registry is not an execution
runtime or orchestrator.

## Active Priorities

| ID | Work | Priority | Status |
| --- | --- | --- | --- |
| A6.1 | Reconcile actual implemented registry surface | P0 | complete |
| A6.2 | Formalize contract relationships and authority boundaries | P0 | complete |
| A6.3 | Reconcile lifecycle/workflow semantics across GC contracts | P0 | complete |
| A6.4 | Define explicit workflow-to-Governance Record mapping/bridge guidance | P0 | complete |
| GC-SDK.02 | Keep `gc-validate` and `gc-report` stable for downstream tools | P0 | complete |
| GC-SDK.03 | Maintain package/release workflows | P1 | complete |
| GC-SDK.04 | Add SDK usage examples for GC adopters | P1 | complete |
| GC-SDK.05 | Define compatibility policy for spec versions | P1 | complete |
| GC-SDK.07 | Capability Contract v0.1 adoption beyond MVP | P1 | complete |
| A7 | Reconcile ATP, Agent Matrix, and APO implemented surfaces and define the cross-spec binding boundary | P0 | reconciliation complete; implementation queued in owning specs |

## A7 — ecosystem conformance reconciliation

A7 was reconciled against the actual `main` surfaces of Agent Team Protocol,
Agent Matrix, and Agent Project Orchestrator. The reconciliation is captured in
`docs/architecture/ecosystem-conformance-reconciliation.md`.

Key findings:

- ATP currently has five section schemas and schema-level test vectors, but no
  complete validator/CLI, CI workflow, delegation/trust runtime verifier, or
  shared-audit runtime writer/verifier.
- ATP's delegation policy requires orchestrator countersigning, while the
  current delegation JSON Schema leaves `signature` optional. This is a
  concrete structural/policy gap to resolve in ATP rather than in the Registry.
- Agent Matrix owns capability/profile/routing semantics. APO already consumes
  Matrix routing and the effective roster for explainable recommendations.
- APO owns runtime dispatch, retries, escalation handling, governance loading,
  resource budgets, telemetry, and agent-dossier-compatible handoff envelopes.
- ATP owns fleet-level delegation, trust, shared audit, fleet escalation, and
  team lifecycle. It should consume Matrix/Orchestrator surfaces rather than
  duplicate their authority or execution models.
- The primary missing integration seam is an explicit binding from APO
  handoff/delegation/escalation events to ATP audit/delegation/trust semantics.
- Governance Record remains the durable governed-event/evidence boundary and
  ConformanceReport remains the shared validation-result boundary.

The next implementation work belongs primarily to ATP and should produce a
complete validator/CI path, executable semantic checks, and an interoperability
fixture spanning Matrix → APO → ATP. Registry changes should consume those
established contracts rather than implement fleet runtime behavior.

## Validation

Run from this repo:

```powershell
python -m pytest -q
npm test
python -m build
npm pack --dry-run
python tests/release_acceptance.py
```

Python validation currently supports:

```powershell
gc-validate --spec ons <subject>
gc-validate --spec capabilities <subject>
gc-validate --spec dossier <subject>
gc-validate --spec governance-record <subject>
gc-discover --capability <capability-id> <repo-root> [<repo-root> ...]
```

The npm surface currently remains ONS/report focused. TypeScript parity for
Capability Contract, Agent Dossier, and Governance Record is a future decision,
not an assumed requirement of the current architecture.

Adopter examples in `examples/` use the existing public SDK/validator surfaces
and existing representative fixtures; they do not define parallel schemas or
runtime behavior.

Capability Contract adoption is documented in `docs/capability-adoption.md`.
The registry itself now carries a canonical `.governance/contracts/capabilities.yaml`
declaration, and the SDK.07 acceptance gate covers provider, consumer, hybrid,
prohibited-boundary, semantic-conflict, and multi-provider discovery cases.

Specification compatibility is documented in `docs/compatibility-policy.md`
and implemented by `governance_commons.compatibility`. SDK/package versions are
independent of specification versions; compatibility is explicit and never
implies silent schema fallback.

## Cross-Platform Release Gate

The repository uses a 3-OS × 3-runtime matrix: Python 3.11/3.12/3.13 and Node
18/20/22 on Ubuntu, macOS, and Windows. Jobs build and install clean artifacts
and exercise validation/CLI behavior. A5 acceptance has been proven through the
same cross-platform workflow. GC-SDK.02 adds explicit npm built-CLI acceptance
and Python report-version boundary coverage. GC-SDK.03 additionally checks that
package metadata agrees across Python/npm and that release tags match metadata
before publication.

## Package Release Workflow

`docs/sdk-0.2-release.md` documents the explicit release workflow. Tag-triggered
publication uses `sdk-v<version>` and both package surfaces must agree on the
version. Manual publication requires an explicit version input. Publication is
not performed by the ordinary cross-platform CI workflow.

## Next architectural work

A6.4, GC-SDK.02, GC-SDK.03, GC-SDK.04, GC-SDK.05, and GC-SDK.07 are complete. A7
now establishes the cross-spec implementation boundary. The next implementation
should occur in the owning ATP/Matrix/APO repositories and then be consumed by
the Registry through fixtures and shared ConformanceReport/Governance Record
boundaries. No universal governance runtime or parallel authority layer should
be introduced.
