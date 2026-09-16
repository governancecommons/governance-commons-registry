# Workflow → Governance Record Mapping

**Status:** normative architecture guidance  
**Applies to:** Governance Commons Registry  
**Current Governance Record:** v1.0.0  
**Current Conformance Report:** v1.0.0

## Purpose

This document turns the A6.3 workflow/lifecycle reconciliation into an explicit
bridge pattern for workflows that emit Governance Record evidence.

The governing distinction remains:

> **A workflow describes how work proceeds; a Governance Record describes the
governed evidence produced as work proceeds.**

The mapping defined here is an interoperability pattern. It does not define a
new runtime, require a particular workflow engine, or make Governance Record a
workflow state machine.

## 1. Mapping boundary

A compatible workflow may be POKEE-derived, TBV-based, an eco loop, LASSO
activity, or another workflow with equivalent governance-significant events.
The workflow remains authoritative for execution state. Governance Record is
authoritative for the governed event evidence that is actually recorded.

```text
Workflow / runtime
      │
      │ executes, branches, retries, pauses, fails
      │
      ▼
Governance-significant event
      │
      │ map event + context into a record
      ▼
Governance Record v1.0.0
      │
      ├── structural validation
      ├── governance-rule evaluation
      └── provenance / relationships
      │
      ▼
ConformanceReport v1.0.0
```

The bridge is therefore **event-oriented**, not state-oriented.

A workflow state such as `running`, `waiting`, or `completed` is not itself a
Governance Record type. It becomes governance evidence only when the transition
or condition has governance significance and is represented by an appropriate
record and supporting context.

## 2. Core mapping pattern

For each governance-significant workflow event, the bridge should answer:

1. **What happened?** — select the appropriate Governance Record type.
2. **Who or what acted?** — identify the actor/subject using the applicable
   identity context.
3. **Under what authority?** — identify approval, authorization, delegation, or
   other applicable authority when required.
4. **What was the scope?** — identify the governed target, action, decision, or
   transfer scope.
5. **When did it happen?** — record the relevant event timestamp(s).
6. **Why did it happen?** — preserve intent, decision, rationale, or governing
   context where applicable.
7. **What supports the assertion?** — preserve evidence and provenance.
8. **What does it relate to?** — link prior, subsequent, parent, source, or
   resulting governed events without transferring authority.
9. **What was the result?** — record validation, conformance, completion,
   failure, rejection, cancellation, escalation, or other applicable outcome.

The bridge should map facts that already exist in the workflow. It should not
invent missing approvals, authorities, human decisions, or execution results.

## 3. Workflow stage → record-family guidance

The following table is a guidance matrix, not a mandatory sequence.

| Workflow concern | Typical Governance Record family | Evidence to preserve | Do not infer |
| --- | --- | --- | --- |
| Observation / sensing | `observation` | source, actor, timestamp, observed subject, provenance | that observation creates intent or authority |
| Framing / planning | `intent` | purpose, scope, constraints, context, provenance | that intent authorizes execution |
| Reasoning / evaluation | `decision` | decision, rationale, alternatives/evidence, actor, relations | that reasoning is approval |
| Human review / approval | `human-approval` | approving actor, decision/scope, approval outcome, timestamp, authority context | that approval proves execution |
| Authorization | `authorized-action` | authority reference, scope, actor, temporal boundaries | that authorization proves action occurred |
| Dispatch | `dispatch` | source/destination, target, scope, timestamp, governing authority | that dispatch proves completion |
| Agent/orchestrator transfer | `handoff` / `orchestrator-handoff` | transfer endpoints, delegated scope, trust boundary, authority reference, acceptance evidence | that a reference alone transfers authority |
| Escalation | `escalation` | trigger, responsible actor/recipient, reason, scope, timestamp | that escalation resolves the issue |
| Execution | `action` | action, actor, target, scope, timestamps, authority context, result/status | that completion means authorization |
| Verification / audit | `validation` | validator, subject, checks, evidence, result, timestamp | that validation grants authority or approval |
| Conformance determination | `conformance` | report/reference, evaluated subject, rule set, result | that conformance authorizes execution |
| Certification | `certification` | certifying actor/process, subject, scope, evidence, validity period | that certification is a runtime permission unless explicitly defined elsewhere |
| Registration | `registration` | registered subject, registrar/process, scope, timestamp, provenance | that registration itself grants action authority |
| Revocation | `revocation` | revoked authority/subject, effective time, reason/context, actor, provenance | that revocation rewrites earlier events |
| Provenance / evidence capture | `provenance` | source, derivation, actor/process, timestamp, evidence reference | that provenance changes ownership or authority |

