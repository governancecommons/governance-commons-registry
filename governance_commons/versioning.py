"""Specification/package compatibility policy for Governance Commons SDKs."""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Literal

CompatibilityStatus = Literal["supported", "compatible", "unsupported", "invalid"]

_VERSION_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:\.(0|[1-9][0-9]*))?(?:[-+][0-9A-Za-z.-]+)?$")


@dataclass(frozen=True)
class ParsedVersion:
    major: int
    minor: int
    patch: int


@dataclass(frozen=True)
class CompatibilityResult:
    spec: str
    requested_version: str
    current_version: str
    minimum_compatible_version: str
    status: CompatibilityStatus
    message: str


def parse_version(value: str) -> ParsedVersion | None:
    """Parse a GC spec version, accepting the repository's two-part 0.1 form."""
    if not isinstance(value, str):
        return None
    match = _VERSION_RE.fullmatch(value)
    if match is None:
        return None
    return ParsedVersion(int(match.group(1)), int(match.group(2)), int(match.group(3) or 0))


def check_spec_compatibility(
    spec: str,
    requested_version: str,
    *,
    current_version: str,
    minimum_compatible_version: str | None = None,
) -> CompatibilityResult:
    """Classify a requested spec version without silently selecting another schema.

    Exact current versions are supported. Older versions are compatible only when
    an explicit minimum-compatible version is declared. Future major versions and
    versions below that boundary are unsupported. Malformed versions are invalid.
    """
    current = parse_version(current_version)
    minimum = parse_version(minimum_compatible_version or current_version)
    requested = parse_version(requested_version)
    if current is None or minimum is None:
        raise ValueError("current_version and minimum_compatible_version must be valid versions")
    if requested is None:
        return CompatibilityResult(spec, requested_version, current_version, minimum_compatible_version or current_version, "invalid", "specification version is not a valid GC version")
    if requested == current:
        return CompatibilityResult(spec, requested_version, current_version, minimum_compatible_version or current_version, "supported", "requested specification version is exactly supported")
    if requested.major == current.major and minimum <= requested < current:
        return CompatibilityResult(spec, requested_version, current_version, minimum_compatible_version or current_version, "compatible", "requested older specification version is within the explicitly declared compatibility range")
    return CompatibilityResult(spec, requested_version, current_version, minimum_compatible_version or current_version, "unsupported", "requested specification version is outside the explicitly supported compatibility range")


# Versions actually implemented by this repository. These are intentionally exact
# today: no older schema is bundled, so no older version is silently treated as safe.
SPEC_POLICIES: dict[str, tuple[str, str]] = {
    "ons": ("1.4.0", "1.4.0"),
    "agent-dossier": ("1.4.0", "1.4.0"),
    "governance-record": ("1.0.0", "1.0.0"),
    "capabilities": ("0.1", "0.1"),
}


def check_registered_spec_compatibility(spec: str, requested_version: str) -> CompatibilityResult:
    """Apply the repository's explicit compatibility declaration for a spec."""
    try:
        current, minimum = SPEC_POLICIES[spec]
    except KeyError:
        return CompatibilityResult(spec, requested_version, "", "", "unsupported", "specification is not registered by this SDK")
    return check_spec_compatibility(
        spec,
        requested_version,
        current_version=current,
        minimum_compatible_version=minimum,
    )
