"""Capability Contract v0.1 validation and repository-root discovery."""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any, Iterable, Sequence

import yaml
from jsonschema import Draft202012Validator

CAPABILITY_CONTRACT_VERSION = "0.1"
CAPABILITY_RELATIVE_PATH = Path(".governance/contracts/capabilities.yaml")


@dataclass(frozen=True)
class ValidationIssue:
    """One deterministic validation failure."""

    rule_id: str
    path: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "rule_id": self.rule_id,
            "path": self.path,
            "message": self.message,
        }


@dataclass(frozen=True)
class CapabilityValidationResult:
    """Validation outcome for one declaration."""

    source_file: str
    valid: bool
    component_id: str | None
    issues: tuple[ValidationIssue, ...]
    declaration: dict[str, Any] | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_file": self.source_file,
            "valid": self.valid,
            "component_id": self.component_id,
            "issues": [issue.to_dict() for issue in self.issues],
        }


@dataclass(frozen=True)
class CapabilityDiscoveryResult:
    """Normalized providers and invalid declarations for one discovery query."""

    capability_id: str | None
    providers: tuple[dict[str, Any], ...]
    invalid_contracts: tuple[CapabilityValidationResult, ...]
    scanned_contracts: int

    @property
    def valid(self) -> bool:
        return not self.invalid_contracts

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_version": CAPABILITY_CONTRACT_VERSION,
            "capability_id": self.capability_id,
            "authority_evaluated": False,
            "execution_authority": "not_evaluated",
            "scanned_contracts": self.scanned_contracts,
            "providers": list(self.providers),
            "invalid_contracts": [result.to_dict() for result in self.invalid_contracts],
        }


def _load_schema() -> dict[str, Any]:
    schema_resource = resources.files("governance_commons").joinpath(
        "schemas/capabilities.schema.json"
    )
    return json.loads(schema_resource.read_text(encoding="utf-8"))


_SCHEMA = _load_schema()
Draft202012Validator.check_schema(_SCHEMA)
_VALIDATOR = Draft202012Validator(_SCHEMA)


def _json_path(parts: Sequence[object]) -> str:
    path = "$"
    for part in parts:
        path += f"[{part}]" if isinstance(part, int) else f".{part}"
    return path


def _schema_issues(data: Any) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    errors = sorted(
        _VALIDATOR.iter_errors(data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    for error in errors:
        path_parts = list(error.absolute_path)
        # Duplicate interface references have a more useful semantic rule below.
        if error.validator == "uniqueItems" and path_parts[-1:] == ["interfaces"]:
            continue
        issues.append(ValidationIssue(
            rule_id="GC-CAP-SCHEMA-001",
            path=_json_path(path_parts),
            message=error.message,
        ))
    return issues


def _semantic_issues(data: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    provides = data.get("provides")
    if not isinstance(provides, list):
        return issues

    provided_ids = [
        item.get("id") for item in provides
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]
    for capability_id, count in sorted(Counter(provided_ids).items()):
        if count > 1:
            issues.append(ValidationIssue(
                rule_id="GC-CAP-SEMANTIC-001",
                path="$.provides",
                message=f"provided capability ID appears {count} times: {capability_id}",
            ))

    prohibited = data.get("prohibits")
    prohibited_ids = {
        item.get("capability") for item in prohibited
        if isinstance(item, dict) and isinstance(item.get("capability"), str)
    } if isinstance(prohibited, list) else set()
    for capability_id in sorted(set(provided_ids) & prohibited_ids):
        issues.append(ValidationIssue(
            rule_id="GC-CAP-SEMANTIC-002",
            path="$.prohibits",
            message=f"capability is both provided and prohibited: {capability_id}",
        ))

    for index, item in enumerate(provides):
        if not isinstance(item, dict) or not isinstance(item.get("interfaces"), list):
            continue
        interface_ids = [value for value in item["interfaces"] if isinstance(value, str)]
        duplicates = sorted(value for value, count in Counter(interface_ids).items() if count > 1)
        for interface_id in duplicates:
            issues.append(ValidationIssue(
                rule_id="GC-CAP-SEMANTIC-003",
                path=f"$.provides[{index}].interfaces",
                message=f"interface reference appears more than once: {interface_id}",
            ))
    return issues


def validate_capability_data(
    data: Any,
    source_file: str = "<memory>",
) -> CapabilityValidationResult:
    """Validate an already-parsed capability declaration without mutating it."""

    issues = _schema_issues(data)
    if isinstance(data, dict):
        issues.extend(_semantic_issues(data))
    issues.sort(key=lambda issue: (issue.path, issue.rule_id, issue.message))

    component_id: str | None = None
    if isinstance(data, dict) and isinstance(data.get("component"), dict):
        candidate = data["component"].get("id")
        component_id = candidate if isinstance(candidate, str) else None

    return CapabilityValidationResult(
        source_file=source_file,
        valid=not issues,
        component_id=component_id,
        issues=tuple(issues),
        declaration=data if isinstance(data, dict) else None,
    )


def validate_capability_contract(path: str | Path) -> CapabilityValidationResult:
    """Parse and validate a YAML capability declaration."""

    source = Path(path)
    source_label = str(source.resolve())
    try:
        data = yaml.safe_load(source.read_text(encoding="utf-8"))
    except OSError as exc:
        issue = ValidationIssue("GC-CAP-INPUT-001", "$", str(exc))
        return CapabilityValidationResult(source_label, False, None, (issue,), None)
    except yaml.YAMLError as exc:
        issue = ValidationIssue("GC-CAP-INPUT-002", "$", f"invalid YAML: {exc}")
        return CapabilityValidationResult(source_label, False, None, (issue,), None)
    return validate_capability_data(data, source_label)


def _contract_candidates(roots: Iterable[str | Path]) -> list[tuple[Path, Path]]:
    candidates: dict[Path, Path] = {}
    for value in roots:
        root = Path(value).resolve()
        if root.is_file():
            candidates[root] = root.parent
            continue
        contract = root / CAPABILITY_RELATIVE_PATH
        if contract.is_file():
            candidates[contract] = root
    return [(repo_root, contract) for contract, repo_root in sorted(
        candidates.items(), key=lambda item: str(item[0]).lower()
    )]


def discover_capabilities(
    roots: Iterable[str | Path],
    capability_id: str | None = None,
) -> CapabilityDiscoveryResult:
    """Discover providers from explicit repository roots or contract files."""

    providers: list[dict[str, Any]] = []
    invalid: list[CapabilityValidationResult] = []
    candidates = _contract_candidates(roots)
    for repo_root, contract_path in candidates:
        result = validate_capability_contract(contract_path)
        if not result.valid or result.declaration is None:
            invalid.append(result)
            continue

        declaration = result.declaration
        component = declaration["component"]
        metadata = declaration.get("metadata", {})
        for capability in declaration["provides"]:
            if capability_id is not None and capability["id"] != capability_id:
                continue
            providers.append({
                "capability_id": capability["id"],
                "capability_version": capability["version"],
                "stability": capability["stability"],
                "component_id": component["id"],
                "component_version": component.get("version"),
                "repository": metadata.get("repository", repo_root.name),
                "interface_refs": capability.get("interfaces", []),
                "source_file": str(contract_path),
                "validation_status": "valid",
            })

    providers.sort(key=lambda item: (
        item["capability_id"], item["component_id"], item["capability_version"]
    ))
    invalid.sort(key=lambda result: result.source_file.lower())
    return CapabilityDiscoveryResult(
        capability_id=capability_id,
        providers=tuple(providers),
        invalid_contracts=tuple(invalid),
        scanned_contracts=len(candidates),
    )
