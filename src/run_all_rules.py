# run_all_rules.py
import argparse
from src.fraud_detection import (
    flag_high_value_transactions,
    flag_rapid_small_transactions,
    flag_same_merchant_transactions,
    flag_unusual_time_transactions,
    flag_transaction_spikes
)

def run_all_rules(csv_path: str):
    print(f"Processing file: {csv_path}\n")

    flagged_rule1 = flag_high_value_transactions(csv_path)
    print(f"Rule 1 - High-value transactions: {len(flagged_rule1)} flagged")
    print(flagged_rule1, "\n")

    flagged_rule2 = flag_rapid_small_transactions(csv_path)
    print(f"Rule 2 - Rapid small transactions: {len(flagged_rule2)} flagged")
    print(flagged_rule2, "\n")

    flagged_rule3 = flag_same_merchant_transactions(csv_path)
    print(f"Rule 3 - Same-merchant transactions: {len(flagged_rule3)} flagged")
    print(flagged_rule3, "\n")

    flagged_rule4 = flag_unusual_time_transactions(csv_path)
    print(f"Rule 4 - Unusual time transactions: {len(flagged_rule4)} flagged")
    print(flagged_rule4, "\n")

    flagged_rule5 = flag_transaction_spikes(csv_path)
    print(f"Rule 5 - High-frequency transactions: {len(flagged_rule5)} flagged")
    print(flagged_rule5, "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run all fraud detection rules on a CSV file.")
    parser.add_argument(
        "--file",
        type=str,
        default="data/input.csv",
        help="Path to CSV file (default: data/input.csv)"
    )
    args = parser.parse_args()
    run_all_rules(args.file)