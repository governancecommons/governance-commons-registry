# Governance Commons adopter examples

These examples are intentionally small and use the public SDK surfaces already
implemented in this repository. They demonstrate validation and reporting
without introducing a runtime, workflow engine, or new contract.

## Python

### Governance Record validation

`python/governance_record_validation.py` shows the registry-side boundary for a
governed event:

1. a workflow/runtime produces a governance-significant event;
2. the event is represented as an existing Governance Record;
3. the registry validates the record structurally and semantically; and
4. the result is emitted through the existing ConformanceReport v1.0.0 contract.

Run it from the repository root:

```bash
python examples/python/governance_record_validation.py
```

The example intentionally validates an existing representative fixture rather
than defining a second record schema.

### Capability declaration validation

`python/capability_validation.py` demonstrates Capability Contract v0.1
validation. Capability declaration/discovery is not authorization; the example
only validates the declaration and prints the shared conformance result.

```bash
python examples/python/capability_validation.py
```

## TypeScript

### ONS validation and shared report

`typescript/ons_validation.ts` demonstrates the current npm/TypeScript surface:
ONS validation plus the shared ConformanceReport builder.

The repository's normal build remains authoritative for package output. The
example is source-level usage intended for adopters to copy into their own
TypeScript project.

## Architecture boundary

The examples follow the same boundary documented by the registry:

```text
POKEE / TBV / eco / LASSO / other workflow
                    |
                    | runtime-owned activity
                    v
          governance-significant event
                    |
                    v
           Governance Record v1.0.0
                    |
                    v
          ConformanceReport v1.0.0
```

Validation does not execute the workflow, grant authority, manufacture approval,
or mutate the governed subject.
