import unittest
from rag.query_transform import transform_query

class Tests(unittest.TestCase):
    def test_support_attribute(self):
        p=transform_query("Which product has priority support?")
        self.assertIn("support",p.attributes)
    def test_preserve_question(self):
        q="Which products integrate with Paystack?"
        self.assertEqual(transform_query(q).original_question,q)
if __name__ == "__main__": unittest.main()
