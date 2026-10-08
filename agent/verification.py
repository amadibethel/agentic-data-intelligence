from agent.normalization import is_valid_email, normalize_attendee

def verify_attendee(record, evidence=None):
    row = normalize_attendee(record)
    ev = evidence or {}
    checks = {
        "email_valid": is_valid_email(row.get("email")),
        "identity_verified": bool(ev.get("identity_supported")),
        "company_verified": bool(ev.get("company_supported")),
        "role_verified": bool(ev.get("role_supported")),
        "external_source_found": bool(ev.get("external_source_found")),
    }
    contradictions = list(ev.get("contradictions") or [])
    score = (15 if checks["email_valid"] else 0) + (20 if checks["identity_verified"] else 0) + (25 if checks["company_verified"] else 0) + (25 if checks["role_verified"] else 0) + (10 if checks["external_source_found"] else 0) + (5 if not contradictions else 0)
    if contradictions: status = "CONFLICT"
    elif score >= 90 and checks["identity_verified"] and checks["company_verified"]: status = "VERIFIED"
    elif score >= 50: status = "PARTIALLY_VERIFIED"
    else: status = "UNVERIFIED"
    missing = [k for k in ("full_name","email","company","role") if not row.get(k)]
    issues = list(row.get("issues") or []) + contradictions
    if not checks["email_valid"]: issues.append("Email missing or invalid")
    if missing: issues.append("Missing fields: " + ", ".join(missing))
    if not checks["external_source_found"]: issues.append("No external evidence found")
    return {**row, **checks, "status":status, "confidence_score":score,
            "sources":list(dict.fromkeys((row.get("sources") or []) + (ev.get("sources") or []))),
            "issues":list(dict.fromkeys(issues))}
