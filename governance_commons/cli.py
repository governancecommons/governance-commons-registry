"""CLI entry points — gc-validate and gc-report (GC-2-A-04)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .ons import ONS_SPEC_VERSION, validate_name
from .report import ConformanceReport, RuleResult, build_report

# Stable rule ID per ONS casing domain (ONS-CASING-001 … ONS-CASING-012).
_ONS_RULE_IDS: dict[str, tuple[str, str]] = {
    "python_identifier":     ("ONS-CASING-001", "Python identifiers must be snake_case"),
    "python_class":          ("ONS-CASING-002", "Python class names must be PascalCase"),
    "python_constant":       ("ONS-CASING-003", "Python constants must be UPPER_SNAKE_CASE"),
    "css_custom_property":   ("ONS-CASING-004", "CSS custom properties must be --root-kebab"),
    "governance_id":         ("ONS-CASING-005", "Governance IDs must be CLUSTER.SEQ (e.g. ONS.00)"),
    "governance_cluster":    ("ONS-CASING-006", "Cluster names must be 2–6 uppercase ASCII letters"),
    "python_filename":       ("ONS-CASING-007", "Python filenames must be snake_case.py"),
    "governance_filename":   ("ONS-CASING-008", "Governance filenames must be CLUSTER.SEQ.md"),
    "ts_js_filename":        ("ONS-CASING-009", "TypeScript/JS filenames must be kebab-case"),
    "directory_name":        ("ONS-CASING-010", "Directory names must be lowercase-kebab"),
    "qualification_authority": ("ONS-CASING-011", "Authority qualifications must be UPPER:integer (e.g. AL:2)"),
    "qualification_metadata":  ("ONS-CASING-012", "Metadata qualifications must be lower:lower (e.g. env:production)"),
}


def _validate_ons(subject: str, profile: str) -> ConformanceReport:
    path = Path(subject)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"gc-validate: file not found: {subject}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as exc:
        print(f"gc-validate: invalid JSON in {subject}: {exc}", file=sys.stderr)
        sys.exit(2)

    checks = data.get("checks")
    if not isinstance(checks, list):
        print(f"gc-validate: {subject} must contain a top-level 'checks' array", file=sys.stderr)
        sys.exit(2)

    rules: list[RuleResult] = []
    for i, check in enumerate(checks):
        if not isinstance(check, dict) or "domain" not in check or "name" not in check:
            print(f"gc-validate: check[{i}] must have 'domain' and 'name' fields", file=sys.stderr)
            sys.exit(2)
        domain: str = check["domain"]
        name: str = check["name"]
        rule_id, description = _ONS_RULE_IDS.get(domain, (f"ONS-CASING-???", f"Unknown domain '{domain}'"))
        result = validate_name(domain, name)
        rules.append(RuleResult(
            rule_id=rule_id,
            description=description,
            result="pass" if result.valid else "fail",
            message=None if result.valid else result.violation,
        ))

    return build_report(
        spec="ons",
        spec_version=ONS_SPEC_VERSION,
        profile=profile,  # type: ignore[arg-type]
        subject=subject,
        rules=rules,
    )


def _print_text(report: ConformanceReport) -> None:
    status = "PASS" if report.conformant else "FAIL"
    print(f"GC Conformance Report")
    print(f"  Spec:    {report.spec} {report.spec_version} ({report.profile} profile)")
    print(f"  Subject: {report.subject}")
    print(f"  Result:  {status}")
    print()
    for r in report.rules:
        marker = "+" if r.result == "pass" else ("-" if r.result == "skip" else "!")
        line = f"  {marker} [{r.rule_id}] {r.description}"
        if r.message:
            line += f"\n      {r.message}"
        print(line)
    s = report.summary
    print(f"\n  Summary: {s.passed} passed, {s.failed} failed, {s.skipped} skipped of {s.total} total")


def validate_cmd() -> None:
    """Entry point for gc-validate."""
    parser = argparse.ArgumentParser(
        prog="gc-validate",
        description="Validate a subject against a Governance Commons spec.",
    )
    parser.add_argument("--spec", required=True, choices=["ons"],
                        help="Spec to validate against.")
    parser.add_argument("--profile", default="standard",
                        choices=["advisory", "standard", "strict"],
                        help="Conformance profile to evaluate (default: standard).")
    parser.add_argument("--output", default="text", choices=["text", "json"],
                        help="Output format (default: text).")
    parser.add_argument("subject", help="Path to the JSON checks manifest to validate.")
    args = parser.parse_args()

    if args.spec == "ons":
        report = _validate_ons(args.subject, args.profile)
    else:
        print(f"gc-validate: unsupported spec '{args.spec}'", file=sys.stderr)
        sys.exit(2)

    if args.output == "json":
        print(report.to_json())
    else:
        _print_text(report)

    sys.exit(0 if report.conformant else 1)


def report_cmd() -> None:
    """Entry point for gc-report — display a saved conformance report."""
    parser = argparse.ArgumentParser(
        prog="gc-report",
        description="Display a saved GC conformance report.",
    )
    parser.add_argument("--output", default="text", choices=["text", "json"],
                        help="Output format (default: text).")
    parser.add_argument("report_file", help="Path to a saved conformance report JSON file.")
    args = parser.parse_args()

    path = Path(args.report_file)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"gc-report: file not found: {args.report_file}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as exc:
        print(f"gc-report: invalid JSON in {args.report_file}: {exc}", file=sys.stderr)
        sys.exit(2)

    try:
        from .report import ReportSummary
        rules = [RuleResult(**r) for r in data.get("rules", [])]
        summary_data = data.get("summary", {})
        summary = ReportSummary(**summary_data)
        report = ConformanceReport(
            spec=data["spec"],
            spec_version=data["spec_version"],
            profile=data["profile"],
            subject=data["subject"],
            generated_at=data["generated_at"],
            rules=rules,
            summary=summary,
            conformant=data["conformant"],
            conformance_level=data["conformance_level"],
        )
    except (KeyError, TypeError) as exc:
        print(f"gc-report: malformed report file: {exc}", file=sys.stderr)
        sys.exit(2)

    if args.output == "json":
        print(report.to_json())
    else:
        _print_text(report)

    sys.exit(0 if report.conformant else 1)
