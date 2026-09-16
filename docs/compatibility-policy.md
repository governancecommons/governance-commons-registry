# Governance Commons SDK Compatibility Policy

**GC-SDK.05**  
**Status:** normative for the current reference implementation  
**Updated:** 2026-09-16

## 1. Scope

This policy defines how the reference SDK relates its release versions to the
Governance Commons specification versions it validates.

The current repository declares these versions:

| Surface | Current specification | Python SDK | npm SDK |
| --- | --- | --- | --- |
| ONS | 1.4.0 | 0.2.0 | 0.1.1 |
| Capability Contract | 0.1 | 0.2.0 | 0.1.1 |
| Agent Dossier instance | 1.4.0 | 0.2.0 | 0.1.1 |
| Governance Record | 1.0.0 | 0.2.0 | 0.1.1 |
| ConformanceReport | 1.0.0 | 0.2.0 | 0.1.1 |

These numbers are deliberately not coupled. An SDK/package release number does
**not** imply a specification version. Compatibility is determined by the
explicit specification version supported by the validator.

## 2. Version rules

For stable specifications (major version >= 1):

- The current declared version is supported.
- An older version within the same major version is **version-compatible**.
- A version from an older major is **incompatible**.
- A newer version than the validator's supported version is **unsupported
  future**.

For pre-1.0 specifications:

- The minor version is the compatibility boundary.
- The current 0.x minor is supported.
- Older patch releases in that same 0.x minor are version-compatible.
- A different 0.x minor is incompatible when older and unsupported future when
  newer.
- This follows the repository's existing use of Capability Contract `0.1` and
  does not assume that a future `0.2` contract is compatible.

Malformed version strings and unknown specification identifiers are explicit
errors. They are never coerced into a supported version.

## 3. Compatibility is not schema fallback

A version-compatible classification does **not** authorize a validator to use
a newer schema silently. The validator remains bound to the schema/specification
version it was built against.

Before an older specification is actually validated, backward compatibility of
the relevant schema and semantic rules must be established explicitly. Until
that evidence exists, the compatibility classifier is advisory metadata and
must not be interpreted as proof that every historical instance can be
validated by the current schema.

A future specification version is never silently downgraded to the current
schema.

## 4. SDK/package version relationship

Python and npm packages may release at different version numbers because they
are independently packaged surfaces. Their package versions identify SDK
releases; they do not identify the specification being validated.

A package release MUST document the specification versions it supports. A
package version change alone MUST NOT be used as an implicit compatibility
claim for a specification.

The current reference implementation exposes one explicit registry of the
specification versions its Python validators are built against:
`governance_commons.compatibility.SUPPORTED_SPEC_VERSIONS`.

## 5. Validation and reporting boundary

Compatibility evaluation is deterministic and side-effect free. The helper
returns a `RuleResult` using the same rule-result shape used by the shared
`ConformanceReport v1.0.0` contract.

Compatibility failures MUST remain distinguishable from ordinary schema or
semantic validation failures. The compatibility rule ID is:

`GC-SDK-COMPAT-001`

The policy does not create a second report format, execute workflow actions,
grant authority, or mutate the subject.

## 6. Required behavior

Implementations following this policy MUST:

1. identify the specification explicitly;
2. parse and validate its declared version;
3. distinguish current, older-compatible, older-incompatible, future, invalid,
   and unknown cases;
4. never silently substitute another schema or specification version; and
5. preserve the existing ConformanceReport output boundary when compatibility
   results are included in validation output.
