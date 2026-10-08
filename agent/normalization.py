import re

def normalize_email(email):
    if not email: return None
    return email.strip().lower() or None

def is_valid_email(email):
    return bool(email and re.fullmatch(r"[^@\\s]+@[^@\\s]+\\.[^@\\s]+", email.strip()))

def normalize_name(name):
    if not name: return None
    return " ".join(name.strip().split()).title() or None

def normalize_attendee(record):
    r = dict(record)
    r["full_name"] = normalize_name(r.get("full_name") or r.get("name"))
    r["email"] = normalize_email(r.get("email"))
    r["company"] = " ".join(str(r["company"]).split()) if r.get("company") else None
    r["role"] = " ".join(str(r["role"]).split()) if r.get("role") else None
    r.setdefault("sources", [])
    r.setdefault("evidence", [])
    return r
