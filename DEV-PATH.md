# DEV-PATH — Governance Commons SDK

**AUTHORITY LEVEL: AL:1**
**Status:** active
Updated: 2026-06-21

## Role

This repo is the code-level reference implementation for Governance Commons
standards. It is not a website and not an editor extension. VS Code extensions
belong in separate repos such as `governance-commons-vscode`.

## Current State

- Git repo exists and is on `main`.
- Python package is scaffolded as `governance-commons` version `0.1.0`.
- npm package is scaffolded as `governance-commons` version `0.1.0`.
- ONS validation logic exists in Python and TypeScript.
- CLI wrappers exist for `gc-validate` and `gc-report`.
- Publication to package registries is pending.

## Validation Baseline

2026-06-21:

- `python -m pytest -q` passes: 150 tests.
- `npm test` passes.
- `python -m build` passes.

Use `python -m pytest -q` rather than bare `pytest` so the active interpreter
and local checkout are used consistently.

## Next Work

| ID | Status | Notes |
| --- | --- | --- |
| GC-SDK.03 | in-progress | Publish workflows now live in this SDK repo; first authenticated PyPI/npm publish remains. |
| GC-SDK.04 | planned | Add minimal adopter examples for Python and TypeScript. |
| GC-SDK.05 | planned | Define compatibility policy between SDK version and GC spec versions. |

## Cross-Platform Clean-Artifact Matrix (2026-07-11)

Added the first portfolio release matrix that distinguishes portable design
from proven installation: Ubuntu/macOS/Windows for Python 3.11-3.13 and Node
18/20/22. The matrix builds and installs wheel/tarball artifacts rather than
editable source, then checks `gc-validate` success, conformance failure, and
input-error exit codes using paths with spaces and Unicode. Publish workflows
were placed in this actual SDK repository; the parent governance-commons repo
gitignores this nested repo and therefore cannot build it from a normal parent
checkout. Remote matrix success and first registry publication remain open.

## Capability Contract MVP (2026-08-17)

Python SDK v0.2.0 adds the executable Capability Contract v0.1 proof without
changing the frozen npm/ONS surface. `gc-validate --spec capabilities` safely
parses YAML, validates the bundled Draft 2020-12 schema, and applies deterministic
duplicate-provider, provided/prohibited-conflict, and duplicate-interface checks.
`gc-discover` scans explicit repository roots, reports invalid declarations, and
answers exact capability queries without evaluating or granting execution
authority.

The bundled schema is semantically identical to the normative v0.1 schema in the
dev-docs contract package. The Python suite covers pure consumers, exact
three-segment IDs, version requirements, YAML numeric coercion, omitted schema
defaults, semantic conflicts, zero/one/multiple providers, invalid-provider
reporting, CLI output, and authority-boundary output. Source validation completed
with 184 Python tests and the existing TypeScript typecheck/build; Python wheel and
sdist creation also succeeded. Registry publication remains a separate release
decision.
