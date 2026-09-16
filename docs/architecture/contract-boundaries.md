# Governance Commons Contract Boundaries

**Status:** normative architecture guidance  
**Applies to:** Governance Commons Registry  
**Current Governance Record:** v1.0.0  
**Current Conformance Report:** v1.0.0

## Purpose

This document defines the authority boundaries between the registry's implemented
contracts. It prevents individual validators from becoming a single, implicit
governance engine and establishes which artifact is authoritative for each kind
of fact.

The registry contains distinct contracts with distinct responsibilities:

- **ONS** defines naming and identifier conformance.
- **Capability Contract** defines declared capabilities and provider/interface
  relationships; it does not grant execution authority.
- **Agent Dossier** defines the structural identity/profile of an agent
  instance; it does not itself authorize an action.
- **Governance Record** records governed events, decisions, authority, actions,
  transitions, validation, and related provenance.
- **ConformanceReport** is the shared machine-readable result boundary for
  validation; it reports a validator's result and does not become the governed
  subject itself.

## Authority model

| Contract | Owns / establishes | May reference | Must not establish |
| --- | --- | --- | --- |
| ONS | Naming rules, identifier form, namespace conventions | IDs used by other contracts | Agent authority, capability grants, approvals, execution decisions |
| Capability Contract | Declared capability, provider, interface, version and conflict semantics | Agent/provider identifiers, interfaces, ONS-conformant identifiers where applicable | Permission to execute, human approval, delegation, runtime success |
| Agent Dossier | Agent identity/profile and dossier-instance structure | Agent IDs, capabilities, metadata, provenance | Authorization to act, approval, delegation, conformance of unrelated artifacts |
| Governance Record | Governed event record, authority state, approval, action, handoff, validation and relationships | ONS IDs, capability/dossier references, validation/conformance evidence | Redefinition of another contract's structural schema |
| ConformanceReport | Validation result, rule outcomes, summary and conformance level | Subject/spec identifiers | Authority, approval, execution, mutation of the subject |

## Relationship rules

### 1. ONS is foundational naming infrastructure

ONS validation answers whether a supplied name or identifier conforms to the
applicable naming rule. A conformant identifier is not thereby authorized,
registered, trusted, executable, or approved.

Other contracts may use ONS-defined identifiers. They remain responsible for
their own semantics.

### 2. Capability declarations describe possibility, not permission

A Capability Contract can establish that a capability is declared, provided,
prohibited, versioned, or associated with an interface/provider. Discovery may
locate declarations and report their validity.

Capability discovery and validation **must not** infer or grant execution
authority. Authorization belongs to the governance layer and must be represented
by applicable Governance Record evidence.

### 3. Agent Dossier establishes identity/profile structure

An Agent Dossier instance can establish the structured identity and declared
profile of an agent. Structural validity of a dossier does not authorize that
agent to perform an action.

A dossier may be referenced by a Governance Record as the identity/profile
context for an actor, delegate, approver, orchestrator, or other subject. The
reference does not transfer authority by itself.

### 4. Governance Record is the governed-event record layer

Governance Record v1.0.0 records the facts and relationships needed to represent
governed events, including intent, decision, approval, authority, action,
dispatch, handoff, escalation, validation, conformance, certification,
registration, revocation, and provenance.

Governance Record validation has two ordered boundaries:

```text
Governance Record
      |
      v
Structural validation (JSON Schema)
      |
      +-- invalid --> reject / no semantic governance evaluation
      |
      v
Governance rules
      |
      +-- non-conformant --> governed record is structurally valid but
      |                       violates an applicable governance rule
      |
      +-- conformant --> governance rules satisfied
```

The governance-rule layer may evaluate relationships among fields and referenced
facts, but it must not silently replace the underlying contract schemas.

### 5. ConformanceReport is the output boundary

Every validator reports through the shared **ConformanceReport v1.0.0**
contract. The report answers:

> What validation rules were evaluated against this subject, and what was the
> resulting conformance state?

The report does **not** grant authority, approve actions, mutate the subject,
or become an authorization record.

Governance Records may reference a conformance report or represent a conformance
event, but the Governance Record schema must not duplicate or fork the
ConformanceReport contract.

## Cross-contract authority rules

1. **Structural validity is not authorization.**
2. **Declaration is not permission.** A capability declaration does not grant
   execution authority.
3. **Identity is not authority.** An Agent Dossier does not authorize its agent.
4. **Conformance is not approval.** A passing validation report does not approve
   an action.
5. **Approval is not execution.** Approval permits a governed action only within
   its applicable scope and authority conditions; it does not assert that the
   action occurred successfully.
6. **Authority is temporal.** When authority has grant/revocation boundaries,
   action occurrence time must be evaluated against those boundaries.
7. **Delegation is explicit.** A handoff or delegation must identify the
   transfer, delegated scope, authority reference, and applicable trust boundary
   rather than inferring them from agent identity alone.
8. **References do not transfer ownership.** Referencing an ONS ID, capability,
   dossier, or report does not transfer that artifact's authority into the
   referencing contract.
9. **Validators report; they do not execute.** Validation and discovery must not
   silently perform the action being described or authorize it as a side effect.
10. **The shared report contract remains stable.** Individual spec evolution must
    not create incompatible report formats without an explicit report-contract
    version change.

## Validation responsibility matrix

| Question | Authoritative layer |
| --- | --- |
| Is this identifier/name structurally compliant with ONS? | ONS validator |
| Is this capability declaration structurally/semantically valid? | Capability Contract validator |
| Which declared providers match an exact capability query? | Capability discovery |
| Is this agent dossier instance structurally valid? | Agent Dossier validator |
| Is this governed record structurally valid? | Governance Record JSON Schema |
| Does an otherwise valid record satisfy GC governance rules? | Governance Record governance-rule validator |
| What was the machine-readable validation result? | ConformanceReport v1.0.0 |
| Was an action authorized/approved within applicable authority and time? | Governance Record + applicable governance rules |

## Non-responsibilities

The registry currently does **not** treat any of these contracts as a runtime
executor, agent orchestrator, permission broker, identity provider, or policy
decision-maker.

In particular:

- `gc-validate` validates and reports; it does not execute the subject.
- `gc-discover` discovers declarations; it does not grant authority.
- A passing ConformanceReport does not create authorization.
- A valid Agent Dossier does not create authorization.
- A valid Capability Contract does not create authorization.
- ONS conformance does not create authorization.

Runtime execution, orchestration, human approval workflows, and external policy
decisions remain outside these contract validators unless explicitly represented
as governed events and evaluated by the applicable governance rules.

## Architectural consequence

The registry should evolve by adding explicit contracts and explicit bridges,
not by expanding one validator until it owns every concern.

The intended dependency direction is:

```text
                   ConformanceReport 1.0.0
                    (shared output boundary)
                              ^
                              |
        +---------------------+---------------------+
        |                     |                     |
       ONS              Capability Contract    Agent Dossier
        |                     |                     |
        +---------------------+---------------------+
                              |
                       referenced context
                              |
                              v
                    Governance Record 1.0.0
                              |
                              v
                    Governance Rules
```

The arrows above describe information/validation relationships, not authority
inheritance. No lower contract automatically grants authority to a higher one.

## Versioning rule

A change that alters a contract's own structural or semantic meaning requires
that contract's versioning process. A change to the shared ConformanceReport
shape requires an explicit ConformanceReport version change and coordinated
consumer updates.

Adding a new Governance Record governance rule does not by itself change the
ConformanceReport version or another specification's version; it changes the
set of rules evaluated by the Governance Record validator and must be covered by
fixtures/tests.
