from src.utils import load_transactions
import pandas as pd
import numpy as np

# Rule 1: High-Value Transactions Threshold
HIGH_VALUE_THRESHOLD = 7000  # Transactions above this amount are flagged as suspicious

# Rule 3: Same-Merchant Transactions Threshold
SAME_MERCHANT_THRESHOLD = 3       # Transactions
SAME_MERCHANT_WINDOW_SEC = 90     # 90 seconds window

# Rule 4: Unusual Time-of-Day
STD_MULTIPLIER = 2  # Transactions outside mean ± 2*std hours are flagged

# Rule 5: User-Specific High-Value Transactions
SPIKE_WINDOW_HOURS = 3          # window to check for spikes
SPIKE_MULTIPLIER = 2            # threshold multiplier over average transactions/hour
MIN_TX_IN_WINDOW = 3            # minimum transactions in a window to consider it a spike


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


def flag_unusual_time_transactions(csv_path: str) -> pd.DataFrame:
    """
    Flags transactions occurring at unusual times for each user.

    Parameters:
        csv_path (str): Path to CSV with columns: user_id, timestamp, merchant_name, amount.

    Returns:
        pd.DataFrame: Transactions flagged for unusual time-of-day.
    """
    df = load_transactions(csv_path)

    # Ensure timestamp column is datetime type
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Extract transaction hour (0-23) as float
    df["hour"] = df["timestamp"].dt.hour.astype(float)

    flagged_indices = []

    # Group by user
    for user, group in df.groupby("user_id"):
        hours = group["hour"]
        if len(hours) < 2:
            continue  # Not enough data to compute deviation
        mean_hour = hours.mean()
        std_hour = hours.std(ddof=0)  # use population std for consistency
        lower = mean_hour - STD_MULTIPLIER * std_hour
        upper = mean_hour + STD_MULTIPLIER * std_hour

        # Flag transactions outside typical range
        outlier_mask = (hours < lower) | (hours > upper)
        flagged_indices.extend(group.index[outlier_mask].tolist())

    flagged = df.loc[sorted(set(flagged_indices))]
    return flagged


def flag_transaction_spikes(csv_path: str) -> pd.DataFrame:
    """
    Flags transactions that exceed a user’s typical frequency.
    A sliding time window (e.g., 3 hours) is used, and
    transactions are flagged if the count in the window
    is at least twice the user’s average transactions per hour.

    Parameters:
        csv_path (str): Path to CSV with columns: user_id, timestamp, merchant_name, amount.

    Returns:
        pd.DataFrame: Transactions flagged for unusually high frequency.
    """
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by=["user_id", "timestamp"])

    flagged_indices = []

    for user, group in df.groupby("user_id"):
        times = group["timestamp"].tolist()
        n = len(times)
        if n < MIN_TX_IN_WINDOW:
            continue  # not enough data to form a spike

        # compute average transactions per hour
        total_hours = max((max(times) - min(times)).total_seconds() / 3600, 1)
        avg_tx_per_hour = n / total_hours
        threshold = SPIKE_MULTIPLIER * avg_tx_per_hour

        start = 0
        for end in range(n):
            while (times[end] - times[start]).total_seconds() / 3600 > SPIKE_WINDOW_HOURS:
                start += 1
            window_count = end - start + 1
            if window_count >= threshold and window_count >= MIN_TX_IN_WINDOW:
                flagged_indices.extend(group.iloc[start:end+1].index.tolist())

    return df.loc[sorted(set(flagged_indices))]


if __name__ == "__main__":
    # Example usage
    flagged_transactions = flag_high_value_transactions("data/input.csv")
    print("High-value transactions flagged:")
    print(flagged_transactions)
