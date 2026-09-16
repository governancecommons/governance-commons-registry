"""
governance-commons — Python reference implementation.

Provides ONS name validation, casing rule checks, governance ID parsing,
separator grammar utilities, shared conformance reporting, capability
validation/discovery, Agent Dossier validation, Governance Record validation,
interoperability bindings, and specification compatibility classification.
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
from .dossier import DOSSIER_SPEC_VERSION, validate_dossier_contract
from .governance_records import GOVERNANCE_RECORD_SPEC_VERSION, validate_governance_record_contract
from .interoperability import bind_atp_audit_trail
from .compatibility import (
    CompatibilityStatus,
    SUPPORTED_SPEC_VERSIONS,
    SpecVersion,
    classify_spec_version,
    compatibility_rule,
)

__version__ = "0.2.0"
__all__ = [
    "__version__",
    "CASING_RULES", "ONS_SPEC_VERSION", "SEPARATORS", "CasingRule", "GovernanceIdResult",
    "SeparatorRule", "ValidationResult", "detect_separator", "detect_separators",
    "get_casing_rule", "list_domains", "parse_governance_id", "validate_cluster", "validate_name",
    "GC_REPORT_VERSION", "ConformanceReport", "ReportSummary", "RuleResult", "build_report",
    "CAPABILITY_CONTRACT_VERSION", "CAPABILITY_RELATIVE_PATH", "CapabilityDiscoveryResult",
    "CapabilityValidationResult", "ValidationIssue", "discover_capabilities",
    "validate_capability_contract", "validate_capability_data",
    "DOSSIER_SPEC_VERSION", "validate_dossier_contract",
    "GOVERNANCE_RECORD_SPEC_VERSION", "validate_governance_record_contract",
    "bind_atp_audit_trail",
    "CompatibilityStatus", "SUPPORTED_SPEC_VERSIONS", "SpecVersion", "classify_spec_version", "compatibility_rule",
]
