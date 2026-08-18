# governance-commons

**Alpha.** Reference implementation of Governance Commons standards:
machine-checkable naming rules, capability-contract discovery, and conformance
reporting.

The Python v0.2.0 package validates **ONS (Ontic Namespace Structure)** and
**Capability Contract v0.1** declarations. The npm package remains ONS-only in
this MVP.
Agent Dossier, Agent Matrix, and Agent Project Orchestrator validation
are planned but not implemented yet — `--spec` currently accepts `ons`
only.

## Install

```bash
pip install governance-commons
# or
npm install governance-commons
```

## Quickstart

`manifest.json`:

```json
{
  "checks": [
    { "domain": "python_identifier", "name": "run_intent" },
    { "domain": "governance_cluster", "name": "ONS" }
  ]
}
```

```bash
gc-validate --spec ons manifest.json
```

```text
GC Conformance Report
  Spec:    ons 1.4.0 (standard profile)
  Subject: manifest.json
  Result:  PASS

  + [ONS-CASING-001] Python identifiers must be snake_case
  + [ONS-CASING-006] Cluster names must be 2–6 uppercase ASCII letters

  Summary: 2 passed, 0 failed, 0 skipped of 2 total
```

Add `--output json` to get the same report as structured JSON, or save
it and inspect it later with `gc-report <file>`.

Validate and discover capability declarations:

```bash
gc-validate --spec capabilities .governance/contracts/capabilities.yaml
gc-discover --capability asset.palette.generate ../niji ../another-repo
```

Discovery validates every contract it reads and reports invalid declarations.
It does not evaluate or grant execution authority.

## Packages

- Python package: `governance-commons` — CLI commands `gc-validate`, `gc-report`, `gc-discover`
- npm package: `governance-commons` — CLI commands `gc-validate`, `gc-report`

## Development

```powershell
python -m pytest -q
npm test
python -m build
npm pack --dry-run
```

## Project Shape

This directory is the SDK/reference-implementation repo. VS Code extensions should live in separate repos, such as `agent-dossier-vscode` or `governance-commons-vscode`.
