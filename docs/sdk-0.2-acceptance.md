# SDK 0.2 Acceptance

**Status:** implementation complete  
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
- `gc-validate`, `gc-report`, and `gc-discover` CLI entry points

### npm 0.2.0

The package retains its existing ONS/report-focused public surface:

- root exports for ONS and report utilities
- `./ons` subpath
- `./report` subpath
- `gc-validate` and `gc-report` CLI entry points

Capability Contract, Agent Dossier, and Governance Record TypeScript parity are
not silently introduced by the version bump.

## CLI/report stability boundary

The CLI contract uses three outcome classes:

- **Exit `0`** — validation/report is conformant.
- **Exit `1`** — validation/report is well-formed and explicitly non-conformant.
- **Exit `2`** — invocation, input, or report-format error; no conformance
  result is asserted.

Both CLI implementations support text and JSON output where exposed by their
public surface. JSON validation output is the machine-readable
ConformanceReport v1.0.0 boundary. `gc-report` accepts only the supported
`gc_report_version` and rejects unsupported report versions rather than silently
interpreting them as the current format.

The npm acceptance test exercises the built CLI entry points themselves,
including pass/fail exit semantics, text output, JSON structure, saved-report
round-trip, malformed input, and unsupported report-version rejection. Python
acceptance tests cover the corresponding module CLI surface and the same report
version boundary.

## Breaking vs additive changes

| Change | Classification | Rationale |
| --- | --- | --- |
| npm package `0.1.1` → `0.2.0` | Version-boundary change | Per the repository's pre-1.0 compatibility policy, a minor package version is a compatibility boundary. |
| Align TypeScript `PACKAGE_VERSION` with package metadata | Corrective/additive | Removes an existing metadata mismatch; no public function is removed. |
| Export implemented Python dossier/governance-record validators | Additive | Makes existing implemented capabilities directly importable from the package root. |
| Add version-consistency smoke tests | Additive | Test-only protection for release metadata. |
| Add CLI acceptance tests | Additive | Locks public CLI exit codes and report I/O behavior. |
| Enforce ConformanceReport version at Python `gc-report` boundary | Corrective | Aligns Python behavior with the shared v1.0.0 report contract and prevents silent format interpretation. |
| Update clean-artifact npm install target | Corrective | Keeps CI aligned with the package version. |
| Add SDK 0.2 acceptance documentation | Additive | Makes the release boundary inspectable. |
| Add TypeScript Capability/Dossier/Governance Record validators | **Out of scope** | Not required by the current architecture or SDK.07 acceptance boundary. |

## Acceptance criteria

1. Python package metadata is `0.2.0`.
2. npm package metadata and lockfile are `0.2.0`.
3. TypeScript runtime package metadata reports `0.2.0`.
4. Existing ONS and ConformanceReport public surfaces remain available.
5. Implemented Python Capability, Dossier, Governance Record, and compatibility
   validators are importable from the package root.
6. `gc-validate` preserves exit `0` for conformant validation, exit `1` for
   explicit validation failure, and exit `2` for malformed invocation/input.
7. `gc-report` preserves exit `0` for conformant reports, exit `1` for
   non-conformant reports, and exit `2` for malformed/unsupported report input.
8. `gc-validate` JSON output is a ConformanceReport v1.0.0 and `gc-report` can
   round-trip that report without changing its machine-readable content.
9. Unsupported ConformanceReport versions are rejected; no silent version
   fallback occurs.
10. No validator grants authority, executes workflow, mutates subjects, or
    bypasses the ConformanceReport boundary.
11. No TypeScript parity is claimed for contracts that remain Python-only.
12. `python -m pytest -q`, `npm test`, `python -m build`, and `npm pack --dry-run`
    pass.
13. The cross-platform 3-OS × 3-runtime CI matrix passes against the release
    candidate commit.
14. The final change is committed and merged to `main` only after CI passes.

## Release boundary

SDK/package versioning remains independent of specification versioning. A
package release does not imply a new GC specification version. Specification
compatibility continues to be evaluated by the explicit compatibility policy;
package version changes never authorize silent schema fallback or automatic
execution behavior.
