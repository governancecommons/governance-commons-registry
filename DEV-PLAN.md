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
| GC-SDK.03 | Add release/publish workflows for PyPI and npm | P1 | implemented; registry credentials/OIDC configuration and first publish pending |
| GC-SDK.04 | Add SDK usage examples for GC adopters | P1 | planned |
| GC-SDK.05 | Define compatibility policy for spec versions | P1 | planned |
| GC-SDK.06 | Prove clean-artifact installs across Windows, macOS, and Linux | P0 | matrix implemented; remote runner evidence pending |

## Cross-Platform Release Gate (2026-07-11)

The SDK now owns a 3-OS × 3-runtime matrix in its own repository. Python
3.11/3.12/3.13 and Node 18/20/22 run on Ubuntu, macOS, and Windows. Jobs test
source, build a wheel/npm tarball, install that artifact, and exercise CLI exit
codes against fixture paths containing spaces and Unicode. This is the release
proof pattern for Marlin and DevXToolkit to reuse. The gate remains open until
GitHub-hosted runs succeed; local Windows source validation alone is not
cross-platform evidence.

## Validation

Run from this repo:

```powershell
python -m pytest -q
npm test
python -m build
npm pack --dry-run
```
