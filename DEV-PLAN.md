# DEV-PLAN — Governance Commons SDK

**AUTHORITY LEVEL: AL:1**
**Status:** active
Updated: 2026-06-21

## Purpose

`governance-commons-sdk` is the reference implementation repo for Governance
Commons standards. It currently packages ONS validation and GC conformance report
helpers for Python and TypeScript/JavaScript adopters.

## Current Surface

| Surface | Status | Evidence |
| --- | --- | --- |
| Python package `governance-commons` | Implemented | `governance_commons/`, `pyproject.toml` |
| npm package `governance-commons` | Implemented | `src/`, `package.json` |
| CLI wrappers | Implemented | `gc-validate`, `gc-report` |
| Tests | Implemented | `tests/`, `npm test` |
| Registry publication | Planned | PyPI/npm publication pending |

## Active Priorities

| ID | Work | Priority | Status |
| --- | --- | --- | --- |
| GC-SDK.01 | Keep Python and TypeScript ONS behavior aligned | P0 | active |
| GC-SDK.02 | Keep `gc-validate` and `gc-report` stable for downstream tools | P0 | active |
| GC-SDK.03 | Add release/publish workflows for PyPI and npm | P1 | planned |
| GC-SDK.04 | Add SDK usage examples for GC adopters | P1 | planned |
| GC-SDK.05 | Define compatibility policy for spec versions | P1 | planned |

## Validation

Run from this repo:

```powershell
python -m pytest -q
npm test
python -m build
npm pack --dry-run
```
