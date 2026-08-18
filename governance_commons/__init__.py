"""
governance-commons — Python reference implementation.

Provides ONS name validation, casing rule checks, governance ID parsing,
separator grammar utilities, and the GC conformance report format.
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
from .report import (
    GC_REPORT_VERSION,
    ConformanceReport,
    ReportSummary,
    RuleResult,
    build_report,
)
from .capabilities import (
    CAPABILITY_CONTRACT_VERSION,
    CAPABILITY_RELATIVE_PATH,
    CapabilityDiscoveryResult,
    CapabilityValidationResult,
    ValidationIssue,
    discover_capabilities,
    validate_capability_contract,
    validate_capability_data,
)

__version__ = "0.2.0"
__all__ = [
    "__version__",
    # ONS
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
    # Conformance report
    "GC_REPORT_VERSION",
    "ConformanceReport",
    "ReportSummary",
    "RuleResult",
    "build_report",
    # Capability contracts
    "CAPABILITY_CONTRACT_VERSION",
    "CAPABILITY_RELATIVE_PATH",
    "CapabilityDiscoveryResult",
    "CapabilityValidationResult",
    "ValidationIssue",
    "discover_capabilities",
    "validate_capability_contract",
    "validate_capability_data",
]
