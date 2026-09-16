"""Governance Commons specification compatibility policy (GC-SDK.05).

Compatibility is evaluated against the specification version a validator is
built against. SDK/package versions are independent release versions; they do
not imply compatibility with a specification version by numeric similarity.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum

from .capabilities import CAPABILITY_CONTRACT_VERSION
from .dossier import DOSSIER_SPEC_VERSION
from .governance_records import GOVERNANCE_RECORD_SPEC_VERSION
from .ons import ONS_SPEC_VERSION
from .report import RuleResult


class CompatibilityStatus(StrEnum):
    """Classification of a declared specification version."""

    CURRENT = "current"
    COMPATIBLE_OLDER = "compatible_older"
    INCOMPATIBLE_OLDER = "incompatible_older"
    UNSUPPORTED_FUTURE = "unsupported_future"
    INVALID = "invalid"
    UNKNOWN_SPEC = "unknown_spec"


@dataclass(frozen=True)
class SpecVersion:
    """Normalized semantic version used by the compatibility policy."""

    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, value: str) -> "SpecVersion | None":
        if not isinstance(value, str):
            return None
        match = re.fullmatch(r"(0|[1-9][0-9]*)(?:\.(0|[1-9][0-9]*))(?:\.(0|[1-9][0-9]*))?", value)
        if not match:
            return None
        major, minor, patch = match.groups()
        return cls(int(major), int(minor), int(patch or 0))

    def __lt__(self, other: "SpecVersion") -> bool:
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

    def __gt__(self, other: "SpecVersion") -> bool:
        return (self.major, self.minor, self.patch) > (other.major, other.minor, other.patch)


# These are the versions the current reference validators are built against.
SUPPORTED_SPEC_VERSIONS: dict[str, str] = {
    "ons": ONS_SPEC_VERSION,
    "capabilities": CAPABILITY_CONTRACT_VERSION,
    "dossier": DOSSIER_SPEC_VERSION,
    "governance-record": GOVERNANCE_RECORD_SPEC_VERSION,
}


def classify_spec_version(spec: str, declared_version: str) -> CompatibilityStatus:
    """Classify a declared version without silently selecting another schema.

    Stable specifications (major >= 1) accept older versions within the same
    major as version-compatible. Pre-1.0 specifications use the minor version
    as the compatibility boundary, so only the same 0.x minor is compatible.
    A version may be classified as compatible_older by this policy, but the
    caller MUST still have an explicitly backward-compatible validator/schema;
    this function never performs a fallback to another schema.
    """
    current_text = SUPPORTED_SPEC_VERSIONS.get(spec)
    if current_text is None:
        return CompatibilityStatus.UNKNOWN_SPEC

    current = SpecVersion.parse(current_text)
    declared = SpecVersion.parse(declared_version)
    if current is None or declared is None:
        return CompatibilityStatus.INVALID
    current_tuple = (current.major, current.minor, current.patch)
    declared_tuple = (declared.major, declared.minor, declared.patch)
    if declared_tuple == current_tuple:
        return CompatibilityStatus.CURRENT
    if declared_tuple > current_tuple:
        return CompatibilityStatus.UNSUPPORTED_FUTURE

    if current.major == 0:
        return (
            CompatibilityStatus.COMPATIBLE_OLDER
            if declared.major == 0 and declared.minor == current.minor
            else CompatibilityStatus.INCOMPATIBLE_OLDER
        )
    return (
        CompatibilityStatus.COMPATIBLE_OLDER
        if declared.major == current.major
        else CompatibilityStatus.INCOMPATIBLE_OLDER
    )


def compatibility_rule(spec: str, declared_version: str) -> RuleResult:
    """Return a deterministic compatibility rule result.

    An older-compatible classification is reported as ``skip`` rather than a
    pass because version compatibility alone does not prove that the current
    schema can validate the historical version.
    """
    status = classify_spec_version(spec, declared_version)
    current = SUPPORTED_SPEC_VERSIONS.get(spec)

    if status is CompatibilityStatus.CURRENT:
        return RuleResult(
            "GC-SDK-COMPAT-001",
            "Declared specification version is supported by this SDK",
            "pass",
            f"{spec} {declared_version} is the current supported version",
        )
    if status is CompatibilityStatus.COMPATIBLE_OLDER:
        return RuleResult(
            "GC-SDK-COMPAT-001",
            "Declared specification version is version-compatible with this SDK",
            "skip",
            f"{spec} {declared_version} is older but version-compatible; schema compatibility must be established separately",
        )
    if status is CompatibilityStatus.UNSUPPORTED_FUTURE:
        return RuleResult(
            "GC-SDK-COMPAT-001",
            "Declared specification version is supported by this SDK",
            "fail",
            f"{spec} {declared_version} is newer than the validator's supported version {current}",
        )
    if status is CompatibilityStatus.INCOMPATIBLE_OLDER:
        return RuleResult(
            "GC-SDK-COMPAT-001",
            "Declared specification version is supported by this SDK",
            "fail",
            f"{spec} {declared_version} is outside the compatible version range for supported version {current}",
        )
    if status is CompatibilityStatus.INVALID:
        return RuleResult(
            "GC-SDK-COMPAT-001",
            "Declared specification version is supported by this SDK",
            "fail",
            f"{spec} has an invalid specification version: {declared_version!r}",
        )
    return RuleResult(
        "GC-SDK-COMPAT-001",
        "Declared specification version is supported by this SDK",
        "fail",
        f"unknown Governance Commons specification: {spec}",
    )


__all__ = [
    "CompatibilityStatus",
    "SpecVersion",
    "SUPPORTED_SPEC_VERSIONS",
    "classify_spec_version",
    "compatibility_rule",
]
