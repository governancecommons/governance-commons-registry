"""Acceptance tests for the APO -> ATP -> Governance Record boundary."""
from __future__ import annotations

import json
from pathlib import Path

from governance_commons import bind_atp_audit_trail
from governance_commons.governance_records import validate_governance_record_data

FIXTURE = Path(__file__).parent / "fixtures" / "interop" / "apo-handoff-sequence.json"


def _atp_trail_from_fixture() -> dict:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    entries = []
    hashes = [
        "b94119bed57e6dcbdd5f394e9516b5468a48123f19d6ea531051028c2467313d",
        "6f138403bb68eb65eec8f57359d91bf241740e82cfaf843cfe4dc5d7cc8fbed8",
        "99d3c5fb0b11c20748d7b2eea60d37bb1f0bc11019f1953faf792809333e0a0f",
    ]
    event_types = ["handoff.issued", "handoff.accepted", "escalation.triggered"]
    for seq, (event, event_type, digest) in enumerate(zip(fixture["events"], event_types, hashes), start=1):
        payload = {
            "task_id": event["task_id"],
            "trace_id": None,
            "source_event_id": event["event_id"],
            "summary": event["summary"],
        }
        if "handoff_envelope" in event:
            envelope = event["handoff_envelope"]
            payload.update(
                {
                    "handoff_id": envelope["envelope_id"],
                    "from_agent_id": envelope["from_agent"],
                    "to_agent_id": envelope["to_agent"],
                }
            )
        if "reason" in event:
            payload["reason"] = event["reason"]
        entries.append(
            {
                "seq": seq,
                "event_type": event_type,
                "agent_id": event["agent_id"],
                "timestamp": event["timestamp"],
                "prev_hash": entries[-1]["hash"] if entries else None,
                "hash": digest,
                "payload": payload,
            }
        )
    return {
        "trail_id": "trail:interop-001",
        "task_id": fixture["task_id"],
        "participants": fixture["participants"],
        "hash_algorithm": "sha256",
        "source_context": {
            "source": fixture["source"],
            "matrix_binding": fixture["matrix_binding"],
        },
        "entries": entries,
    }


def test_atp_interoperability_fixture_binds_to_governance_record_boundary() -> None:
    trail = _atp_trail_from_fixture()
    records = bind_atp_audit_trail(trail)

    assert len(records) == 3
    assert [record["record_type"] for record in records] == ["provenance"] * 3
    assert [record["governance_context"]["source_event_type"] for record in records] == [
        "handoff.issued",
        "handoff.accepted",
        "escalation.triggered",
    ]
    assert records[0]["governance_context"]["source_context"]["matrix_binding"]["route_owner"] == "agent-matrix"
    assert records[0]["extensions"]["atp_audit_entry"]["payload"]["handoff_id"].startswith("agent_handoff:")
    assert records[2]["extensions"]["atp_audit_entry"]["payload"]["reason"] == "requires_human_review"

    for record in records:
        report = validate_governance_record_data(record)
        assert report.conformant, report.to_dict()


def test_binding_does_not_infer_authority_or_handoff_transfer() -> None:
    record = bind_atp_audit_trail(_atp_trail_from_fixture())[1]

    assert "authority" not in record
    assert "approval" not in record
    assert "handoff" not in record
    assert record["record_type"] == "provenance"
    assert record["provenance"]["method"] == "atp.shared-audit-event"
