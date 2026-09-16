"""CLI entry points for Governance Commons validation and report display."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .capabilities import CAPABILITY_CONTRACT_VERSION, validate_capability_contract
from .dossier import DOSSIER_SPEC_VERSION, validate_dossier_contract
from .governance_records import GOVERNANCE_RECORD_SPEC_VERSION, validate_governance_record_contract
from .ons import ONS_SPEC_VERSION, validate_name
from .report import GC_REPORT_VERSION, ConformanceReport, RuleResult, ReportSummary, build_report

_ONS_RULE_IDS: dict[str, tuple[str, str]] = {
    "python_identifier": ("ONS-CASING-001", "Python identifiers must be snake_case"),
    "python_class": ("ONS-CASING-002", "Python class names must be PascalCase"),
    "python_constant": ("ONS-CASING-003", "Python constants must be UPPER_SNAKE_CASE"),
    "css_custom_property": ("ONS-CASING-004", "CSS custom properties must be --root-kebab"),
    "governance_id": ("ONS-CASING-005", "Governance IDs must be CLUSTER.SEQ"),
    "governance_cluster": ("ONS-CASING-006", "Cluster names must be 2–6 uppercase ASCII letters"),
    "python_filename": ("ONS-CASING-007", "Python filenames must be snake_case.py"),
    "governance_filename": ("ONS-CASING-008", "Governance filenames must be CLUSTER.SEQ.md"),
    "ts_js_filename": ("ONS-CASING-009", "TypeScript/JS filenames must be kebab-case"),
    "directory_name": ("ONS-CASING-010", "Directory names must be lowercase-kebab"),
    "qualification_authority": ("ONS-CASING-011", "Authority qualifications must be UPPER:integer"),
    "qualification_metadata": ("ONS-CASING-012", "Metadata qualifications must be lower:lower"),
}


def _load_json(subject: str) -> object:
    try:
        return json.loads(Path(subject).read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"gc-validate: file not found: {subject}", file=sys.stderr)
        raise SystemExit(2)
    except json.JSONDecodeError as exc:
        print(f"gc-validate: invalid JSON in {subject}: {exc}", file=sys.stderr)
        raise SystemExit(2)


def _validate_ons(subject: str, profile: str) -> ConformanceReport:
    data = _load_json(subject)
    if not isinstance(data, dict) or not isinstance(data.get("checks"), list):
        print(f"gc-validate: {subject} must contain a top-level 'checks' array", file=sys.stderr)
        raise SystemExit(2)
    rules: list[RuleResult] = []
    for i, check in enumerate(data["checks"]):
        if not isinstance(check, dict) or not isinstance(check.get("domain"), str) or not isinstance(check.get("name"), str):
            print(f"gc-validate: check[{i}] must have 'domain' and 'name' fields", file=sys.stderr)
            raise SystemExit(2)
        domain, name = check["domain"], check["name"]
        rule_id, description = _ONS_RULE_IDS.get(domain, ("ONS-CASING-???", f"Unknown domain '{domain}'"))
        result = validate_name(domain, name)
        rules.append(RuleResult(rule_id, description, "pass" if result.valid else "fail", None if result.valid else result.violation))
    return build_report(spec="ons", spec_version=ONS_SPEC_VERSION, profile=profile, subject=subject, rules=rules)  # type: ignore[arg-type]


def _validate_capabilities(subject: str, profile: str) -> ConformanceReport:
    result = validate_capability_contract(subject)
    rules = [RuleResult("GC-CAP-SCHEMA-000", "Capability declaration satisfies v0.1 structure and semantics", "pass")] if result.valid else [RuleResult(i.rule_id, f"Capability contract issue at {i.path}", "fail", i.message) for i in result.issues]
    return build_report(spec="capabilities", spec_version=CAPABILITY_CONTRACT_VERSION, profile=profile, subject=subject, rules=rules)  # type: ignore[arg-type]


def _validate_dossier(subject: str, profile: str) -> ConformanceReport:
    result = validate_dossier_contract(subject)
    rules = [RuleResult("GC-DOSSIER-SCHEMA-000", "Agent dossier instance satisfies v1.4.0 structure", "pass")] if result.valid else [RuleResult(i.rule_id, f"Agent dossier issue at {i.path}", "fail", i.message) for i in result.issues]
    return build_report(spec="dossier", spec_version=DOSSIER_SPEC_VERSION, profile=profile, subject=subject, rules=rules)  # type: ignore[arg-type]


def _validate_governance_record(subject: str, profile: str) -> ConformanceReport:
    return validate_governance_record_contract(subject, profile=profile)


def _print_text(report: ConformanceReport) -> None:
    print("GC Conformance Report")
    print(f"  Spec:    {report.spec} {report.spec_version} ({report.profile} profile)")
    print(f"  Subject: {report.subject}")
    print(f"  Result:  {'PASS' if report.conformant else 'FAIL'}\n")
    for rule in report.rules:
        marker = "+" if rule.result == "pass" else ("-" if rule.result == "skip" else "!")
        print(f"  {marker} [{rule.rule_id}] {rule.description}")
        if rule.message:
            print(f"      {rule.message}")
    s = report.summary
    print(f"\n  Summary: {s.passed} passed, {s.failed} failed, {s.skipped} skipped of {s.total} total")


def validate_cmd() -> None:
    parser = argparse.ArgumentParser(prog="gc-validate", description="Validate a subject against a Governance Commons spec.")
    parser.add_argument("--spec", required=True, choices=["ons", "capabilities", "dossier", "governance-record"])
    parser.add_argument("--profile", default="standard", choices=["advisory", "standard", "strict"])
    parser.add_argument("--output", default="text", choices=["text", "json"])
    parser.add_argument("subject")
    args = parser.parse_args()
    validators = {"ons": _validate_ons, "capabilities": _validate_capabilities, "dossier": _validate_dossier, "governance-record": _validate_governance_record}
    report = validators[args.spec](args.subject, args.profile)
    print(report.to_json() if args.output == "json" else "", end="" if args.output == "json" else "") if args.output == "json" else _print_text(report)
    raise SystemExit(0 if report.conformant else 1)


def report_cmd() -> None:
    parser = argparse.ArgumentParser(prog="gc-report", description="Display a saved GC conformance report.")
    parser.add_argument("--output", default="text", choices=["text", "json"])
    parser.add_argument("report_file")
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.report_file).read_text(encoding="utf-8"))
        if data.get("gc_report_version") != GC_REPORT_VERSION:
            raise ValueError(
                f"report version '{data.get('gc_report_version')}' is not supported by this tool "
                f"(expected '{GC_REPORT_VERSION}')"
            )
        report = ConformanceReport(
            spec=data["spec"], spec_version=data["spec_version"], profile=data["profile"], subject=data["subject"],
            generated_at=data["generated_at"], rules=[RuleResult(**r) for r in data["rules"]],
            summary=ReportSummary(**data["summary"]), conformant=data["conformant"], conformance_level=data["conformance_level"],
        )
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"gc-report: malformed report file: {exc}", file=sys.stderr)
        raise SystemExit(2)
    print(report.to_json() if args.output == "json" else "") if args.output == "json" else _print_text(report)
    raise SystemExit(0 if report.conformant else 1)
