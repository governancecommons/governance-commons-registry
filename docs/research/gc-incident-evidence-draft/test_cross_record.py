"""Adversarial tests for experimental incident cross-record integrity."""
import copy
import json
from pathlib import Path
from cross_record import cross_record_issues

ROOT = Path(__file__).resolve().parent
report = json.loads((ROOT / "fixtures/valid-minimal.json").read_text(encoding="utf-8"))
report["response_actions"][0]["status"] = "completed"
report["review"] = {"status": "approved", "reviewer": {"type": "human", "id": "alice"}, "governance_record": {"type": "governance-record", "id": "gr-approval"}}
report["disclosure"] = {"classification": "public", "publication_status": "approved_for_release"}

action = {
    "record_id": "gr-001", "record_type": "action", "schema_version": "1.0.0",
    "actor": {"type": "human", "id": "alice"},
    "subject": {"type": "incident", "id": "example-001"},
    "timestamps": {"created_at": "2026-10-19T09:00:00Z", "occurred_at": "2026-10-19T10:00:00Z"},
    "authority": {"basis": "human_authorization", "authority_id": "auth-001", "status": "active", "granted_at": "2026-10-19T09:00:00Z"},
    "approval": {"required": True, "status": "approved", "approver": {"type": "human", "id": "alice"}, "scope": "incident response", "timestamp": "2026-10-19T09:30:00Z"},
    "action": {"type": "pause", "status": "completed"}
}
approval = {
    "record_id": "gr-approval", "record_type": "approval", "schema_version": "1.0.0",
    "actor": {"type": "human", "id": "alice"},
    "subject": {"type": "incident", "id": "example-001"},
    "timestamps": {"created_at": "2026-10-19T10:00:00Z", "occurred_at": "2026-10-19T10:00:00Z"},
    "approval": {"required": True, "status": "approved", "approver": {"type": "human", "id": "alice"}, "scope": "incident review", "timestamp": "2026-10-19T10:00:00Z"}
}
records = {"gr-001": action, "gr-approval": approval}


def check(name, mutate, expected):
    candidate = copy.deepcopy(records)
    incident = copy.deepcopy(report)
    mutate(incident, candidate)
    problems = cross_record_issues(incident, candidate)
    observed = not problems
    print(f'{"PASS" if observed == expected else "FAIL"} {name}: expected_valid={expected}, observed_valid={observed}; issues={problems}')
    assert observed == expected, name


check("valid-authorized-evidence", lambda r, d: None, True)
check("unresolved-record", lambda r, d: d.pop("gr-001"), False)
check("mismatched-record-id", lambda r, d: d["gr-001"].update(record_id="wrong"), False)
check("action-without-authority", lambda r, d: d["gr-001"]["authority"].update(status="pending"), False)
check("revoked-authority", lambda r, d: d["gr-001"]["authority"].update(status="revoked", revoked_at="2026-10-19T09:30:00Z"), False)
check("action-before-grant", lambda r, d: d["gr-001"]["authority"].update(granted_at="2026-10-19T11:00:00Z"), False)
check("required-approval-pending", lambda r, d: d["gr-001"]["approval"].update(status="pending"), False)
check("unapproved-response", lambda r, d: d["gr-001"]["action"].update(status="proposed"), False)
check("incomplete-response", lambda r, d: d["gr-001"]["action"].update(status="authorized"), False)
check("wrong-incident-subject", lambda r, d: d["gr-001"]["subject"].update(id="different"), False)
check("wrong-record-type", lambda r, d: d["gr-001"].update(record_type="observation"), False)
check("reviewer-mismatch", lambda r, d: d["gr-approval"]["approval"]["approver"].update(id="bob"), False)
check("review-status-mismatch", lambda r, d: d["gr-approval"]["approval"].update(status="rejected"), False)
check("review-subject-mismatch", lambda r, d: d["gr-approval"]["subject"].update(id="different"), False)
check("invalid-record-schema", lambda r, d: d["gr-001"].pop("actor"), False)
print("14 cross-record cases matched expectations. No real-world provenance or OECD conformance implied.")
