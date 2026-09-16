# governance-commons

**Alpha.** Reference implementation of Governance Commons standards:
machine-checkable naming rules, capability-contract discovery, governance-record
validation, conformance reporting, and specification compatibility utilities.

## SDK 0.2.0

The current Python and npm package line is **0.2.0**. The two language surfaces
are intentionally not identical:

- **Python 0.2.0** provides ONS v1.4.0, Capability Contract v0.1, Agent Dossier
  v1.4.0 structural validation, Governance Record v1.0.0 validation, shared
  ConformanceReport v1.0.0, compatibility classification, and the
  `gc-validate`, `gc-report`, and `gc-discover` CLIs.
- **npm 0.2.0** retains the ONS/report-focused TypeScript/JavaScript surface:
  root exports plus `./ons` and `./report`, with `gc-validate` and `gc-report`
  CLI commands.

TypeScript parity for Capability Contract, Agent Dossier, and Governance Record
is not claimed by this release.

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

Add `--output json` to get the same report as structured JSON, or save it and
inspect it later with `gc-report <file>`.

Validate and discover capability declarations with the Python SDK:

```bash
gc-validate --spec capabilities .governance/contracts/capabilities.yaml
gc-discover --capability asset.palette.generate ../niji ../another-repo
```

Discovery validates every contract it reads and reports invalid declarations.
It does not evaluate or grant execution authority.

Validate Governance Records with the Python SDK:

```bash
gc-validate --spec governance-record governance-record.json
```

## Packages

- Python package: `governance-commons` 0.2.0 — `gc-validate`, `gc-report`, `gc-discover`
- npm package: `governance-commons` 0.2.0 — `gc-validate`, `gc-report`

SDK/package versions are independent of Governance Commons specification
versions. See `docs/compatibility-policy.md` for the explicit compatibility
rules; compatibility never implies silent schema fallback.

## Development

```powershell
python -m pytest -q
npm test
python -m build
npm pack --dry-run
```

## Project Shape

This directory is the SDK/reference-implementation repo. VS Code extensions
should live in separate repos, such as `agent-dossier-vscode` or
`governance-commons-vscode`.
