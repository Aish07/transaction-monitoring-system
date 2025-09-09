import unittest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import patch
from src.fraud_detection import flag_unusual_time_transactions

class TestRule4UnusualTimeTransactions(unittest.TestCase):
    """
    Unit tests for Rule 4: Unusual Time-of-Day Transactions
    Flags transactions outside mean ± 2*std of user transaction hours.
    """

    def setUp(self):
        base_date = datetime(2025, 9, 8)

        # Happy path: transaction at unusual hour (3 AM)
        self.happy_df = pd.DataFrame({
            "user_id": ["u1"] * 5 + ["u1"],
            "timestamp": [
                base_date + timedelta(hours=9),
                base_date + timedelta(hours=10),
                base_date + timedelta(hours=11),
                base_date + timedelta(hours=10),
                base_date + timedelta(hours=9),
                base_date + timedelta(hours=3)  # unusual
            ],
            "merchant_name": ["M1"]*6,
            "amount": [10, 20, 30, 40, 50, 60]
        })

        # Sad path: all transactions within typical hours
        self.sad_df = pd.DataFrame({
            "user_id": ["u2"] * 5,
            "timestamp": [
                base_date + timedelta(hours=9),
                base_date + timedelta(hours=10),
                base_date + timedelta(hours=11),
                base_date + timedelta(hours=10),
                base_date + timedelta(hours=9)
            ],
            "merchant_name": ["M2"]*5,
            "amount": [15, 25, 35, 45, 55]
        })

        # Ensure timestamp column is datetime
        self.happy_df["timestamp"] = pd.to_datetime(self.happy_df["timestamp"])
        self.sad_df["timestamp"] = pd.to_datetime(self.sad_df["timestamp"])

    @patch("src.fraud_detection.load_transactions")
    def test_happy_path_unusual_time(self, mock_load):
        """Verify that transactions at unusual hours are flagged"""
        mock_load.return_value = self.happy_df
        flagged = flag_unusual_time_transactions("dummy.csv")
        self.assertEqual(len(flagged), 1)
        self.assertEqual(flagged.iloc[0]["timestamp"].hour, 3)
        self.assertTrue(all(flagged["user_id"] == "u1"))

    @patch("src.fraud_detection.load_transactions")
    def test_sad_path_normal_hours(self, mock_load):
        """Verify that transactions within typical hours are NOT flagged"""
        mock_load.return_value = self.sad_df
        flagged = flag_unusual_time_transactions("dummy.csv")
        self.assertEqual(len(flagged), 0)

if __name__ == "__main__":
    unittest.main()
