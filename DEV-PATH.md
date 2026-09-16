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
  Agent Dossier structural validation, Governance Record validation, and
  compatibility classification.
- npm package `governance-commons` v0.2.0 remains the ONS/report-focused surface.
- CLI wrappers exist for `gc-validate` and `gc-report`; Python also provides
  `gc-discover` for capability discovery.
- Governance Record v1.0.0 structural and semantic validation is implemented.
- A5 acceptance and A6.1-A6.4 architectural reconciliation are complete.
- Cross-platform clean-artifact CI covers Ubuntu/macOS/Windows with Python
  3.11-3.13 and Node 18/20/22.
- GC-SDK.04 adopter examples and GC-SDK.05 specification compatibility policy
  are complete.
- GC-SDK.02 CLI/report behavior and GC-SDK.03 package/release workflow
  maintenance are complete.

## SDK 0.2 boundary

SDK 0.2 consolidates the existing implemented Python 0.2.0 surface with the
npm package metadata and release gate. It does not require TypeScript parity for
Capability Contract, Agent Dossier, or Governance Record.

The package version boundary is separate from specification versions. For
pre-1.0 package versions, a minor version is a compatibility boundary; SDK 0.2
does not silently promise compatibility with npm 0.1.x. Existing public
ONS/report exports remain available, and the Python package additionally
exposes the validators already implemented in the repository.

See `docs/sdk-0.2-acceptance.md` and `docs/sdk-0.2-release.md` for the
inspectable acceptance and release criteria.

## Validation Baseline

Use these commands from the repository root:

```powershell
python -m pytest -q
npm test
python -m build
npm pack --dry-run
python tests/release_acceptance.py
```

Use `python -m pytest -q` rather than bare `pytest` so the active interpreter
and local checkout are used consistently.

## Next Work

| ID | Status | Notes |
| --- | --- | --- |
| GC-SDK.02 | complete | CLI/report behavior locked with cross-language acceptance coverage and explicit report-version rejection. |
| GC-SDK.03 | complete | Package/release workflows now validate matching versions, release tags, tests, and clean artifacts before publication. |
| GC-SDK.04 | complete | Added minimal adopter examples for Python and TypeScript. |
| GC-SDK.05 | complete | Defined specification compatibility policy. |
| GC-SDK.07 | active | Continue Capability Contract v0.1 adoption beyond MVP. |

## Cross-Platform Clean-Artifact Matrix

The release matrix distinguishes portable design from proven installation:
Ubuntu/macOS/Windows for Python 3.11-3.13 and Node 18/20/22. The matrix builds
and installs wheel/tarball artifacts rather than editable source, then checks
`gc-validate` success, conformance failure, and input-error exit codes using
paths with spaces and Unicode. The npm artifact smoke test is pinned to the
current SDK 0.2.0 package name. Release metadata acceptance is also exercised
across the Python matrix and npm package metadata is checked across the Node
matrix.

## Package Release Workflow

GC-SDK.03 release mechanics are documented in `docs/sdk-0.2-release.md`.
Publication remains an explicit release decision. Release workflows do not
invent versions or silently downgrade package/specification compatibility.

## Capability Contract MVP

Python SDK v0.2.0 provides the executable Capability Contract v0.1 proof without
changing the frozen TypeScript contract surface. `gc-validate --spec
capabilities` parses YAML, validates the bundled Draft 2020-12 schema, and
applies deterministic semantic checks. `gc-discover` scans explicit repository
roots and answers exact capability queries without evaluating or granting
execution authority.

## Architecture Reconciliation

A6.1-A6.4 established the current boundaries:

- POKEE/TBV/eco/LASSO remain workflow/runtime architectures.
- Governance Record captures governance-significant events rather than workflow
  state.
- ConformanceReport v1.0.0 remains the shared validation-result boundary.
- Validators report; they do not execute or grant authority.
- The workflow-to-record bridge is event-oriented, not a second state machine.

GC-SDK.04 examples, GC-SDK.05 compatibility policy, and GC-SDK.03 release
maintenance build on those boundaries without introducing a new runtime or
duplicating any contract schema.
