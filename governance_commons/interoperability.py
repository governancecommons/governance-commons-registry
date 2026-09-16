"""Cross-spec bindings into the Governance Record boundary.

This module does not create a competing ATP audit store. It converts an ATP
shared-audit trail into durable Governance Record-shaped provenance records,
preserving the originating event, hash-chain evidence, task identity, and
source-system ownership.
"""
from __future__ import annotations

from typing import Any


def _ref(ref_type: str, identifier: str) -> dict[str, str]:
    return {"type": ref_type, "id": identifier}


def bind_atp_audit_trail(trail: dict[str, Any]) -> list[dict[str, Any]]:
    """Bind an ATP shared-audit trail to the Governance Record boundary.

    Each ATP audit entry becomes one ``provenance`` Governance Record. The
    binding is intentionally provenance-only: ATP remains authoritative for
    fleet-level audit semantics, while Governance Record remains the durable
    governed-event/evidence boundary. No authority, approval, or handoff
    transfer is inferred from an ATP audit entry that does not contain it.
    """
    if not isinstance(trail, dict):
        raise TypeError("ATP audit trail must be a mapping")

    trail_id = trail.get("trail_id")
    task_id = trail.get("task_id")
    participants = trail.get("participants", [])
    entries = trail.get("entries")
    if not isinstance(trail_id, str) or not trail_id:
        raise ValueError("ATP audit trail requires trail_id")
    if not isinstance(task_id, str) or not task_id:
        raise ValueError("ATP audit trail requires task_id")
    if not isinstance(participants, list) or not all(isinstance(item, str) for item in participants):
        raise ValueError("ATP audit trail participants must be a list of strings")
    if not isinstance(entries, list):
        raise ValueError("ATP audit trail requires entries")

    records: list[dict[str, Any]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("ATP audit trail entries must be mappings")
        seq = entry.get("seq")
        event_type = entry.get("event_type")
        agent_id = entry.get("agent_id")
        timestamp = entry.get("timestamp")
        entry_hash = entry.get("hash")
        if not isinstance(seq, int) or seq < 1:
            raise ValueError("ATP audit entry requires a positive integer seq")
        if not isinstance(event_type, str) or not event_type:
            raise ValueError("ATP audit entry requires event_type")
        if not isinstance(agent_id, str) or not agent_id:
            raise ValueError("ATP audit entry requires agent_id")
        if not isinstance(timestamp, str) or not timestamp:
            raise ValueError("ATP audit entry requires timestamp")
        if not isinstance(entry_hash, str) or not entry_hash:
            raise ValueError("ATP audit entry requires hash")

        record = {
            "record_id": f"governance-record:atp:{trail_id}:{seq}",
            "record_type": "provenance",
            "schema_version": "1.0.0",
            "subject": _ref("task", task_id),
            "actor": _ref("agent", agent_id),
            "provenance": {
                "source": _ref("atp-audit-trail", trail_id),
                "method": "atp.shared-audit-event",
            },
            "timestamps": {
                "created_at": timestamp,
                "occurred_at": timestamp,
            },
            "relations": [
                {"type": "derived_from", "target": _ref("atp-audit-entry", f"{trail_id}:{seq}")},
            ],
            "governance_context": {
                "source_system": "agent-team-protocol",
                "source_event_type": event_type,
                "audit_sequence": seq,
                "audit_hash": entry_hash,
                "previous_audit_hash": entry.get("prev_hash"),
                "participants": participants,
            },
            "extensions": {
                "atp_audit_entry": entry,
            },
        }
        records.append(record)
    return records
