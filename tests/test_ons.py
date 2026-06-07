"""Tests for governance_commons.ons — ONS Python reference implementation."""
from __future__ import annotations

import pytest

from governance_commons.ons import (
    CASING_RULES,
    ONS_SPEC_VERSION,
    SEPARATORS,
    detect_separator,
    detect_separators,
    get_casing_rule,
    list_domains,
    parse_governance_id,
    validate_cluster,
    validate_name,
)


# ── module-level invariants ───────────────────────────────────────────────────

class TestModuleInvariants:
    def test_ons_spec_version_is_semver(self) -> None:
        parts = ONS_SPEC_VERSION.split(".")
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)

    def test_casing_rules_nonempty(self) -> None:
        assert len(CASING_RULES) >= 12

    def test_separators_count(self) -> None:
        assert len(SEPARATORS) == 4

    def test_domain_index_covers_all_rules(self) -> None:
        domains = list_domains()
        assert len(domains) == len(CASING_RULES)
        for rule in CASING_RULES:
            assert rule.domain in domains


# ── validate_name ─────────────────────────────────────────────────────────────

class TestValidateName:
    @pytest.mark.parametrize("name", [
        "run_intent", "enforce_result", "_private", "x", "a1_b2",
    ])
    def test_valid_python_identifier(self, name: str) -> None:
        assert validate_name("python_identifier", name).valid

    @pytest.mark.parametrize("name", [
        "runIntent", "run-intent", "RunIntent", "RUN_INTENT",
    ])
    def test_invalid_python_identifier(self, name: str) -> None:
        result = validate_name("python_identifier", name)
        assert not result.valid
        assert result.violation is not None

    @pytest.mark.parametrize("name", ["NehiOrchestrator", "RunIntent", "A"])
    def test_valid_python_class(self, name: str) -> None:
        assert validate_name("python_class", name).valid

    @pytest.mark.parametrize("name", ["nehi_orchestrator", "nehi-orchestrator", "a"])
    def test_invalid_python_class(self, name: str) -> None:
        assert not validate_name("python_class", name).valid

    @pytest.mark.parametrize("name", ["PIPELINE_STEPS", "NEHI_API_VERSION", "X"])
    def test_valid_python_constant(self, name: str) -> None:
        assert validate_name("python_constant", name).valid

    @pytest.mark.parametrize("name", ["pipelineSteps", "pipeline-steps", "pipeline_steps"])
    def test_invalid_python_constant(self, name: str) -> None:
        assert not validate_name("python_constant", name).valid

    @pytest.mark.parametrize("name", ["--eco-color-primary", "--eco-space-sm"])
    def test_valid_css_custom_property(self, name: str) -> None:
        assert validate_name("css_custom_property", name).valid

    @pytest.mark.parametrize("name", ["--eco_color_primary", "eco-color-primary", "--x"])
    def test_invalid_css_custom_property(self, name: str) -> None:
        assert not validate_name("css_custom_property", name).valid

    @pytest.mark.parametrize("name", ["ONS.00", "NEHI.01", "GC.99", "AB.00"])
    def test_valid_governance_id(self, name: str) -> None:
        assert validate_name("governance_id", name).valid

    @pytest.mark.parametrize("name", ["ons.00", "ONS-00", "ONS.0", "O.00"])
    def test_invalid_governance_id(self, name: str) -> None:
        assert not validate_name("governance_id", name).valid

    @pytest.mark.parametrize("name", ["ONS", "LASSO", "GC", "AB"])
    def test_valid_governance_cluster(self, name: str) -> None:
        assert validate_name("governance_cluster", name).valid

    @pytest.mark.parametrize("name", ["ons", "O", "TOOLONGCLUSTER"])
    def test_invalid_governance_cluster(self, name: str) -> None:
        assert not validate_name("governance_cluster", name).valid

    @pytest.mark.parametrize("name", ["nehi_orchestrator.py", "run_intent.py", "a.py"])
    def test_valid_python_filename(self, name: str) -> None:
        assert validate_name("python_filename", name).valid

    @pytest.mark.parametrize("name", ["nehi-orchestrator.py", "NeHi.py"])
    def test_invalid_python_filename(self, name: str) -> None:
        assert not validate_name("python_filename", name).valid

    @pytest.mark.parametrize("name", ["ONS.00.md", "NEHI.01.md"])
    def test_valid_governance_filename(self, name: str) -> None:
        assert validate_name("governance_filename", name).valid

    @pytest.mark.parametrize("name", ["ons.00.md", "ONS.0.md", "ONS.00.txt"])
    def test_invalid_governance_filename(self, name: str) -> None:
        assert not validate_name("governance_filename", name).valid

    @pytest.mark.parametrize("name", ["cockpit-panel.ts", "validate.js", "my-tool.ts"])
    def test_valid_ts_js_filename(self, name: str) -> None:
        assert validate_name("ts_js_filename", name).valid

    @pytest.mark.parametrize("name", ["cockpit_panel.ts", "MyTool.ts", "validate.py"])
    def test_invalid_ts_js_filename(self, name: str) -> None:
        assert not validate_name("ts_js_filename", name).valid

    @pytest.mark.parametrize("name", ["platform-core", "passes", "my-dir", "a1"])
    def test_valid_directory_name(self, name: str) -> None:
        assert validate_name("directory_name", name).valid

    @pytest.mark.parametrize("name", ["PlatformCore", "platform_core", ""])
    def test_invalid_directory_name(self, name: str) -> None:
        assert not validate_name("directory_name", name).valid

    @pytest.mark.parametrize("name", ["AL:2", "AL:3", "GC:1"])
    def test_valid_qualification_authority(self, name: str) -> None:
        assert validate_name("qualification_authority", name).valid

    @pytest.mark.parametrize("name", ["al:2", "AL-2", "AL:two"])
    def test_invalid_qualification_authority(self, name: str) -> None:
        assert not validate_name("qualification_authority", name).valid

    @pytest.mark.parametrize("name", ["env:production", "env:staging", "time.loc:2026-06-06"])
    def test_valid_qualification_metadata(self, name: str) -> None:
        assert validate_name("qualification_metadata", name).valid

    @pytest.mark.parametrize("name", ["Env:production", "env_production", "ENV:production"])
    def test_invalid_qualification_metadata(self, name: str) -> None:
        assert not validate_name("qualification_metadata", name).valid

    def test_unknown_domain_returns_invalid(self) -> None:
        result = validate_name("nonexistent_domain", "anything")
        assert not result.valid
        assert "Unknown casing domain" in (result.violation or "")


