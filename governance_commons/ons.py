"""
ONS (Ontic Namespace Structure) — Python reference implementation.

Validates names against the casing rules, separator grammar, governance ID grammar,
and cluster registration protocol defined in ONS v1.4.0.

This module has zero runtime dependencies. All patterns are derived directly from
the canonical ONS specification (ons/ons.yaml) and are versioned with this package.

Spec: ONS v1.4.0  |  https://governancecommons.org/ons
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

# ---------------------------------------------------------------------------
# Separator grammar
# ---------------------------------------------------------------------------

SeparatorToken = Literal[".", "-", "_", ":"]
SeparatorSemantic = Literal["hierarchy", "compound", "lexical_binding", "qualification"]


@dataclass(frozen=True)
class SeparatorRule:
    token: SeparatorToken
    name: Literal["dot", "hyphen", "underscore", "colon"]
    semantic: SeparatorSemantic
    meaning: str


SEPARATORS: tuple[SeparatorRule, ...] = (
    SeparatorRule(token=".", name="dot", semantic="hierarchy",
                  meaning="Scope depth or namespace nesting."),
    SeparatorRule(token="-", name="hyphen", semantic="compound",
                  meaning="Human-readable word or segment joining."),
    SeparatorRule(token="_", name="underscore", semantic="lexical_binding",
                  meaning="Words bound inside a language identifier."),
    SeparatorRule(token=":", name="colon", semantic="qualification",
                  meaning="Attribute qualification, level, or key-value boundary."),
)

# ---------------------------------------------------------------------------
# Casing rules
# ---------------------------------------------------------------------------

CasingDomain = Literal[
    "python_identifier",
    "python_class",
    "python_constant",
    "css_custom_property",
    "governance_id",
    "governance_cluster",
    "python_filename",
    "governance_filename",
    "ts_js_filename",
    "directory_name",
    "qualification_authority",
    "qualification_metadata",
]


@dataclass(frozen=True)
class CasingRule:
    domain: CasingDomain
    rule: str
    pattern: re.Pattern[str]
    description: str


CASING_RULES: tuple[CasingRule, ...] = (
    CasingRule(
        domain="python_identifier",
        rule="snake_case",
        pattern=re.compile(r"^[a-z_][a-z0-9_]*$"),
        description="Lowercase, underscore-separated Python identifiers.",
    ),
    CasingRule(
        domain="python_class",
        rule="PascalCase",
        pattern=re.compile(r"^[A-Z][A-Za-z0-9]*$"),
        description="PascalCase Python class names.",
    ),
    CasingRule(
        domain="python_constant",
        rule="UPPER_SNAKE",
        pattern=re.compile(r"^[A-Z][A-Z0-9_]*$"),
        description="UPPER_SNAKE_CASE Python constants.",
    ),
    CasingRule(
        domain="css_custom_property",
        rule="--root-kebab",
        pattern=re.compile(r"^--[a-z][a-z0-9]*(?:-[a-z0-9]+)+$"),
        description="CSS custom properties prefixed with -- in kebab-case.",
    ),
    CasingRule(
        domain="governance_id",
        rule="UPPER.decimal",
        pattern=re.compile(r"^[A-Z]{2,6}\.[0-9]{2}$"),
        description="Governance record IDs: CLUSTER.SEQ (e.g. ONS.00).",
    ),
    CasingRule(
        domain="governance_cluster",
        rule="UPPER",
        pattern=re.compile(r"^[A-Z]{2,6}$"),
        description="Registered uppercase cluster identifiers (2–6 chars).",
    ),
    CasingRule(
        domain="python_filename",
        rule="snake_case.py",
        pattern=re.compile(r"^[a-z][a-z0-9_]*\.py$"),
        description="snake_case Python filenames ending in .py.",
    ),
    CasingRule(
        domain="governance_filename",
        rule="UPPER.decimal.md",
        pattern=re.compile(r"^[A-Z]{2,6}\.[0-9]{2}\.md$"),
        description="Governance document filenames: CLUSTER.SEQ.md.",
    ),
    CasingRule(
        domain="ts_js_filename",
        rule="kebab-case",
        pattern=re.compile(r"^[a-z0-9][a-z0-9-]*\.(?:ts|js)$"),
        description="kebab-case TypeScript and JavaScript filenames.",
    ),
    CasingRule(
        domain="directory_name",
        rule="lowercase-kebab",
        pattern=re.compile(r"^[a-z0-9][a-z0-9-]*$"),
        description="Lowercase kebab-case directory names.",
    ),
    CasingRule(
        domain="qualification_authority",
        rule="UPPER:integer",
        pattern=re.compile(r"^[A-Z]{1,6}:[0-9]+$"),
        description="Authority level qualifications (e.g. AL:2).",
    ),
    CasingRule(
        domain="qualification_metadata",
        rule="lower:lower",
        pattern=re.compile(r"^[a-z][a-z0-9.]*:[a-z0-9._-]+$"),
        description="Metadata key-value qualifications (e.g. env:production).",
    ),
)

_DOMAIN_INDEX: dict[str, CasingRule] = {r.domain: r for r in CASING_RULES}

# ---------------------------------------------------------------------------
# Governance ID grammar
# ---------------------------------------------------------------------------

_CLUSTER_RE = re.compile(r"^[A-Z]{2,6}$")
_SEQ_RE = re.compile(r"^[0-9]{2}$")
_GOVERNANCE_ID_RE = re.compile(r"^[A-Z]{2,6}\.[0-9]{2}$")

# ---------------------------------------------------------------------------
# Validation result types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    violation: str | None = None


@dataclass(frozen=True)
class GovernanceIdResult:
    valid: bool
    cluster: str | None = None
    seq: str | None = None
    violation: str | None = None


# ---------------------------------------------------------------------------
# Core validation API
# ---------------------------------------------------------------------------


def validate_name(domain: str, name: str) -> ValidationResult:
    """Validate a name against the casing rule for a given ONS domain.

    Args:
        domain: The ONS casing domain to validate against.
        name: The name to validate.

    Returns:
        ValidationResult with valid=True if the name conforms.

    Example::

        validate_name("python_identifier", "run_intent")  # ValidationResult(valid=True)
        validate_name("python_identifier", "runIntent")   # ValidationResult(valid=False, ...)
    """
    rule = _DOMAIN_INDEX.get(domain)
    if rule is None:
        return ValidationResult(
            valid=False,
            violation=f'Unknown casing domain: "{domain}".',
        )
    if rule.pattern.match(name):
        return ValidationResult(valid=True)
    return ValidationResult(
        valid=False,
        violation=(
            f'"{name}" does not conform to ONS domain "{domain}" '
            f"(rule: {rule.rule}, pattern: {rule.pattern.pattern})."
        ),
    )


def parse_governance_id(id_: str) -> GovernanceIdResult:
    """Parse and validate an ONS governance ID (CLUSTER.SEQ format).

    A governance ID MUST match ``^[A-Z]{2,6}\\.[0-9]{2}$``.

    Args:
        id_: The governance ID to validate (e.g. "ONS.00", "PASS.01").

    Returns:
        GovernanceIdResult with cluster and seq on success.

    Example::

        parse_governance_id("ONS.00")  # GovernanceIdResult(valid=True, cluster="ONS", seq="00")
        parse_governance_id("ons.00")  # GovernanceIdResult(valid=False, ...)
    """
    if _GOVERNANCE_ID_RE.match(id_):
        dot = id_.index(".")
        return GovernanceIdResult(valid=True, cluster=id_[:dot], seq=id_[dot + 1 :])

    dot = id_.find(".")
    if dot == -1:
        return GovernanceIdResult(
            valid=False,
            violation=(
                f'"{id_}" is missing the dot separator. '
                "Expected format: CLUSTER.SEQ (e.g. ONS.00)."
            ),
        )
    cluster, seq = id_[:dot], id_[dot + 1 :]
    if not _CLUSTER_RE.match(cluster):
        return GovernanceIdResult(
            valid=False,
            violation=(
                f'Cluster "{cluster}" must be 2–6 uppercase ASCII letters '
                f"(pattern: {_CLUSTER_RE.pattern})."
            ),
        )
    return GovernanceIdResult(
        valid=False,
        violation=(
            f'Sequence "{seq}" must be a zero-padded two-digit integer '
            f"(pattern: {_SEQ_RE.pattern})."
        ),
    )


def validate_cluster(cluster: str) -> ValidationResult:
    """Validate whether a governance cluster name is well-formed.

    A valid cluster name is 2–6 uppercase ASCII letters, matching ``^[A-Z]{2,6}$``.

    Args:
        cluster: The cluster name to validate (e.g. "ONS", "PASS", "GC").

    Example::

        validate_cluster("ONS")  # ValidationResult(valid=True)
        validate_cluster("ons")  # ValidationResult(valid=False, ...)
    """
    if _CLUSTER_RE.match(cluster):
        return ValidationResult(valid=True)
    return ValidationResult(
        valid=False,
        violation=(
            f'"{cluster}" is not a valid cluster name. '
            f"Expected 2–6 uppercase ASCII letters (pattern: {_CLUSTER_RE.pattern})."
        ),
    )


def detect_separator(name: str) -> SeparatorSemantic | None:
    """Return the semantic of the first ONS separator found in a name, or None.

    Args:
        name: The name to inspect.

    Example::

        detect_separator("eco.ui.help")  # "hierarchy"
        detect_separator("run_intent")   # "lexical_binding"
        detect_separator("simple")       # None
    """
    for sep in SEPARATORS:
        if sep.token in name:
            return sep.semantic
    return None


def detect_separators(
    name: str,
) -> list[tuple[SeparatorToken, SeparatorSemantic]]:
    """Audit all ONS separator tokens present in a name.

    An ONS-conformant name MUST use at most one separator semantic.

    Args:
        name: The name to audit.

    Returns:
        List of (token, semantic) tuples for each separator found.

    Example::

        detect_separators("eco.ui_help")
        # [(".", "hierarchy"), ("_", "lexical_binding")]
    """
    return [(sep.token, sep.semantic) for sep in SEPARATORS if sep.token in name]


def get_casing_rule(domain: str) -> CasingRule | None:
    """Look up the casing rule for a domain by name.

    Returns None if the domain is not registered in ONS.
    """
    return _DOMAIN_INDEX.get(domain)


def list_domains() -> tuple[CasingDomain, ...]:
    """Return all registered ONS casing domain names."""
    return tuple(r.domain for r in CASING_RULES)


# ---------------------------------------------------------------------------
# Version metadata
# ---------------------------------------------------------------------------

ONS_SPEC_VERSION = "1.4.0"
