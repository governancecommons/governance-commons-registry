# Delegation Lifecycle and Revocation Evidence

**Workstream:** A7  
**Status:** evidence boundary implemented in Governance Record validation  
**Date:** 2026-09-16

## Purpose

This document defines the Registry-side evidence boundary for delegated authority
without introducing a new delegation runtime or a second authority model.

ATP remains the owner of delegation issuance, trust-chain verification, and fleet
runtime semantics. APO remains the owner of execution and dispatch. The Registry
records and evaluates the durable governance evidence produced by those systems.

## Lifecycle evidence

A delegation lifecycle is represented as a sequence of governed events rather
than a new `delegation` record type:

1. **Grant evidence** — an action or handoff carries an `authority` reference,
   including `authority_id`, `status`, and `granted_at` when temporal evaluation
   is required.
2. **Use evidence** — the governed action records `timestamps.occurred_at` so
   the action can be evaluated against the authority's effective interval.
3. **Revocation evidence** — a `record_type: revocation` record identifies the
   authority as its `subject` and contains a `relations` entry of type `revokes`
   targeting that same authority.
4. **Post-revocation enforcement evidence** — an action using a revoked authority
   must carry a valid `revoked_at` timestamp, and an action occurring after that
   timestamp fails `GR-AUTH-002`.

This keeps lifecycle state, durable evidence, and execution behavior separate.

## Revocation rule

`GR-AUTH-003` is the Registry-side evidence check for revocation records. It
requires:

- `subject.type == "authority"`;
- a non-empty authority subject identifier;
- a `revokes` relation targeting the same authority identifier; and
- a valid `timestamps.occurred_at` value.

The rule does not decide whether the actor was permitted to revoke the authority;
that is an authority/authorization question evaluated by the surrounding
Governance Record and owning protocol semantics.

## Cross-spec binding

The intended event flow is:

`Matrix eligibility → APO dispatch/handoff → ATP delegation/trust event → Governance Record evidence`

The Registry consumes the resulting evidence. It does not issue grants, execute
revocations, perform fleet trust traversal, or write ATP's runtime audit log.

## Acceptance evidence

The representative A5 fixture set now includes:

- a valid revocation record with a matching `revokes` relation;
- a semantic-negative revocation record whose relation targets a different
  authority; and
- the existing temporal negative fixture proving that an action after
  `revoked_at` is rejected by `GR-AUTH-002`.

Together these establish the Registry-side evidence boundary needed for the
A7 interoperability seam without claiming implementation of ATP runtime
behavior.
