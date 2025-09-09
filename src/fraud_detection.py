from src.utils import load_transactions
import pandas as pd

# Rule 1: High-Value Transactions Threshold
HIGH_VALUE_THRESHOLD = 7000  # Transactions above this amount are flagged as suspicious

# Rule 3: Same-Merchant Transactions Threshold
SAME_MERCHANT_THRESHOLD = 3       # Transactions
SAME_MERCHANT_WINDOW_SEC = 90     # 90 seconds window

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


def flag_rapid_small_transactions(csv_path: str) -> pd.DataFrame:
    """
    Flags users who make 5 or more transactions within a 2-minute window.
    Designed for live/continuous fraud monitoring.

    Parameters:
        csv_path (str): Path to the input CSV file.

    Returns:
        pd.DataFrame: All transactions that are part of rapid small transaction bursts.

    Logic:
        - Fixed 2-minute window for rapid detection.
        - Threshold of 5 transactions within window triggers a flag.
    """
    df = load_transactions(csv_path)
    df = df.sort_values(by=["user_id", "timestamp"])
    
    window_minutes = 2
    transaction_count_threshold = 5
    flagged_indices = []

    for user, user_df in df.groupby("user_id"):
        timestamps = user_df["timestamp"].tolist()
        n = len(timestamps)
        start = 0
        
        for end in range(n):
            # Move start pointer forward if outside the window
            while (timestamps[end] - timestamps[start]).total_seconds() / 60 > window_minutes:
                start += 1
            # Flag if window has threshold or more transactions
            if (end - start + 1) >= transaction_count_threshold:
                flagged_indices.extend(user_df.iloc[start:end+1].index.tolist())

    flagged = df.loc[sorted(set(flagged_indices))]
    return flagged


def flag_same_merchant_transactions(csv_path: str) -> pd.DataFrame:
    """
    Flags transactions where a user makes 3 or more transactions
    at the same merchant within a 90-second window.

    Parameters:
        csv_path (str): Path to the CSV containing transactions.
                        CSV must have columns: user_id, timestamp, merchant_name, amount.

    Returns:
        pd.DataFrame: All flagged transactions.
    """
    df = load_transactions(csv_path)
    df = df.sort_values(by=["user_id", "merchant_name", "timestamp"])
    
    flagged_indices = []

    # Group by user and merchant
    for (user, merchant), group in df.groupby(["user_id", "merchant_name"]):
        timestamps = group["timestamp"].tolist()
        n = len(timestamps)
        start = 0
        
        for end in range(n):
            # Move start pointer if outside the 90-second window
            while (timestamps[end] - timestamps[start]).total_seconds() > SAME_MERCHANT_WINDOW_SEC:
                start += 1
            if (end - start + 1) >= SAME_MERCHANT_THRESHOLD:
                flagged_indices.extend(group.iloc[start:end+1].index.tolist())

    flagged = df.loc[sorted(set(flagged_indices))]
    return flagged


if __name__ == "__main__":
    # Example usage
    flagged_transactions = flag_high_value_transactions("data/input.csv")
    print("High-value transactions flagged:")
    print(flagged_transactions)
