# Capability Contract v0.1 Adoption

**Status:** active  
**Workstream:** GC-SDK.07

## Purpose

This document defines the repository-level adoption pattern for Capability
Contract v0.1. Adoption uses the existing contract directly; it does not add a
second manifest, schema, registry database, execution runtime, or authority
model.

## Canonical location

An adopter places its declaration at:

```text
.governance/contracts/capabilities.yaml
```

The registry recognizes that path through `CAPABILITY_RELATIVE_PATH` and can
validate it with the public Python SDK or discover it from an explicit
repository root.

## Adoption profiles

An adopter may use any of these profiles:

- **Provider:** declares capabilities under `provides`.
- **Consumer:** declares dependencies under `consumes`.
- **Hybrid:** declares both provided and consumed capabilities.
- **Boundary:** may use `prohibits` to document capabilities that remain
  intentionally outside the component boundary.

`provides`, `consumes`, and `prohibits` are declarations. They do not grant
execution authority, create approvals, or authorize a caller.

## Recommended CI gate

A repository adopting the contract should validate its declaration before
merging changes that modify the contract:

```bash
gc-validate --spec capabilities .governance/contracts/capabilities.yaml
```

For provider discovery across explicitly selected repositories:

```bash
gc-discover --capability asset.palette.generate ./provider-a ./provider-b
```

The discovery result identifies validated providers and explicitly reports that
authority is not evaluated. Authorization and governed action remain outside
Capability Contract discovery.

## Version boundary

The declaration uses `schema_version: "0.1"`. The SDK/package version and the
Capability Contract specification version are independent. A future contract
version must be handled through the repository compatibility policy rather than
silently interpreted as v0.1.

## Acceptance coverage

GC-SDK.07 acceptance covers:

1. the registry's own canonical declaration;
2. provider-only adoption;
3. consumer-only adoption;
4. provider + consumer adoption;
5. prohibited-boundary declarations;
6. semantic rejection of a capability that is both provided and prohibited;
7. multi-provider discovery with deterministic ordering; and
8. explicit preservation of the non-authority boundary.

Representative fixtures live under `tests/fixtures/capability-adoption/`.

## Architecture boundary

The adoption pattern remains consistent with the existing GC architecture:

```text
workflow/runtime
      |
      | activity
      v
capability declaration / discovery
      |
      | declaration is validated
      v
ConformanceReport / validation result

Governance Record owns governed events and authority evaluation.
```

The SDK validates and reports. It does not execute workflows, mutate subjects,
manufacture approval, or grant authority.
