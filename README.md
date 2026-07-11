# governance-commons-registry

Reference implementations for Governance Commons standards.

This package currently contains the ONS (Ontic Namespace Structure) Python and TypeScript validators used by downstream tools, including future editor extensions.

## Packages

- Python package: `governance-commons`
- npm package: `governance-commons`

Both package manifests are scaffolded for version `0.1.0`. Registry publication is pending.

## Development

```powershell
python -m pytest -q
npm test
python -m build
npm pack --dry-run
```

## Project Shape

This directory is the SDK/reference-implementation repo. VS Code extensions should live in separate repos, such as `agent-dossier-vscode` or `governance-commons-vscode`.
