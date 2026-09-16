"""Agent Dossier instance validation (structural, v1.4.0 instance schema)."""
from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any, Sequence

import yaml
from jsonschema import Draft202012Validator

# Version of agent-dossier-instance.schema.json this validator was built against.
# Tracks the Agent Dossier Specification's specification.version, not the schema $id.
DOSSIER_SPEC_VERSION = "1.4.0"


@dataclass(frozen=True)
class ValidationIssue:
    """One deterministic validation failure."""

    rule_id: str
    path: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"rule_id": self.rule_id, "path": self.path, "message": self.message}


@dataclass(frozen=True)
class DossierValidationResult:
    """Validation outcome for one agent dossier instance."""

    source_file: str
    valid: bool
    agent_id: str | None
    issues: tuple[ValidationIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_file": self.source_file,
            "valid": self.valid,
            "agent_id": self.agent_id,
            "issues": [issue.to_dict() for issue in self.issues],
        }


def _load_schema() -> dict[str, Any]:
    schema_resource = resources.files("governance_commons").joinpath(
        "schemas/agent-dossier-instance.schema.json"
    )
    return json.loads(schema_resource.read_text(encoding="utf-8"))


_SCHEMA = _load_schema()
Draft202012Validator.check_schema(_SCHEMA)
_VALIDATOR = Draft202012Validator(_SCHEMA)


class _StringTimestampLoader(yaml.SafeLoader):
    """SafeLoader variant that keeps RFC3339 timestamps as strings.

    The schema requires whole-second RFC3339 UTC strings (e.g. dossier_metadata.created_at,
    capability_claims[].declared_at). PyYAML's default SafeLoader auto-converts unquoted
    ISO8601-looking scalars into datetime.datetime, which then fails the schema's
    {"type": "string", "pattern": ...} check even though the source YAML is valid.
    """


_StringTimestampLoader.yaml_implicit_resolvers = {
    key: [(tag, regexp) for tag, regexp in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


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
        issues.append(ValidationIssue(
            rule_id="GC-DOSSIER-SCHEMA-001",
            path=_json_path(list(error.absolute_path)),
            message=error.message,
        ))
    return issues


def validate_dossier_data(
    data: Any,
    source_file: str = "<memory>",
) -> DossierValidationResult:
    """Validate an already-parsed agent dossier instance without mutating it."""

    issues = _schema_issues(data)
    agent_id: str | None = None
    if isinstance(data, dict) and isinstance(data.get("identity"), dict):
        candidate = data["identity"].get("agent_id")
        agent_id = candidate if isinstance(candidate, str) else None

    return DossierValidationResult(
        source_file=source_file,
        valid=not issues,
        agent_id=agent_id,
        issues=tuple(issues),
    )


def validate_dossier_contract(path: str | Path) -> DossierValidationResult:
    """Parse and validate a YAML agent dossier instance."""

    source = Path(path)
    source_label = str(source.resolve())
    try:
        data = yaml.load(source.read_text(encoding="utf-8"), Loader=_StringTimestampLoader)
    except OSError as exc:
        issue = ValidationIssue("GC-DOSSIER-INPUT-001", "$", str(exc))
        return DossierValidationResult(source_label, False, None, (issue,))
    except yaml.YAMLError as exc:
        issue = ValidationIssue("GC-DOSSIER-INPUT-002", "$", f"invalid YAML: {exc}")
        return DossierValidationResult(source_label, False, None, (issue,))
    return validate_dossier_data(data, source_label)
