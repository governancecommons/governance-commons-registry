# Governance Commons Workflow and Lifecycle Semantics

**Status:** normative architecture guidance  
**Applies to:** Governance Commons Registry  
**Current Governance Record:** v1.0.0  
**Current Conformance Report:** v1.0.0

## Purpose

This document reconciles the registry's Governance Record model with the
workflow/lifecycle architecture from which Governance Commons originated.

Governance Commons does not define a new execution workflow here. The registry
captures and evaluates governed events produced by workflows and runtimes that
may use established POKEE, TBV, eco, LASSO, or other compatible methods.

The governing distinction is:

> **A workflow describes how work proceeds; a Governance Record describes the
governed evidence produced as work proceeds.**

The registry therefore provides a governance/evidence layer over workflows,
not a replacement for them.

## Architectural lineage

The applicable lineage is:

```text
POKEE
  │
  ▼
TBV
  │
  ▼
Governance Commons
  │
  ├──────────────► eco
  │
  └──────────────► LASSO
```

POKEE supplies the reusable cognitive/workflow pattern. TBV applies that
pattern to a verify-before-trust workflow. Governance Commons adds explicit
authority, evidence, provenance, approval, audit, and conformance boundaries.
eco and LASSO provide broader workflow and agent-operation environments in
which governed work can occur.

These systems are related but are not interchangeable contracts. GC must not
copy runtime semantics from eco or LASSO into the registry merely to make the
registry appear complete.

## Workflow versus governance lifecycle

A workflow may have its own states, stages, loops, retries, branching, and
terminal conditions. Those are execution concerns.

GC defines a smaller governance lifecycle that can observe and constrain
relevant workflow transitions:

```text
                 WORKFLOW / RUNTIME
                        │
        ┌───────────────┴────────────────┐
        │                                │
        ▼                                ▼
   work progresses                 governance gate
        │                                │
        └───────────────┬────────────────┘
                        ▼
                 governed event
                        │
                        ▼
                Governance Record
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
        governance rules      provenance/evidence
              │                   │
              └─────────┬─────────┘
                        ▼
               ConformanceReport
```

A workflow stage does not automatically become a Governance Record. A record
is warranted when an event has governance significance, such as an intent,
decision, approval, dispatch, handoff, action, escalation, validation,
conformance result, certification, registration, revocation, or provenance
event.

## Canonical governance lifecycle

The registry recognizes the following conceptual progression without requiring
every workflow to instantiate every stage:

```text
OBSERVE
   │
   ▼
INTEND
   │
   ▼
DECIDE
   │
   ├──────────────► ESCALATE
   │
   ▼
APPROVE / AUTHORIZE
   │
   ▼
DISPATCH / HANDOFF
   │
   ▼
ACT
   │
   ▼
VALIDATE
   │
   ▼
CONFORM / CERTIFY / RECORD
```

This is a governance evidence model, not a mandatory runtime state machine.
Workflows may omit stages, repeat stages, branch, pause, fail, cancel, or
return to earlier reasoning. The Governance Record captures the events that
matter rather than forcing the runtime into a fixed sequence.

## Relationship to POKEE

The POKEE pattern is treated as the reusable reasoning/workflow ancestor rather
than a competing GC lifecycle.

The following correspondence is intentionally semantic rather than a strict
one-to-one mapping:

| POKEE concern | GC governance concern |
| --- | --- |
| Signal / observation | `observation` record and provenance/evidence |
| Understanding / framing | intent and contextual evidence |
| Reasoning / evaluation | decision evidence and relations |
| Prospective evaluation | approval/authority gates where required |
| Action | `action` record and applicable authority |
| Reflection / result | validation, conformance, provenance, and subsequent records |

GC does not claim that these terms are identical. The mapping exists so that a
POKEE-derived workflow can emit governed evidence without adopting a second,
unrelated conceptual architecture.

## Relationship to TBV

TBV is treated as a governance-oriented workflow profile derived from POKEE.
Its familiar progression can be represented as:

```text
PLAN → GENERATE → AUDIT → APPROVE → RECORD
```

Within GC, these are workflow activities rather than new registry contracts.
The governance significance is represented by the evidence produced around
those activities:

- **PLAN** may produce intent and scope evidence.
- **GENERATE** may produce an artifact/action proposal.
- **AUDIT** may produce validation or conformance evidence.
- **APPROVE** may produce an approval record and establish the required
  authorization evidence.
- **RECORD** persists the resulting governed event and provenance.

TBV's exact execution implementation remains outside the registry.

## Relationship to eco

The eco canonical loop is:

```text
SENSE → FRAME → THINK → DECIDE → ACT → RECORD
```

GC can overlay governance evidence on this loop without replacing it:

| eco stage | Typical GC evidence |
| --- | --- |
| SENSE | observation, provenance |
| FRAME | intent, framework/governance context |
| THINK | decision context, relations, evidence |
| DECIDE | decision, approval requirement, escalation |
| ACT | authorization, dispatch, handoff, action |
| RECORD | validation, conformance, certification, provenance |

This mapping is deliberately non-prescriptive. A runtime may emit several
records during one eco stage, or no registry record for an internal operation
that has no governance significance.

## Relationship to LASSO

LASSO is a workspace/reasoning and multi-agent operating environment, not a
Governance Record validator.

When LASSO performs governed work, the registry boundary is:

