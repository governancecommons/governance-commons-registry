"""Minimal Governance Record adopter example.

Run from the repository root:
    python examples/python/governance_record_validation.py
"""
from pathlib import Path

from governance_commons.governance_records import validate_governance_record_contract

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "fixtures" / "governance-record" / "valid" / "authorized-action.json"


def main() -> int:
    report = validate_governance_record_contract(FIXTURE)
    print(report.to_json())
    return 0 if report.conformant else 1


if __name__ == "__main__":
    raise SystemExit(main())
