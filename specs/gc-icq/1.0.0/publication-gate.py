"""GC–ICQ.01 publication decision (standalone reference, no SDK registration)."""
from datetime import datetime, timezone

SENSITIVE = {"PERSONAL_DATA", "CREDENTIAL", "EMBARGOED", "PROPRIETARY", "SECURITY_FINDING", "OTHER_SENSITIVE"}
QUADRANTS = {("high", "restricted"): "Q1", ("low", "restricted"): "Q2", ("low", "open"): "Q3", ("high", "open"): "Q4"}

def may_publish(record):
    """Fail closed; classification does not replace schema validation."""
    if not isinstance(record, dict) or record.get("specVersion") != "1.0.0":
        return False
    if QUADRANTS.get((record.get("impact"), record.get("access"))) != record.get("quadrant"):
        return False
    labels = record.get("dataLabels")
    if not isinstance(labels, list) or any(not isinstance(x, str) for x in labels):
        return False
    if set(labels) & SENSITIVE:
        return False
    approval = record.get("publication")
    return (
        record.get("impact") == "low"
        and record.get("access") == "open"
        and isinstance(approval, dict)
        and approval.get("status") == "approved"
        and isinstance(approval.get("approvedBy"), str)
        and bool(approval["approvedBy"].strip())
        and isinstance(approval.get("approvalRecordId"), str)
        and bool(approval["approvalRecordId"].strip())
    )

def q4_exception_valid(record, now=None):
    """Controlled-disclosure exception only; never a public publication override."""
    if record.get("quadrant") != "Q4" or "CREDENTIAL" in record.get("dataLabels", []):
        return False
    e = record.get("exception")
    if not isinstance(e, dict) or not all(e.get(k) for k in ("authority", "rationale", "expiresAt", "mitigations")):
        return False
    try:
        expiry = datetime.fromisoformat(e["expiresAt"].replace("Z", "+00:00"))
        return expiry.tzinfo is not None and expiry > (now or datetime.now(timezone.utc)) and isinstance(e["mitigations"], list) and len(e["mitigations"]) > 0
    except (TypeError, ValueError, AttributeError):
        return False
