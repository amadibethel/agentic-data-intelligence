import unittest
from agent.verification import verify_attendee

class Tests(unittest.TestCase):
    def test_verified(self):
        r=verify_attendee({"full_name":"Jane Smith","email":"jane@acme.ai","company":"Acme","role":"Engineer"},{"identity_supported":True,"company_supported":True,"role_supported":True,"external_source_found":True})
        self.assertEqual(r["status"],"VERIFIED"); self.assertEqual(r["confidence_score"],100)
    def test_conflict(self):
        r=verify_attendee({"full_name":"Michael","email":"m@example.org","company":"Example","role":"CTO"},{"contradictions":["Role conflict"]})
        self.assertEqual(r["status"],"CONFLICT")
    def test_unverified(self):
        r = verify_attendee({"full_name": "A Person", "email": "bad"}, {})
        self.assertEqual(r["status"],"UNVERIFIED")
if __name__ == "__main__": unittest.main()
