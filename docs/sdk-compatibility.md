# GC-SDK.05 — Specification compatibility policy

**Status:** normative for the registry SDK implementation

## 1. Version layers are independent

Governance Commons has three distinct version layers:

- **SDK/package version** identifies a released implementation artifact. The
  Python package is currently `0.2.0`; the npm package is currently `0.1.1`.
- **Specification version** identifies the contract being validated, such as
  ONS `1.4.0` or Governance Record `1.0.0`.
- **ConformanceReport version** identifies the output contract. It remains
  `1.0.0` and is independent of both package and specification versions.

A package version MUST NOT be interpreted as a specification version, and a
specification version MUST NOT be inferred from a package version.

## 2. Compatibility is explicit

A validator has an explicit current specification version and an explicit
minimum compatible version. The implementation MUST NOT silently substitute a
different schema or contract when the requested version is outside that range.

The result classes are:

| Status | Meaning |
| --- | --- |
| `supported` | Requested version exactly matches the validator's current version. |
| `compatible` | Requested older version is inside an explicitly declared compatibility range. |
| `unsupported` | Requested version is outside that range, including future major versions and older versions for which no compatibility support is declared. |
| `invalid` | Requested version is not a syntactically valid GC version. |

Compatibility is therefore an implementation claim, not a generic assumption
that all versions with the same major number are interchangeable.

## 3. Current registry declaration

The current repository bundles only one schema/contract revision for each
implemented validator. Therefore the minimum compatible version currently equals
the current version:

| Spec | Current | Minimum compatible | Current status |
| --- | --- | --- | --- |
| ONS | `1.4.0` | `1.4.0` | exact support only |
| Agent Dossier | `1.4.0` | `1.4.0` | exact support only |
| Governance Record | `1.0.0` | `1.0.0` | exact support only |
| Capability Contract | `0.1` | `0.1` | exact support only |

This is deliberately conservative. An older specification becomes `compatible`
only after its schema/semantics are actually retained and the compatibility
boundary is changed explicitly.

## 4. Validator behavior

Version handling occurs before any claim that a different contract is being
validated. A malformed declaration is `invalid`; a known-but-not-supported
revision is `unsupported`. Validators remain deterministic and side-effect free.
They report conformance; they do not execute, authorize, approve, or mutate the
subject.

For validators that emit a `ConformanceReport`, version failures remain ordinary
rule results inside the existing `ConformanceReport v1.0.0` output boundary.
The report version itself is not upgraded merely because a subject references a
different specification version.

## 5. SDK release semantics

SDK/package releases and specification releases move independently:

- patch/minor SDK releases may add implementation support without changing the
  specification version;
- a new specification version requires an explicit compatibility declaration;
- a breaking SDK change is governed by the package's own release/versioning
  policy and does not silently redefine a specification contract;
- adding support for an older specification version is an explicit compatibility
  change, not an automatic consequence of semver.

The Python and TypeScript implementations expose the same compatibility model so
adopters can inspect the support boundary without duplicating it locally.

## 6. Relationship to the architecture

This policy does not create a second lifecycle or authority system. POKEE, TBV,
eco, LASSO, and other workflows remain runtime/workflow concerns. Governance
Record remains the event-oriented governance record. ConformanceReport remains
the shared validation-result boundary.
