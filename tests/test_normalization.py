import unittest
from agent.normalization import normalize_email, normalize_name, is_valid_email

class Tests(unittest.TestCase):
    def test_email(self): self.assertEqual(normalize_email(" JANE@ACME.AI "), "jane@acme.ai")
    def test_name(self): self.assertEqual(normalize_name(" JANE   smith "), "Jane Smith")
    def test_validity(self):
        self.assertTrue(is_valid_email("jane@acme.ai"))
        self.assertFalse(is_valid_email("bad"))
if __name__ == "__main__": unittest.main()
