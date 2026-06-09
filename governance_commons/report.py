"""
Conformance report types — GC-2-C-01.

Defines the machine-readable output contract for all Governance Commons validators.
Every validator (Python or TypeScript) MUST produce a ConformanceReport whose
serialised form validates against:
  docs/conformance/conformance-report.schema.json  (gc_report_version: "1.0.0")
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Literal

GC_REPORT_VERSION = "1.0.0"

ConformanceProfile = Literal["advisory", "standard", "strict"]
RuleOutcome = Literal["pass", "fail", "skip"]
ConformanceLevel = Literal["none", "advisory", "standard", "strict"]


@dataclass
class RuleResult:
    rule_id: str
    description: str
    result: RuleOutcome
    message: str | None = None


@dataclass
class ReportSummary:
    total: int
    passed: int
    failed: int
    skipped: int


@dataclass
class ConformanceReport:
    spec: str
    spec_version: str
    profile: ConformanceProfile
    subject: str
    generated_at: str
    rules: list[RuleResult]
    summary: ReportSummary
    conformant: bool
    conformance_level: ConformanceLevel
    gc_report_version: str = field(default=GC_REPORT_VERSION, init=False)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, *, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


def build_report(
    *,
    spec: str,
    spec_version: str,
    profile: ConformanceProfile,
    subject: str,
    rules: list[RuleResult],
    generated_at: str | None = None,
) -> ConformanceReport:
    """Construct a ConformanceReport from a list of RuleResults.

    Computes summary counts, conformant flag, and conformance_level automatically.

    Args:
        spec: Spec identifier (e.g. "ons").
        spec_version: Semver of the spec (e.g. "1.4.0").
        profile: Conformance profile evaluated.
        subject: File path, URI, or label of what was validated.
        rules: Ordered list of per-rule results.
        generated_at: ISO 8601 UTC timestamp; defaults to now.

    Example::

        report = build_report(
            spec="ons",
            spec_version="1.4.0",
            profile="standard",
            subject="my-file.yaml",
            rules=[RuleResult("ONS-CASING-001", "snake_case identifiers", "pass")],
        )
    """
    passed = sum(1 for r in rules if r.result == "pass")
    failed = sum(1 for r in rules if r.result == "fail")
    skipped = sum(1 for r in rules if r.result == "skip")
    conformant = failed == 0
    conformance_level: ConformanceLevel = profile if conformant else "none"

    return ConformanceReport(
        spec=spec,
        spec_version=spec_version,
        profile=profile,
        subject=subject,
        generated_at=generated_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        rules=rules,
        summary=ReportSummary(total=passed + failed + skipped, passed=passed, failed=failed, skipped=skipped),
        conformant=conformant,
        conformance_level=conformance_level,
    )
