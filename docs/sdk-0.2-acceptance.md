# SDK 0.2 Acceptance

**Status:** implementation in progress  
**Target package version:** `0.2.0`

## Scope derived from the repository

SDK 0.2 consolidates the already-implemented Python 0.2.0 surface with the
npm package and makes the public Python exports explicit. It does **not** make
TypeScript parity for Capability Contract, Agent Dossier, or Governance Record
a release requirement; the current architecture deliberately records that
asymmetry.

The work is grounded in GC-SDK.02 (CLI/report stability), GC-SDK.03
(package/release workflow maintenance), and GC-SDK.07 (Capability Contract v0.1
adoption). GC-SDK.04 examples and GC-SDK.05 compatibility policy are treated as
existing release inputs, not reimplemented here.

## Public surface

### Python 0.2.0

The package exposes:

- ONS v1.4.0 validation and grammar utilities
- ConformanceReport v1.0.0 types/building
- Capability Contract v0.1 validation and discovery
- Agent Dossier v1.4.0 structural validation
- Governance Record v1.0.0 validation, including semantic governance rules
- Specification compatibility classification
- `gc-validate`, `gc-report`, and `gc-discover`

### npm 0.2.0

The package retains its existing ONS/report-focused public surface:

- root exports for ONS and report utilities
- `./ons` subpath
- `./report` subpath
- `gc-validate` and `gc-report` CLI entry points

Capability Contract, Agent Dossier, and Governance Record TypeScript parity are
not silently introduced by the version bump.

## Breaking vs additive changes

| Change | Classification | Rationale |
| --- | --- | --- |
| npm package `0.1.1` → `0.2.0` | Version-boundary change | Per the repository's pre-1.0 compatibility policy, a minor package version is a compatibility boundary. |
| Align TypeScript `PACKAGE_VERSION` with package metadata | Corrective/additive | Removes an existing metadata mismatch; no public function is removed. |
| Export implemented Python dossier/governance-record validators | Additive | Makes existing implemented capabilities directly importable from the package root. |
| Add version-consistency smoke tests | Additive | Test-only protection for release metadata. |
| Update clean-artifact npm install target | Corrective | Keeps CI aligned with the published package version. |
| Add SDK 0.2 acceptance documentation | Additive | Makes the release boundary inspectable. |
| Add TypeScript Capability/Dossier/Governance Record validators | **Out of scope** | Not required by the current architecture or SDK.07 acceptance boundary. |

## Acceptance criteria

1. Python package metadata is `0.2.0`.
2. npm package metadata and lockfile are `0.2.0`.
3. TypeScript runtime package metadata reports `0.2.0`.
4. Existing ONS and ConformanceReport public surfaces remain available.
5. Implemented Python Capability, Dossier, Governance Record, and compatibility
   validators are importable from the package root.
6. `gc-validate`, `gc-report`, and `gc-discover` behavior remains covered by
   existing tests and clean-artifact smoke tests.
7. No validator grants authority, executes workflow, mutates subjects, or
   bypasses the ConformanceReport boundary.
8. No TypeScript parity is claimed for contracts that remain Python-only.
9. `python -m pytest -q`, `npm test`, `python -m build`, and `npm pack --dry-run`
   pass.
10. The cross-platform 3-OS × 3-runtime CI matrix passes against the release
    candidate commit.
11. The final change is committed and merged to `main` only after CI passes.

## Release boundary

SDK/package versioning remains independent of specification versioning. A
package release does not imply a new GC specification version. Specification
compatibility continues to be evaluated by the explicit compatibility policy;
package version changes never authorize silent schema fallback or automatic
execution behavior.
