# Governance Commons Ecosystem Conformance Reconciliation

**Workstream:** A7  
**Status:** Implemented seam reconciled against current repository surfaces  
**Date:** 2026-09-16

## Purpose

This records the cross-spec reconciliation of the Registry, Agent Team Protocol (ATP), Agent Matrix, and Agent Project Orchestrator (APO). It records actual implementation boundaries and the executable A7 evidence seam. It does not create a new runtime or authority model.

## Current implemented surfaces

| Surface | Implemented evidence | Boundary |
| --- | --- | --- |
| Capability Contract v0.1 | Registry validator, discovery, canonical adopter declaration, acceptance fixtures | Declares/discovers capability; does not grant execution authority |
| Agent Dossier | Registry structural validation; APO runtime validates dossier instances | Owns per-agent identity/profile structure |
| Agent Matrix 1.6 | Capability classes, profiles, routing rules, workflow patterns, runtime API surface | Per-agent capability/routing/identity layer |
| APO 1.1 | Runtime contract/task queue loading, typed dispatch, governance loading, telemetry, handoff envelopes | Execution/orchestration runtime |
| ATP 0.1 | Five section schemas, semantic delegation/trust bridge, shared-audit writer/verifier, APO event adapter, delegation lifecycle evidence checker | Fleet-level delegation, trust, shared audit, escalation, lifecycle |
| Governance Record v1.0 | Registry schema and semantic governance validation, including authority/revocation evidence rules | Durable governed-event record and authority/evidence evaluation |
| ConformanceReport v1.0 | Registry shared validation output | Reports validation results; does not grant authority |

## ATP delegation and trust

The delegation schema now requires the orchestrator countersignature structurally. The ATP semantic conformance bridge validates issuer/recipient trust levels, delegation depth, scope subset, grant interval arithmetic, propagation/depth consistency, root authority constraints, and root-backed delegation for non-root issuers.

The remaining cryptographic trust operation is intentionally not reproduced in the Registry: ATP owns delegation/trust semantics, while the Registry records and evaluates durable governance evidence.

## ATP shared audit and APO binding

ATP now provides an append-only shared-audit writer and hash-chain verifier. `append_apo_event()` maps the current APO telemetry vocabulary into registered ATP audit events, including task start/completion/failure, handoff issuance/acceptance/rejection, and escalation. Unknown APO event types fail closed.

This establishes the runtime-event translation boundary without moving runtime ownership: APO continues to own dispatch, handoff, escalation, and telemetry; ATP owns fleet-level audit translation and chain integrity.

## Delegation lifecycle / revocation evidence

ATP now provides a reference lifecycle checker for one delegation. The executable evidence model is:

`delegation.granted → governed use evidence → delegation.revoked`

with expiry and task completion acting as additional terminal boundaries. The checker rejects missing grant evidence, invalid grant intervals, missing countersignature evidence, use before issuance, use at/after expiry, use after revocation, task-bound use after completion, duplicate revocations, and revocation before issuance.

The Registry separately evaluates Governance Record evidence. `GR-AUTH-003` requires a revocation record to identify an authority, contain a matching `revokes` relation, and preserve `timestamps.occurred_at`. `GR-AUTH-002` rejects action evidence occurring after `authority.revoked_at`. This is the intended cross-spec separation rather than duplicated runtime authority state.

## Matrix ↔ APO integration

APO's recommendation path loads Matrix routing rules, classifies a task into a role/category, loads the effective roster, selects ranked candidates, applies provider/agent exclusions, and returns a primary candidate with fallbacks and exclusions.

APO then separately loads its runtime contract, task queue, multi-agent governance, and effective roster before dispatch. Governance records are attached to registered agents and governance-load evidence is emitted through telemetry.

Therefore the responsibility split remains:

- **Agent Matrix:** eligibility, capability classification, routing, identity/profile context.
- **APO:** execution, retries, dispatch, escalation handling, handoff, runtime telemetry.
- **ATP:** fleet-level delegation, trust, shared audit, escalation, lifecycle semantics.
- **Governance Record:** durable governed-event and authority/evidence evaluation.

## A7 acceptance matrix — reconciled

| Concern | Current state | Boundary/evidence |
| --- | --- | --- |
| Capability declaration/discovery | Implemented | Registry owns declaration/discovery |
| Agent identity/profile | Implemented | Dossier + Matrix; cross-reference only |
| Task routing | Implemented | Matrix owns routing; APO consumes it |
| Runtime dispatch | Implemented | APO owns execution/dispatch |
| Handoff envelope | Implemented | APO envelope → ATP audit mapping |
| Delegation grant | Implemented | ATP schema + semantic conformance; no Registry runtime |
| Trust-chain verification | Implemented | ATP semantic verifier; no duplicate Registry trust engine |
| Shared audit writer | Implemented | ATP hash-chain writer/verifier + APO event bridge |
| Fleet escalation | Spec + runtime surfaces | ATP policy + APO escalation; explicit event mapping |
| Fleet lifecycle | Schema/procedural surface | Runtime implementation remains ATP work, not a Registry gap |
| Delegation revocation evidence | Implemented | ATP lifecycle checker + GC `GR-AUTH-002/003` |
| Human escalation | Implemented policy surfaces | Preserve human-required stop boundary |
| Conformance result | Implemented | Registry v1.0 shared report; no ATP-specific report |

## A7 implementation boundary

The A7 integration gaps identified by the original reconciliation are now closed at the evidence seam:

1. ATP has executable delegation/trust semantic checks.
2. ATP has the shared-audit writer/verifier and APO event mapping bridge.
3. ATP has executable delegation lifecycle/revocation evidence checks.
4. Registry has the corresponding Governance Record revocation/effective-time rules and representative fixtures.
5. The cross-spec ownership boundary remains explicit: Matrix → APO → ATP → Governance Record/ConformanceReport.

ATP's remaining CLI/reference-runtime release work is ordinary ATP Phase 1/2 work and is not an A7 Registry implementation gap. Matrix's unrelated backlog items likewise remain in Matrix's own workstream.

## Phase B reconciliation

The implementation boundary for the next phase is therefore **integration and conformance consumption**, not another governance runtime. Phase B should consume the established contracts and fixtures, prove the Matrix → APO → ATP event path, and terminate the evidence chain at Governance Record/ConformanceReport. Any implementation that introduces a second authority store, duplicates Matrix routing, or moves dispatch ownership into ATP/Registry would violate the reconciled boundary.

## Architectural conclusion

`Agent Matrix → routing/capability/identity`

`APO → execution/dispatch/runtime telemetry/handoff`

`ATP → fleet delegation/trust/shared audit/lifecycle`

`Governance Record → governed-event and authority/evidence evaluation`

`ConformanceReport → validation-result output`

A7 is now an interoperability/evidence boundary rather than an invitation to build a universal governance runtime. The remaining work is to consume and test this boundary across repositories, not to duplicate it.
