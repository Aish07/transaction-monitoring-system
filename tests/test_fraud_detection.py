import unittest
import pandas as pd
from io import StringIO
from src.fraud_detection import flag_high_value_transactions

class TestRule1HighValueTransactions(unittest.TestCase):
    """
    Unit tests for Rule 1: High-Value Transactions
    
    This class tests both the happy path (transactions above threshold)
    and the sad path (transactions below threshold) to ensure correctness.
    """

    def setUp(self):
        """
        Prepare in-memory CSV data using StringIO for testing.
        - happy_csv: Transactions that should be flagged
        - sad_csv: Transactions that should NOT be flagged
        """
        self.happy_csv = StringIO(
            """user_id,timestamp,merchant_name,amount
            u1,2025-01-01 10:00:00,Rolex Boutique,8000
            u2,2025-01-02 12:00:00,Jewellery World,12000"""
        )
        
        self.sad_csv = StringIO(
            """user_id,timestamp,merchant_name,amount
            u3,2025-01-03 15:00:00,Walmart,50
            u4,2025-01-04 16:00:00,Target,200"""
        )

    def test_happy_path_high_value(self):
        """
        Happy Path:
        Verify that transactions exceeding $7000 are flagged.
        - Expected: Both transactions in happy_csv should be flagged.
        """
        df = pd.read_csv(self.happy_csv, parse_dates=["timestamp"])
        flagged = df[df["amount"] > 7000]
        self.assertEqual(len(flagged), 2)
        self.assertTrue(all(flagged["amount"] > 7000))

    def test_sad_path_no_high_value(self):
        """
        Sad Path:
        Verify that transactions below $7000 are NOT flagged.
        - Expected: No transactions in sad_csv should be flagged.
        """
        df = pd.read_csv(self.sad_csv, parse_dates=["timestamp"])
        flagged = df[df["amount"] > 7000]
        self.assertEqual(len(flagged), 0)

if __name__ == "__main__":
    # Run all tests in this module
    unittest.main()
