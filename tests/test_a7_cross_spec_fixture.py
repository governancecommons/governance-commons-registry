import json
from pathlib import Path

from governance_commons import bind_atp_audit_trail
from governance_commons.governance_records import validate_governance_record_data

FIXTURE = Path(__file__).parent / "fixtures" / "interop" / "a7-delegation-lifecycle.json"


def _trail_from_fixture() -> dict:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    entries = []
    hashes = [
        "a7" * 32,
        "b7" * 32,
        "c7" * 32,
        "d7" * 32,
        "e7" * 32,
    ]
    for seq, (event, digest) in enumerate(zip(fixture["events"], hashes), start=1):
        entries.append(
            {
                "seq": seq,
                "event_type": event["event_type"],
                "agent_id": event["agent_id"],
                "timestamp": event["timestamp"],
                "prev_hash": entries[-1]["hash"] if entries else None,
                "hash": digest,
                "payload": event["payload"],
            }
        )
    return {
        "trail_id": "trail:a7-interop-001",
        "task_id": fixture["task_id"],
        "participants": ["agent:orchestrator", "agent:reviewer"],
        "hash_algorithm": "sha256",
        "source_context": fixture["source"],
        "entries": entries,
    }


def test_a7_fixture_reaches_governance_record_boundary():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    records = bind_atp_audit_trail(_trail_from_fixture())

    assert len(records) == len(fixture["events"]) == 5
    assert [record["governance_context"]["source_event_type"] for record in records] == [
        event["event_type"] for event in fixture["events"]
    ]
    revoked = records[3]
    assert revoked["governance_context"]["source_event_type"] == "delegation.revoked"
    assert revoked["extensions"]["atp_audit_entry"]["payload"]["reason"] == "review_boundary_reached"

    for record in records:
        report = validate_governance_record_data(record)
        assert report.conformant, report.to_dict()


def test_a7_registry_binding_does_not_promote_atp_events_to_authority():
    records = bind_atp_audit_trail(_trail_from_fixture())
    for record in records:
        assert "authority" not in record
        assert "approval" not in record
        assert record["record_type"] == "provenance"
        assert record["provenance"]["method"] == "atp.shared-audit-event"
