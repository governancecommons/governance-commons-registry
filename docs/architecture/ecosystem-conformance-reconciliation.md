# Governance Commons Ecosystem Conformance Reconciliation

**Workstream:** A7  
**Status:** Reconciled against implemented repository surfaces  
**Date:** 2026-09-16

## Purpose

This records a read-only reconciliation of the implemented surfaces in the Registry, Agent Team Protocol (ATP), Agent Matrix, and Agent Project Orchestrator (APO). It identifies actual boundaries and integration gaps before new implementation work. It does not create a new runtime or authority model.

## Current implemented surfaces

| Surface | Implemented evidence | Boundary |
| --- | --- | --- |
| Capability Contract v0.1 | Registry validator, discovery, canonical adopter declaration, acceptance fixtures | Declares/discovers capability; does not grant execution authority |
| Agent Dossier | Registry structural validation; APO runtime validates dossier instances | Owns per-agent identity/profile structure |
| Agent Matrix 1.6 | Capability classes, profiles, routing rules, workflow patterns, runtime API surface | Per-agent capability/routing/identity layer |
| APO 1.1 | Runtime contract/task queue loading, typed dispatch, governance loading, telemetry, handoff envelopes | Execution/orchestration runtime |
| ATP 0.1 | Five section schemas and schema test vectors | Fleet-level delegation, trust, shared audit, escalation, lifecycle |
| Governance Record v1.0 | Registry schema and semantic governance validation | Durable governed-event record and authority/evidence evaluation |
| ConformanceReport v1.0 | Registry shared validation output | Reports validation results; does not grant authority |

## ATP schema findings

### Delegation

The delegation schema requires grant identity, task, scope, constraints, and timestamps. Propagation is limited to `none` or `single-hop`, and `max_depth` is limited to 0 or 1. The `signature` property is **optional in the JSON Schema**, while the normative ATP specification says grants must be orchestrator-countersigned before taking effect. This is a concrete structural-vs-policy gap.

Existing tests cover structural validity, required fields, propagation, depth, and additional properties. They do not yet verify signer identity, issuer-scope subset rules, expiry arithmetic, or signature validity.

### Trust topology

The schema defines root authority, trust levels, permitted delegation targets, and a chain-derivation rule. The chain rule is prose; there is no corresponding executable verifier in the current ATP repository.

### Shared audit trail

The schema defines an append-only sequence, event types, SHA-256 chaining, and signed-export metadata. The repository has schema/test coverage but no runtime audit writer/verifier implementation yet.

### Fleet escalation

The schema defines four fleet levels. Level 3 is `human_escalation`, with `auto_resume: false`. This is fleet policy; Agent Matrix remains the per-agent escalation layer.

### Team lifecycle

The schema defines formation/dissolution triggers, steps, and audit events. It is currently procedural specification rather than runtime implementation.

## Matrix ↔ APO integration

APO's implemented recommendation path loads Matrix routing rules, classifies a task into a role/category, loads the effective roster, selects ranked candidates, applies provider/agent exclusions, and returns a primary candidate with fallbacks and exclusions.

APO's runtime then separately loads its runtime contract, task queue, multi-agent governance, and effective roster before dispatch. Governance records are attached to registered agents and governance-load evidence is emitted through telemetry.

Therefore the current responsibility split is:

- **Agent Matrix:** eligibility, capability classification, and routing.
- **APO:** execution, retries, dispatch, escalation handling, and runtime telemetry.
- **ATP:** fleet-level delegation, trust, shared audit, escalation, and lifecycle semantics.

ATP should consume Matrix identity/capability/routing information rather than duplicate it.

## APO ↔ ATP integration gap

APO already emits agent-dossier-compatible handoff envelopes for peer-handoff escalation. ATP defines matching audit event types (`handoff.issued`, `handoff.accepted`, `handoff.rejected`), but there is no implemented adapter that converts APO handoff/delegation/escalation events into ATP shared-audit entries.

APO also enforces its own loaded governance/resource-budget model, while ATP defines delegation grants and fleet trust levels. No current implementation proves that an APO-issued delegation grant is checked against ATP trust topology before execution.

This is the principal integration seam.

## Registry boundary

The Registry should remain a validator/reference-contract layer. It should not absorb ATP runtime delegation, Matrix routing, or APO dispatch behavior.

Governance Record remains the durable evidence boundary for governance-significant events. ATP shared-audit entries can be represented as governed events where authority, approval, handoff, revocation, or validation relationships require governance evaluation.

ConformanceReport remains the shared validation-result boundary. It is not an authority token or execution permit.

## A7 acceptance matrix

| Concern | Current state | Required evidence |
| --- | --- | --- |
| Capability declaration/discovery | Registry implemented | No duplicate declaration model |
| Agent identity/profile | Dossier + Matrix implemented | Cross-reference only |
| Task routing | Matrix + APO implemented | Preserve Matrix ownership |
| Runtime dispatch | APO implemented | Preserve APO ownership |
| Handoff envelope | APO implemented | Bind events to ATP audit semantics |
| Delegation grant | ATP schema only | Runtime issuance + verification bridge |
| Trust-chain verification | ATP prose/schema | Executable verifier + evidence |
| Shared audit writer | ATP schema only | Runtime writer/verifier + Record mapping |
| Fleet escalation | ATP schema + APO escalation runtime | Explicit cross-spec trigger mapping |
| Fleet lifecycle | ATP schema only | Runtime formation/dissolution evidence |
| Human escalation | Matrix + ATP policy surfaces | Preserve human-required stop boundary |
| Conformance result | Registry v1.0 implemented | Reuse shared report; no ATP-specific report |

## A7 implementation boundary

A7 should **not** add ATP runtime behavior to the Registry. The next implementation slice belongs primarily to `agent-team-protocol` and should establish:

1. a real ATP validator/CLI for complete section validation;
2. CI for ATP;
3. semantic validation for delegation/trust relationships;
4. a machine-readable mapping from APO handoff/escalation events to ATP audit events;
5. an interoperability fixture proving Matrix → APO → ATP without transferring authority ownership between specs.

The Registry can then consume those established contracts through validation fixtures and the existing ConformanceReport/Governance Record boundaries.

## Architectural conclusion

The implemented ecosystem already has distinct responsibilities:

`Agent Matrix → routing/capability/identity`

`APO → execution/dispatch/runtime telemetry`

`ATP → fleet delegation/trust/shared audit/lifecycle`

`Governance Record → governed-event and authority/evidence evaluation`

`ConformanceReport → validation-result output`

The remaining work is the binding between these existing surfaces, especially APO events and ATP delegation/trust/audit semantics. That binding is the A7 implementation target.