# ── parse_governance_id ───────────────────────────────────────────────────────

class TestParseGovernanceId:
    @pytest.mark.parametrize("id_, cluster, seq", [
        ("ONS.00", "ONS", "00"),
        ("NEHI.01", "NEHI", "01"),
        ("GC.99", "GC", "99"),
        ("AB.00", "AB", "00"),
    ])
    def test_valid_id(self, id_: str, cluster: str, seq: str) -> None:
        result = parse_governance_id(id_)
        assert result.valid
        assert result.cluster == cluster
        assert result.seq == seq
        assert result.violation is None

    @pytest.mark.parametrize("id_", ["ons.00", "ONS-00", "O.00", "TOOLONGCLUSTER.00"])
    def test_invalid_id(self, id_: str) -> None:
        result = parse_governance_id(id_)
        assert not result.valid
        assert result.cluster is None
        assert result.violation is not None

    def test_missing_dot_separator(self) -> None:
        result = parse_governance_id("ONS00")
        assert not result.valid
        assert "dot separator" in (result.violation or "").lower() or "missing" in (result.violation or "").lower()

    def test_invalid_cluster_part(self) -> None:
        result = parse_governance_id("ons.00")
        assert not result.valid

    def test_invalid_seq_part(self) -> None:
        result = parse_governance_id("ONS.0")
        assert not result.valid


# ── validate_cluster ──────────────────────────────────────────────────────────

class TestValidateCluster:
    @pytest.mark.parametrize("cluster", ["ONS", "GC", "LASSO", "AB", "ABCDEF"])
    def test_valid_cluster(self, cluster: str) -> None:
        assert validate_cluster(cluster).valid

    @pytest.mark.parametrize("cluster", ["ons", "O", "TOOLONGCLUST", "123", ""])
    def test_invalid_cluster(self, cluster: str) -> None:
        result = validate_cluster(cluster)
        assert not result.valid
        assert result.violation is not None


# ── detect_separator ─────────────────────────────────────────────────────────

class TestDetectSeparator:
    def test_dot_returns_hierarchy(self) -> None:
        assert detect_separator("eco.ui.help") == "hierarchy"

    def test_hyphen_returns_compound(self) -> None:
        assert detect_separator("cockpit-panel") == "compound"

    def test_underscore_returns_lexical_binding(self) -> None:
        assert detect_separator("run_intent") == "lexical_binding"

    def test_colon_returns_qualification(self) -> None:
        assert detect_separator("AL:2") == "qualification"

    def test_no_separator_returns_none(self) -> None:
        assert detect_separator("simple") is None


# ── detect_separators ────────────────────────────────────────────────────────

class TestDetectSeparators:
    def test_single_separator(self) -> None:
        result = detect_separators("eco.ui.help")
        assert len(result) == 1
        assert result[0] == (".", "hierarchy")

    def test_multiple_separators(self) -> None:
        result = detect_separators("eco.ui_help")
        tokens = [r[0] for r in result]
        assert "." in tokens
        assert "_" in tokens

    def test_no_separator(self) -> None:
        assert detect_separators("simple") == []

    def test_all_four_separators(self) -> None:
        result = detect_separators("a.b-c_d:e")
        assert len(result) == 4


# ── get_casing_rule ───────────────────────────────────────────────────────────

class TestGetCasingRule:
    def test_known_domain_returns_rule(self) -> None:
        rule = get_casing_rule("python_identifier")
        assert rule is not None
        assert rule.domain == "python_identifier"
        assert rule.rule == "snake_case"

    def test_unknown_domain_returns_none(self) -> None:
        assert get_casing_rule("nonexistent") is None


# ── list_domains ──────────────────────────────────────────────────────────────

class TestListDomains:
    def test_returns_all_domains(self) -> None:
        domains = list_domains()
        assert len(domains) == len(CASING_RULES)

    def test_contains_expected_domains(self) -> None:
        domains = list_domains()
        for expected in [
            "python_identifier", "python_class", "python_constant",
            "css_custom_property", "governance_id", "governance_cluster",
        ]:
            assert expected in domains