A workflow may produce multiple records for one stage or one record spanning a
small number of closely related governance facts when the Governance Record
contract permits it. Conversely, internal runtime activity with no governance
significance need not produce a record.

## 4. Canonical bridge examples

### 4.1 POKEE-derived reasoning

A POKEE-derived workflow may move from observation through framing and reasoning
to action. The bridge can preserve the governance-significant evidence as:

```text
POKEE activity                    Governance evidence
─────────────                     ───────────────────
observe / signal          ─────►  observation
understand / frame        ─────►  intent
reason / evaluate        ─────►  decision
prospective gate         ─────►  human-approval / authorized-action (if required)
act                       ─────►  action
reflect / verify          ─────►  validation / conformance / provenance
```

The correspondence is semantic. A POKEE step does not dictate a record type if
the underlying event has different governance meaning.

### 4.2 TBV

For the TBV pattern:

```text
PLAN      ─────► intent / scope evidence
GENERATE  ─────► proposed artifact or action evidence
AUDIT     ─────► validation / conformance evidence
APPROVE   ─────► approval / authorization evidence
RECORD    ─────► governed event + provenance
```

The bridge preserves the verify-before-trust boundary without making TBV a
registry-defined execution lifecycle.

### 4.3 eco

For the canonical eco loop:

```text
SENSE   ─────► observation / provenance
FRAME   ─────► intent / context
THINK   ─────► decision / evidence / relations
DECIDE  ─────► decision + approval/escalation evidence where applicable
ACT     ─────► authorization / dispatch / handoff / action
RECORD  ─────► validation / conformance / certification / provenance
```

An eco iteration can emit several records. A purely internal operation can emit
none. The bridge follows governance significance rather than forcing one record
per eco stage.

### 4.4 LASSO / multi-agent work

When LASSO coordinates work across agents, the bridge should record the
cross-agent governance events that matter:

```text
LASSO coordination
      │
      ├── delegation / handoff ───► handoff evidence
      ├── approval gate ──────────► approval / authority evidence
      ├── dispatch ───────────────► dispatch evidence
      ├── governed action ────────► action evidence
      └── result / audit ─────────► validation / conformance evidence
```

LASSO remains responsible for orchestration, scheduling, workspace state,
retries, and execution. GC records and evaluates the governance evidence at the
boundary.

## 5. One workflow event may produce multiple records

The bridge must not assume a one-stage/one-record relationship.

For example, an approved agent action may legitimately produce:

```text
intent
  │
  ▼
decision
  │
  ▼
human-approval
  │
  ▼
authorized-action
  │
  ▼
dispatch
  │
  ▼
action
  │
  ▼
validation
  │
  ▼
conformance
```

These records describe different governed facts. They should be related using
the Governance Record relationship mechanism and provenance rather than merged
into a synthetic workflow-state object.

## 6. One record does not necessarily represent one workflow state

A Governance Record can capture a governed event whose surrounding workflow
contains additional operational states that are not represented in the record.

For example:

```text
runtime: queued → running → retrying → completed
                         │
                         └──── governed action record
```

The record does not need to become a mirror of the runtime's state machine. If a
retry, failure, cancellation, or escalation is itself governance-significant,
that event should be recorded separately or through the applicable record
fields and relations.

## 7. Authority and approval mapping

The bridge must preserve the distinction between these facts:

```text
approval       ≠ authorization
authorization  ≠ execution
execution      ≠ successful validation
validation     ≠ conformance certification
conformance    ≠ permission
```

When a workflow reaches an action gate, the bridge should carry forward the
applicable approval/authority evidence rather than infer it from sequence.

For temporal authority, the bridge must preserve timestamps sufficient for the
registry's governance rules to determine whether authority was active when the
governed action occurred. A later approval or earlier grant must not be silently
substituted for the authority applicable to the event being evaluated.

