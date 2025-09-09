import unittest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import patch
from src.fraud_detection import flag_same_merchant_transactions

class TestRule3SameMerchantTransactions(unittest.TestCase):
    """
    Unit tests for Rule 3: Repeated Same-Merchant Transactions
    Threshold: 3 transactions at the same merchant within 90 seconds
    """

    def setUp(self):
        base_time = datetime(2025, 9, 8, 10, 0)

        # Happy path: 3 transactions at same merchant within 90 seconds
        self.happy_df = pd.DataFrame({
            "user_id": ["u1"] * 3,
            "timestamp": [
                base_time + timedelta(seconds=i*30) for i in range(3)  # 0s, 30s, 60s
            ],
            "merchant_name": ["MerchantA"] * 3,
            "amount": [10, 20, 30]
        })

        # Sad path: spaced out or different merchants
        self.sad_df = pd.DataFrame({
            "user_id": ["u2", "u2", "u2"],
            "timestamp": [
                base_time + timedelta(seconds=i*61) for i in range(3)  # 0s, 61s, 122s
            ],
            "merchant_name": ["MerchantA", "MerchantB", "MerchantC"],
            "amount": [10, 20, 30]
        })

        # Extra edge case: overlapping windows (4 transactions in 90s)
        self.edge_df = pd.DataFrame({
            "user_id": ["u3"] * 4,
            "timestamp": [
                base_time + timedelta(seconds=i*30) for i in range(4)  # 0s, 30s, 60s, 90s
            ],
            "merchant_name": ["MerchantX"] * 4,
            "amount": [5, 15, 25, 35]
        })

    @patch("src.fraud_detection.load_transactions")
    def test_happy_path_same_merchant(self, mock_load):
        """3 transactions at same merchant within 90s should be flagged"""
        mock_load.return_value = self.happy_df
        flagged = flag_same_merchant_transactions("dummy.csv")
        self.assertEqual(len(flagged), 3)
        self.assertTrue(all(flagged["user_id"] == "u1"))
        self.assertTrue(all(flagged["merchant_name"] == "MerchantA"))

    @patch("src.fraud_detection.load_transactions")
    def test_sad_path_no_flag(self, mock_load):
        """Transactions spaced out >90s or at different merchants are NOT flagged"""
        mock_load.return_value = self.sad_df
        flagged = flag_same_merchant_transactions("dummy.csv")
        self.assertEqual(len(flagged), 0)

    @patch("src.fraud_detection.load_transactions")
    def test_edge_case_overlapping_windows(self, mock_load):
        """
        Overlapping windows: 4 transactions in 90s
        All 4 transactions should be flagged because windows overlap
        """
        mock_load.return_value = self.edge_df
        flagged = flag_same_merchant_transactions("dummy.csv")
        self.assertEqual(len(flagged), 4)
        self.assertTrue(all(flagged["user_id"] == "u3"))
        self.assertTrue(all(flagged["merchant_name"] == "MerchantX"))

if __name__ == "__main__":
    unittest.main()
