"""Tests for governance_commons.report — GC conformance report format (GC-2-C-01)."""
from __future__ import annotations

import json

import pytest

from governance_commons.report import (
    GC_REPORT_VERSION,
    ConformanceReport,
    RuleResult,
    build_report,
)


# ── module-level invariants ───────────────────────────────────────────────────

class TestConstants:
    def test_gc_report_version_is_semver(self) -> None:
        parts = GC_REPORT_VERSION.split(".")
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)

    def test_gc_report_version_is_1_0_0(self) -> None:
        assert GC_REPORT_VERSION == "1.0.0"


# ── build_report: all-pass ────────────────────────────────────────────────────

class TestBuildReportAllPass:
    def _rules(self) -> list[RuleResult]:
        return [
            RuleResult("ONS-CASING-001", "Python identifiers must be snake_case", "pass"),
            RuleResult("ONS-SEP-001", "Names must not mix separator semantics", "pass"),
        ]

    def test_conformant_true(self) -> None:
        report = build_report(spec="ons", spec_version="1.4.0", profile="standard",
                              subject="my.yaml", rules=self._rules())
        assert report.conformant is True

    def test_conformance_level_matches_profile(self) -> None:
        for profile in ("advisory", "standard", "strict"):
            report = build_report(spec="ons", spec_version="1.4.0", profile=profile,
                                  subject="my.yaml", rules=self._rules())
            assert report.conformance_level == profile

    def test_summary_counts(self) -> None:
        report = build_report(spec="ons", spec_version="1.4.0", profile="standard",
                              subject="my.yaml", rules=self._rules())
        assert report.summary.total == 2
        assert report.summary.passed == 2
        assert report.summary.failed == 0
        assert report.summary.skipped == 0

    def test_gc_report_version_set(self) -> None:
        report = build_report(spec="ons", spec_version="1.4.0", profile="standard",
                              subject="my.yaml", rules=self._rules())
        assert report.gc_report_version == GC_REPORT_VERSION


# ── build_report: with failures ───────────────────────────────────────────────

class TestBuildReportWithFailures:
    def _rules(self) -> list[RuleResult]:
        return [
            RuleResult("ONS-CASING-001", "Python identifiers must be snake_case", "pass"),
            RuleResult("ONS-SEP-001", "Names must not mix separator semantics", "fail",
                       message='"eco.ui_help" mixes hierarchy and lexical_binding'),
        ]

    def test_conformant_false(self) -> None:
        report = build_report(spec="ons", spec_version="1.4.0", profile="standard",
                              subject="my.yaml", rules=self._rules())
        assert report.conformant is False

    def test_conformance_level_none(self) -> None:
        report = build_report(spec="ons", spec_version="1.4.0", profile="strict",
                              subject="my.yaml", rules=self._rules())
        assert report.conformance_level == "none"

    def test_summary_counts(self) -> None:
        report = build_report(spec="ons", spec_version="1.4.0", profile="standard",
                              subject="my.yaml", rules=self._rules())
        assert report.summary.total == 2
        assert report.summary.passed == 1
        assert report.summary.failed == 1
        assert report.summary.skipped == 0


# ── build_report: with skips ──────────────────────────────────────────────────

class TestBuildReportWithSkips:
    def _rules(self) -> list[RuleResult]:
        return [
            RuleResult("ONS-CASING-001", "Python identifiers must be snake_case", "pass"),
            RuleResult("ONS-CLUSTER-001", "Cluster names must be 2–6 uppercase letters", "skip",
                       message="No cluster declarations found in subject"),
        ]

    def test_conformant_true_when_only_skips(self) -> None:
        report = build_report(spec="ons", spec_version="1.4.0", profile="standard",
                              subject="my.yaml", rules=self._rules())
        assert report.conformant is True

    def test_summary_skipped_count(self) -> None:
        report = build_report(spec="ons", spec_version="1.4.0", profile="standard",
                              subject="my.yaml", rules=self._rules())
        assert report.summary.skipped == 1
        assert report.summary.total == 2


# ── build_report: empty rules ─────────────────────────────────────────────────

class TestBuildReportEmpty:
    def test_empty_rules_conformant(self) -> None:
        report = build_report(spec="ons", spec_version="1.4.0", profile="advisory",
                              subject="empty.yaml", rules=[])
        assert report.conformant is True
        assert report.summary.total == 0

    def test_empty_rules_conformance_level(self) -> None:
        report = build_report(spec="ons", spec_version="1.4.0", profile="advisory",
                              subject="empty.yaml", rules=[])
        assert report.conformance_level == "advisory"


# ── generated_at ─────────────────────────────────────────────────────────────

class TestGeneratedAt:
    def test_default_generated_at_is_iso8601(self) -> None:
        from datetime import datetime
        report = build_report(spec="ons", spec_version="1.4.0", profile="standard",
                              subject="x.yaml", rules=[])
        dt = datetime.fromisoformat(report.generated_at.replace("Z", "+00:00"))
        assert dt.year >= 2026

    def test_explicit_generated_at_preserved(self) -> None:
        ts = "2026-06-07T00:00:00Z"
        report = build_report(spec="ons", spec_version="1.4.0", profile="standard",
                              subject="x.yaml", rules=[], generated_at=ts)
        assert report.generated_at == ts


# ── serialisation ─────────────────────────────────────────────────────────────

class TestSerialisation:
    def _report(self) -> ConformanceReport:
        return build_report(
            spec="ons",
            spec_version="1.4.0",
            profile="standard",
            subject="test.yaml",
            generated_at="2026-06-07T00:00:00Z",
            rules=[
                RuleResult("ONS-CASING-001", "snake_case identifiers", "pass"),
                RuleResult("ONS-SEP-001", "No mixed separators", "fail", message="mixed"),
            ],
        )

    def test_to_dict_has_required_keys(self) -> None:
        d = self._report().to_dict()
        for key in ("gc_report_version", "spec", "spec_version", "profile", "subject",
                    "generated_at", "rules", "summary", "conformant", "conformance_level"):
            assert key in d, f"Missing key: {key}"

    def test_to_json_is_valid_json(self) -> None:
        parsed = json.loads(self._report().to_json())
        assert parsed["spec"] == "ons"
        assert parsed["gc_report_version"] == "1.0.0"

    def test_to_dict_summary_structure(self) -> None:
        d = self._report().to_dict()
        assert d["summary"]["total"] == 2
        assert d["summary"]["passed"] == 1
        assert d["summary"]["failed"] == 1

    def test_to_dict_rules_structure(self) -> None:
        d = self._report().to_dict()
        assert len(d["rules"]) == 2
        assert d["rules"][0]["result"] == "pass"
        assert d["rules"][1]["message"] == "mixed"
