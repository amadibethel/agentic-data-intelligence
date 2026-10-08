from agent.deduplication import deduplicate_attendees
from agent.verification import verify_attendee
from agent.csv_export import export_records

def main():
    raw = [
      {"full_name":"JANE SMITH","email":"JANE@ACME.AI","company":"Acme AI","role":"Head of Engineering","sources":["Calendar","Gmail"]},
      {"full_name":"Jane Smith","email":"jane@acme.ai","company":"Acme AI","role":"Head of Engineering","sources":["Gmail"]},
      {"full_name":"Michael Okoro","email":"michael@example.org","company":"Example Org","role":"CTO","sources":["Calendar","Gmail"]},
      {"full_name":"Unknown Attendee","email":"bad-email","company":None,"role":None,"sources":["Calendar"]},
    ]
    rows, dupes = deduplicate_attendees(raw)
    evidence = {
      "jane@acme.ai":{"identity_supported":True,"company_supported":True,"role_supported":True,"external_source_found":True,"sources":["Official team page"],"contradictions":[]},
      "michael@example.org":{"identity_supported":True,"company_supported":True,"role_supported":False,"external_source_found":True,"sources":["Public directory"],"contradictions":["Email says CTO; public directory says Senior Engineer"]},
    }
    results = [verify_attendee(r, evidence.get(r.get("email"), {})) for r in rows]
    out = export_records(results, "outputs/attendee-verification-demo.csv")
    print("Duplicates merged:", dupes)
    for r in results: print(r.get("full_name"), "|", r["status"], "|", r["confidence_score"])
    print("CSV:", out.resolve())

if __name__ == "__main__": main()
