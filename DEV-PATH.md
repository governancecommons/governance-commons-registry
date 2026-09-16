# DEV-PATH — Governance Commons SDK

**AUTHORITY LEVEL: AL:1**
**Status:** active
Updated: 2026-09-16

## Role

This repo is the code-level reference implementation for Governance Commons
standards. It is not a website and not an editor extension. VS Code extensions
belong in separate repos such as `governance-commons-vscode`.

## Current State

- Git repo exists and is on `main`.
- Python package `governance-commons` v0.2.0 includes ONS, Capability Contract,
  Agent Dossier structural validation, and Governance Record validation.
- npm package `governance-commons` v0.1.1 remains the ONS/report-focused surface.
- CLI wrappers exist for `gc-validate` and `gc-report`; Python also provides
  `gc-discover` for capability discovery.
- Governance Record v1.0.0 structural and semantic validation is implemented.
- A5 acceptance and A6.1-A6.4 architectural reconciliation are complete.
- Cross-platform clean-artifact CI covers Ubuntu/macOS/Windows with Python
  3.11-3.13 and Node 18/20/22.

## Validation Baseline

Use these commands from the repository root:

```powershell
python -m pytest -q
npm test
python -m build
npm pack --dry-run
```

Use `python -m pytest -q` rather than bare `pytest` so the active interpreter
and local checkout are used consistently.

## Next Work

| ID | Status | Notes |
| --- | --- | --- |
| GC-SDK.02 | active | Preserve `gc-validate` / `gc-report` behavior and shared report output for downstream tools. |
| GC-SDK.03 | active | Maintain package/release workflows; publication remains a separate release decision. |
| GC-SDK.04 | complete | Added minimal adopter examples for Python and TypeScript. |
| GC-SDK.05 | planned | Define compatibility policy between SDK version and GC spec versions. |

## Cross-Platform Clean-Artifact Matrix

The release matrix distinguishes portable design from proven installation:
Ubuntu/macOS/Windows for Python 3.11-3.13 and Node 18/20/22. The matrix builds
and installs wheel/tarball artifacts rather than editable source, then checks
`gc-validate` success, conformance failure, and input-error exit codes using
paths with spaces and Unicode.

## Capability Contract MVP

Python SDK v0.2.0 adds the executable Capability Contract v0.1 proof without
changing the frozen npm/ONS surface. `gc-validate --spec capabilities` parses
YAML, validates the bundled Draft 2020-12 schema, and applies deterministic
semantic checks. `gc-discover` scans explicit repository roots and answers exact
capability queries without evaluating or granting execution authority.

## Architecture Reconciliation

A6.1-A6.4 established the current boundaries:

- POKEE/TBV/eco/LASSO remain workflow/runtime architectures.
- Governance Record captures governance-significant events rather than workflow
  state.
- ConformanceReport v1.0.0 remains the shared validation-result boundary.
- Validators report; they do not execute or grant authority.
- The workflow-to-record bridge is event-oriented, not a second state machine.

GC-SDK.04 examples build on those boundaries without introducing a new runtime
or duplicating any contract schema.
