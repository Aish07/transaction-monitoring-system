from src.utils import load_transactions
import pandas as pd

# Rule 1: High-Value Transactions Threshold
HIGH_VALUE_THRESHOLD = 7000  # Transactions above this amount are flagged as suspicious

def flag_high_value_transactions(csv_path: str) -> pd.DataFrame:
    """
    Flags transactions that exceed a high-value threshold.

    Parameters:
        csv_path (str): Path to the input CSV file containing transactions.
                        CSV must have columns: user_id, timestamp, merchant_name, amount.

    Returns:
        pd.DataFrame: A DataFrame containing all transactions where amount > HIGH_VALUE_THRESHOLD.

    Logic:
        - Transactions over $7,000 are considered high-risk.
        - This rule focuses on absolute amount, independent of user history.
        - Provides a first-pass filter for potential fraud review.

    Example:
        flagged = flag_high_value_transactions("data/input.csv")
        print(flagged)
    """
    # Load transactions using the utility function
    df = load_transactions(csv_path)

    # Filter transactions above the threshold
    flagged = df[df["amount"] > HIGH_VALUE_THRESHOLD]

    # Return the flagged transactions
    return flagged


if __name__ == "__main__":
    # Example usage
    flagged_transactions = flag_high_value_transactions("data/input.csv")
    print("High-value transactions flagged:")
    print(flagged_transactions)
