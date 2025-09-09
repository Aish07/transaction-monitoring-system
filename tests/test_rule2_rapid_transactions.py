import unittest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import patch
from src.fraud_detection import flag_rapid_small_transactions

class TestRule2RapidSmallTransactions(unittest.TestCase):
    """
    Unit tests for Rule 2: Rapid Small Transactions
    """

    def setUp(self):
        base_time = datetime(2025, 9, 8, 10, 0)

        # Happy path: user has 5 transactions within 2 minutes
        self.happy_df = pd.DataFrame({
            "user_id": ["u1"] * 5,
            "timestamp": [
                (base_time + timedelta(seconds=i*30)) for i in range(5)
            ],
            "merchant_name": [f"Merchant{i}" for i in range(5)],
            "amount": [10*(i+1) for i in range(5)]
        })

        # Sad path: user has 4 transactions within 2 minutes (should NOT flag)
        self.sad_df = pd.DataFrame({
            "user_id": ["u2"] * 4,
            "timestamp": [
                (base_time + timedelta(seconds=i*30)) for i in range(4)
            ],
            "merchant_name": [f"Merchant{i}" for i in range(4)],
            "amount": [20*(i+1) for i in range(4)]
        })

    @patch("src.fraud_detection.load_transactions")
    def test_happy_path_rapid_transactions(self, mock_load):
        """Verify that transactions meeting the rapid threshold are flagged."""
        mock_load.return_value = self.happy_df
        flagged = flag_rapid_small_transactions("dummy.csv")
        self.assertEqual(len(flagged), 5)
        self.assertTrue(all(flagged["user_id"] == "u1"))

    @patch("src.fraud_detection.load_transactions")
    def test_sad_path_no_rapid_transactions(self, mock_load):
        """Verify that transactions below threshold are NOT flagged."""
        mock_load.return_value = self.sad_df
        flagged = flag_rapid_small_transactions("dummy.csv")
        self.assertEqual(len(flagged), 0)

if __name__ == "__main__":
    unittest.main()
