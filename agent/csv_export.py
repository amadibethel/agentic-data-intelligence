import csv
from pathlib import Path

def export_records(records, path):
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fields = ["full_name","email","company","role","status","confidence_score","email_valid",
              "identity_verified","company_verified","role_verified","sources","issues"]
    with dest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for r in records:
            row = dict(r)
            for k in ("sources","issues"):
                if isinstance(row.get(k), list): row[k] = " | ".join(map(str,row[k]))
            writer.writerow(row)
    return dest
