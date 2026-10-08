import unittest
from agent.deduplication import deduplicate_attendees

class Tests(unittest.TestCase):
    def test_merge(self):
        rows,n=deduplicate_attendees([{"full_name":"Jane Smith","email":"JANE@ACME.AI","sources":["Calendar"]},{"full_name":"Jane Smith","email":"jane@acme.ai","sources":["Gmail"]}])
        self.assertEqual(len(rows),1); self.assertEqual(n,1); self.assertIn("Gmail",rows[0]["sources"])
    def test_no_email_not_merged(self):
        rows,n=deduplicate_attendees([{"full_name":"Jane Smith"},{"full_name":"Jane Smith"}])
        self.assertEqual(len(rows),2); self.assertEqual(n,0)
if __name__ == "__main__": unittest.main()
