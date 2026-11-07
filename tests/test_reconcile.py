import unittest
from decimal import Decimal
from reconcile.cli import reconcile

class ReconcileTests(unittest.TestCase):
    def test_match(self):
        self.assertEqual(reconcile({"1":[Decimal("10.00")]},{"1":[Decimal("10")]})[0]["status"], "matched")
    def test_mismatch(self):
        self.assertEqual(reconcile({"1":[Decimal("10")]},{"1":[Decimal("9")]})[0]["status"], "amount_mismatch")
    def test_missing(self):
        self.assertEqual(reconcile({"1":[Decimal("10")]}, {})[0]["status"], "missing_in_right")
    def test_duplicate(self):
        self.assertEqual(reconcile({"1":[Decimal("10"),Decimal("10")]},{"1":[Decimal("20")]})[0]["status"], "duplicate_id")

if __name__ == "__main__":
    unittest.main()
