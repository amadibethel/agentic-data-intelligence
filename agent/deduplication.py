from agent.normalization import normalize_attendee

def deduplicate_attendees(records):
    by_email, no_email, duplicates = {}, [], 0
    for raw in records:
        r = normalize_attendee(raw)
        email = r.get("email")
        if not email:
            no_email.append(r)
            continue
        if email not in by_email:
            by_email[email] = r
            continue
        duplicates += 1
        target = by_email[email]
        for key in ("sources", "evidence", "issues"):
            target[key] = list(dict.fromkeys((target.get(key) or []) + (r.get(key) or [])))
        for key in ("full_name", "company", "role"):
            if not target.get(key) and r.get(key): target[key] = r[key]
            elif target.get(key) and r.get(key) and target[key] != r[key]:
                target.setdefault("issues", []).append(f"Conflicting {key}: {target[key]} vs {r[key]}")
    return list(by_email.values()) + no_email, duplicates
