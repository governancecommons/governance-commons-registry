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
| GC-SDK.03 | planned | Add PyPI and npm publish workflows aligned with Governance Commons release gates. |
| GC-SDK.04 | planned | Add minimal adopter examples for Python and TypeScript. |
| GC-SDK.05 | planned | Define compatibility policy between SDK version and GC spec versions. |
