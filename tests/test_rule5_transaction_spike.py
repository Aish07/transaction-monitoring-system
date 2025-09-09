import unittest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import patch
from src.fraud_detection import flag_transaction_spikes

class TestRule5TransactionSpikes(unittest.TestCase):
    """
    Unit tests for Rule 5: Unusually High Transaction Frequency
    Flags transactions if count in SPIKE_WINDOW_HOURS exceeds threshold.
    """

    def setUp(self):
        base_time = datetime(2025, 9, 8, 9, 0, 0)

        # Happy path: 5 transactions in 3 hours (spike)
        self.happy_df = pd.DataFrame({
            "user_id": ["u1"]*5,
            "timestamp": [
                base_time + timedelta(minutes=0),
                base_time + timedelta(minutes=30),
                base_time + timedelta(minutes=60),
                base_time + timedelta(minutes=90),
                base_time + timedelta(minutes=120)
            ],
            "merchant_name": ["M1"]*5,
            "amount": [10, 20, 30, 40, 50]
        })

        # Sad path: transactions spread out (normal frequency)
        self.sad_df = pd.DataFrame({
            "user_id": ["u2"]*5,
            "timestamp": [
                base_time + timedelta(hours=0),
                base_time + timedelta(hours=4),
                base_time + timedelta(hours=8),
                base_time + timedelta(hours=12),
                base_time + timedelta(hours=16)
            ],
            "merchant_name": ["M2"]*5,
            "amount": [15, 25, 35, 45, 55]
        })

        # Ensure timestamp is datetime
        self.happy_df["timestamp"] = pd.to_datetime(self.happy_df["timestamp"])
        self.sad_df["timestamp"] = pd.to_datetime(self.sad_df["timestamp"])

    @patch("src.fraud_detection.pd.read_csv")
    def test_happy_path_spike(self, mock_read):
        """Verify that transactions in a short window are flagged"""
        mock_read.return_value = self.happy_df
        flagged = flag_transaction_spikes("dummy.csv")
        self.assertEqual(len(flagged), 5)
        self.assertTrue(all(flagged["user_id"] == "u1"))

    @patch("src.fraud_detection.pd.read_csv")
    def test_sad_path_normal_frequency(self, mock_read):
        """Verify that normal transaction frequencies are NOT flagged"""
        mock_read.return_value = self.sad_df
        flagged = flag_transaction_spikes("dummy.csv")
        self.assertEqual(len(flagged), 0)

if __name__ == "__main__":
    unittest.main()