## 8. Handoff and delegation mapping

A workflow handoff is governance-significant when responsibility, authority, or
scope crosses an agent, process, trust boundary, or organizational boundary.

The bridge should preserve, as applicable:

- transfer source;
- transfer destination;
- delegated scope;
- handoff scope description;
- authority reference;
- delegating actor;
- trust-boundary information;
- acceptance evidence;
- acceptance timestamp; and
- relations to the originating and resulting records.

A `handoff` reference, agent identifier, or routing event alone does not
establish authority transfer.

## 9. Human intervention mapping

Human review is mapped as evidence of an actual human governance event.

Examples include:

```text
human review       ─────► human-approval / decision evidence
human rejection    ─────► decision / escalation / rejection evidence
human escalation   ─────► escalation evidence
human override     ─────► applicable decision/approval/action evidence
```

The bridge must preserve the responsible actor and relevant scope. A validator
may check that required human evidence exists; it must never manufacture the
human decision to satisfy a rule.

## 10. Failure, cancellation, and interruption

The bridge applies to unsuccessful work as well as successful work.

```text
workflow outcome
      │
      ├── completed ───► result / validation as applicable
      ├── failed ──────► failure evidence + provenance
      ├── cancelled ───► cancellation evidence + actor/context
      ├── rejected ────► decision / approval outcome evidence
      ├── escalated ───► escalation evidence
      └── interrupted ─► interruption evidence + later resume/result linkage
```

The registry must not rewrite a failed event into a successful one merely because
a later workflow attempt succeeds. Later attempts are separate governed events
linked through relations and provenance.

## 11. Minimal bridge algorithm

A workflow integration can use this conceptual procedure:

```text
1. Observe a workflow event.
2. Determine whether it has governance significance.
3. If not significant, continue runtime execution normally.
4. If significant, identify the appropriate Governance Record family.
5. Copy the event's authoritative facts and provenance into the record.
6. Add applicable actor, scope, authority, approval, timestamp, and relations.
7. Preserve failure/interruption/result information when present.
8. Validate the record structurally.
9. Evaluate applicable governance rules.
10. Emit the existing ConformanceReport v1.0.0.
11. Keep runtime state and governance result separate.
```

This procedure is a bridge pattern, not a required implementation API.

## 12. Mapping invariants

A conforming workflow bridge should preserve these invariants:

1. **Workflow state remains workflow-owned.**
2. **Governed events remain Governance Record-owned once recorded.**
3. **Record type is selected by governed meaning, not runtime state name.**
4. **Authority is explicit and temporal where applicable.**
5. **Approval is represented by evidence, not inferred from sequence.**
6. **Delegation/handoff is explicit.**
7. **References link records but do not transfer authority.**
8. **Provenance is preserved across the bridge.**
9. **Failure and interruption remain auditable events.**
10. **Human decisions remain attributable.**
11. **Validators remain side-effect free.**
12. **ConformanceReport v1.0.0 remains the validation-result boundary.**
13. **The bridge does not introduce a second runtime lifecycle.**

## 13. What this bridge does not define

This guidance does not define:

- a workflow engine;
- a scheduler;
- an agent orchestrator;
- a universal workflow state enum;
- a permission broker;
- a human approval UI;
- a replacement for POKEE, TBV, eco, or LASSO;
- a new Governance Record version;
- a new ConformanceReport version; or
- automatic authority inheritance across contracts.

Those concerns remain outside this bridge unless separately defined by an
explicit contract.

## 14. Canonical interoperability boundary

```text
POKEE / TBV / eco / LASSO / other workflow
                    │
                    │ runtime-owned activity
                    ▼
          governance-significant event
                    │
                    │ explicit bridge mapping
                    ▼
           Governance Record v1.0.0
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
   governance rules     evidence/provenance
          │                   │
          └─────────┬─────────┘
                    ▼
          ConformanceReport 1.0.0
                    │
                    ▼
           registry / audit / reuse
```

This bridge is the explicit A6.4 realization of the A6.3 lifecycle
reconciliation: workflows remain execution architectures, while Governance
Commons supplies a stable, inspectable mapping from governance-significant
workflow events to governed records and validation evidence.