```text
LASSO executes / coordinates work
             │
             ▼
      governed event occurs
             │
             ▼
      Governance Record
             │
             ▼
      GC governance rules
```

The registry may record dispatch, delegation, handoff, approval, authority,
escalation, action, validation, and provenance associated with LASSO activity.
It must not assume responsibility for LASSO scheduling, agent execution,
workspace state, retries, tool invocation, or orchestration.

## Lifecycle state and record status are different

A critical boundary is maintained between:

1. **workflow state** — what the runtime says is happening;
2. **record type** — what kind of governed event was recorded; and
3. **governance status** — whether the relevant governed condition is satisfied.

For example, `action.status = "completed"` is an assertion about the recorded
action event. It does not itself establish that the action was authorized.
The existing governance rules separately evaluate authority, approval, and
temporal constraints.

Likewise, `handoff.status = "accepted"` does not by itself establish a valid
authority transfer. The governance-rule layer requires explicit transfer,
scope, trust-boundary, authority, and acceptance information.

## Transition evidence

When a governed transition matters, the record should make the transition
inspectable through explicit fields and relations rather than relying on an
implicit state machine.

The preferred evidence pattern is:

```text
prior context
    │
    ▼
current governed event
    │
    ├── actor
    ├── authority / approval
    ├── timestamps
    ├── scope / target
    ├── relations
    └── provenance
    │
    ▼
result / next governed event
```

`relations` provide linkage between records without transferring ownership or
authority. References remain references.

## Human governance

Human intervention is a governance event, not merely an implementation detail.
Where a workflow requires human approval, rejection, escalation, override, or
other intervention, the resulting evidence should identify the responsible
actor and applicable scope through Governance Records.

A validator may determine whether the required evidence exists and whether it
satisfies the applicable rule. It does not impersonate the human actor or
create approval as a side effect.

## Failure, cancellation, and interruption

Governance evidence must remain meaningful when work does not complete.

A workflow may terminate as:

- completed;
- failed;
- cancelled;
- rejected;
- escalated; or
- interrupted and resumed later.

The registry does not require a successful terminal state. Failed or cancelled
actions can still be governed events and can still require provenance,
authority, validation, or subsequent remediation records.

This is why workflow lifecycle state must not be collapsed into a single
`lifecycle.status` interpretation for the entire Governance Record contract.
The existing record-specific fields and relations carry the stronger semantic
meaning.

## Governance gates versus execution transitions

A governance gate answers a question such as:

> Is the evidence sufficient for this transition to be considered authorized,
approved, accepted, or conformant?

An execution transition answers a different question:

> Should the runtime move from one operational state to another?

GC governs the first question. Runtime systems govern the second.

A conformant Governance Record therefore does not command execution, and a
runtime transition does not automatically establish governance conformance.

## Reusable lifecycle contract pattern

GC-adjacent workflows should be describable using the following reusable
contract vocabulary when useful:

| Element | Meaning |
| --- | --- |
| Purpose | Why the workflow exists |
| Inputs | Required starting information/artifacts |
| Preconditions | Conditions required before progression |
| Stage | Current workflow activity |
| Transition | Movement between workflow activities |
| Action | Concrete operation performed or proposed |
| Decision | Deliberate choice and its rationale/outcome |
| Gate | Condition requiring verification or approval |
| Authority | Applicable permission and temporal scope |
| Evidence | Facts/artifacts supporting the event |
| Provenance | Where/how the evidence or event originated |
| Record | Durable governed event representation |
| Verification | Validation/audit of evidence or result |
| Failure | Non-success terminal or intermediate condition |
| Human intervention | Required or recorded human decision/action |

This vocabulary is intentionally a contract pattern, not a runtime API.
Different workflow systems may implement it differently while emitting GC
compatible governance evidence.

## Rules for lifecycle interoperability

1. **Do not invent a second runtime lifecycle.** GC overlays governance on
   established workflows.
2. **Do not require every record type in every workflow.** Emit records for
governance-significant events.
3. **Do not infer authority from sequence alone.** An action following an
   approval-looking event still requires applicable authority and scope.
4. **Do not infer approval from conformance.** Validation reports remain reports.
5. **Do not infer execution from authorization.** Authorization permits a
   governed action; it does not prove completion.
6. **Do not infer delegation from a handoff reference.** Authority transfer
   remains explicit.
7. **Use timestamps and relations for event ordering.** Do not create a hidden
   global state machine inside the registry.
8. **Preserve failure and interruption evidence.** Governance applies to
   unsuccessful work as well as successful work.
9. **Keep human decisions attributable.** Human approval or intervention must
   remain represented as evidence, not simulated by a validator.
10. **Keep ConformanceReport stable.** Lifecycle additions must not fork the
    shared report contract.
11. **Keep validators side-effect free.** Validation reports on the governed
    evidence; it does not execute or alter the workflow.

## Canonical boundary

The resulting architecture is:

```text
     POKEE / TBV / eco / LASSO / other workflow
                         │
                         │ executes work
                         ▼
                  governed event(s)
                         │
                         ▼
                Governance Record
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       governance rules       evidence/provenance
              │                     │
              └──────────┬──────────┘
                         ▼
              ConformanceReport 1.0.0
                         │
                         ▼
              registry / audit / reuse
```

This is the A6.3 lifecycle reconciliation boundary. It connects GC to the
workflow architecture that produced it while preserving the registry's role as
contract, evidence, validation, and governance infrastructure.
