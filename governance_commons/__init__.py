"""
governance-commons — Python reference implementation.

Provides ONS name validation, casing rule checks, governance ID parsing,
and separator grammar utilities derived from the canonical ONS specification.
"""

from .ons import (
    CASING_RULES,
    ONS_SPEC_VERSION,
    SEPARATORS,
    CasingRule,
    GovernanceIdResult,
    SeparatorRule,
    ValidationResult,
    detect_separator,
    detect_separators,
    get_casing_rule,
    list_domains,
    parse_governance_id,
    validate_cluster,
    validate_name,
)

__version__ = "0.1.0"
__all__ = [
    "__version__",
    "CASING_RULES",
    "ONS_SPEC_VERSION",
    "SEPARATORS",
    "CasingRule",
    "GovernanceIdResult",
    "SeparatorRule",
    "ValidationResult",
    "detect_separator",
    "detect_separators",
    "get_casing_rule",
    "list_domains",
    "parse_governance_id",
    "validate_cluster",
    "validate_name",
]
