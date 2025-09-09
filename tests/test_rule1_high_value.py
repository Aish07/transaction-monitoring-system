import unittest
import pandas as pd
from io import StringIO
from unittest.mock import patch
from src.fraud_detection import flag_high_value_transactions, HIGH_VALUE_THRESHOLD

class TestRule1HighValueTransactions(unittest.TestCase):
    def setUp(self):
        # Happy path: transactions above threshold
        self.happy_df = pd.DataFrame({
            "user_id": ["u1", "u2"],
            "timestamp": ["2025-01-01 10:00:00", "2025-01-02 12:00:00"],
            "merchant_name": ["Rolex Boutique", "Jewellery World"],
            "amount": [8000, 12000]
        })

        # Sad path: transactions below threshold
        self.sad_df = pd.DataFrame({
            "user_id": ["u3", "u4"],
            "timestamp": ["2025-01-03 15:00:00", "2025-01-04 16:00:00"],
            "merchant_name": ["Walmart", "Target"],
            "amount": [50, 200]
        })

    @patch("src.fraud_detection.load_transactions")
    def test_happy_path_high_value(self, mock_load):
        mock_load.return_value = self.happy_df
        flagged = flag_high_value_transactions("dummy.csv")
        self.assertEqual(len(flagged), 2)
        self.assertTrue(all(flagged["amount"] > HIGH_VALUE_THRESHOLD))

    @patch("src.fraud_detection.load_transactions")
    def test_sad_path_no_high_value(self, mock_load):
        mock_load.return_value = self.sad_df
        flagged = flag_high_value_transactions("dummy.csv")
        self.assertEqual(len(flagged), 0)

if __name__ == "__main__":
    unittest.main()
