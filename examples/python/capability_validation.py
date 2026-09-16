"""Minimal Capability Contract adopter example.

Run from the repository root:
    python examples/python/capability_validation.py
"""
from pathlib import Path

from governance_commons.capabilities import validate_capability_contract

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "fixtures" / "capabilities.valid.yaml"


def main() -> int:
    result = validate_capability_contract(FIXTURE)
    if result.valid:
        print("Capability Contract v0.1: PASS")
        return 0
    for issue in result.issues:
        print(f"FAIL [{issue.rule_id}] {issue.path}: {issue.message}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
