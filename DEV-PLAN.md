# DEV-PLAN — Governance Commons SDK

**AUTHORITY LEVEL: AL:1**  
**Status:** active  
**Updated:** 2026-09-16

## Purpose

`governance-commons-registry` is the code-level reference implementation repo
for Governance Commons standards. It provides specification validators,
capability discovery, version compatibility declarations, and the shared
machine-readable ConformanceReport contract.

The registry intentionally keeps specification responsibilities separate. The
current contract relationships and authority boundaries are normative in
[`docs/architecture/contract-boundaries.md`](docs/architecture/contract-boundaries.md).
The workflow/lifecycle relationship is normative in
[`docs/architecture/workflow-lifecycle.md`](docs/architecture/workflow-lifecycle.md).
The explicit workflow-to-record bridge is normative in
`docs/architecture/workflow-governance-record-mapping.md`.

## Current Surface

| Surface | Status | Evidence |
| --- | --- | --- |
| Python package `governance-commons` | Implemented | `governance_commons/`, `pyproject.toml` |
| npm package `governance-commons` | Implemented | `src/`, `package.json` |
| Shared ConformanceReport v1.0.0 | Implemented | `governance_commons/report.py`, `src/report.ts`, schema |
| ONS validation | Implemented | Python + TypeScript |
| Capability Contract v0.1 validation | Implemented in Python | `governance_commons/capabilities.py`, bundled schema |
| Capability provider discovery | Implemented in Python | `gc-discover` |
| Agent Dossier instance validation v1.4.0 | Implemented in Python, structural | `governance_commons/dossier.py`, bundled schema |
| Governance Record v1.0.0 schema validation | Implemented in Python | `governance_commons/governance_records.py`, bundled schema |
| Governance Record semantic governance rules | Implemented in Python | authorization, temporal authority, handoff/trust-boundary rules |
| Governance Record representative fixtures | Implemented | `tests/fixtures/governance-record/` |
| A5 Governance Record acceptance gate | Implemented | `tests/test_a5_acceptance.py` |
| Cross-platform clean-artifact CI | Implemented | `.github/workflows/` |
| Python/TypeScript adopter examples | Implemented | `examples/` |
| SDK/spec compatibility policy | Implemented | `governance_commons/versioning.py`, `src/versioning.ts`, `docs/sdk-compatibility.md` |
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

## Active Priorities

| ID | Work | Priority | Status |
| --- | --- | --- | --- |
| A6.1 | Reconcile actual implemented registry surface | P0 | complete |
| A6.2 | Formalize contract relationships and authority boundaries | P0 | complete |
| A6.3 | Reconcile lifecycle/workflow semantics across GC contracts | P0 | complete |
| A6.4 | Define explicit workflow-to-Governance Record mapping/bridge guidance | P0 | complete |
| GC-SDK.02 | Keep `gc-validate` and `gc-report` stable for downstream tools | P0 | active |
| GC-SDK.03 | Maintain package/release workflows | P1 | active |
| GC-SDK.04 | Add SDK usage examples for GC adopters | P1 | complete |
| GC-SDK.05 | Define compatibility policy for spec versions | P1 | complete |
| GC-SDK.07 | Capability Contract v0.1 adoption beyond MVP | P1 | active |

## GC-SDK.05 compatibility boundary

SDK/package versions and specification versions are independent. The repository
now declares an explicit current and minimum-compatible version for every
implemented specification. Current declarations are exact-only because no older
schema revision is bundled. An older version is therefore not treated as
compatible merely because it shares a major version. Future major versions,
unsupported older versions, malformed versions, and unknown specifications are
reported explicitly rather than silently falling back to another contract.

The normative policy is `docs/sdk-compatibility.md`. Python and TypeScript expose
the same classification API for adopters.

## Validation

Run from this repo:

```powershell
python -m pytest -q
npm test
python -m build
npm pack --dry-run
```

The version compatibility suite covers current supported versions, explicitly
ranged older versions, unsupported older versions, future major versions,
malformed versions, two-part Capability Contract versions, and unknown specs.
The fixture matrix is under `tests/fixtures/versioning/`.

## Cross-Platform Release Gate

The repository uses a 3-OS × 3-runtime matrix: Python 3.11/3.12/3.13 and Node
18/20/22 on Ubuntu, macOS, and Windows. Jobs build and install clean artifacts
and exercise validation/CLI behavior. A5 acceptance has been proven through the
same cross-platform workflow.

## Next architectural work

GC-SDK.05 is complete. The next work should preserve the reconciled contract and
workflow boundaries while addressing actual adoption/stability evidence. Current
planned follow-on work remains GC-SDK.02/03 maintenance and GC-SDK.07 Capability
Contract adoption beyond the MVP; TypeScript parity for the other contracts is
not assumed without an adopter-driven requirement.
