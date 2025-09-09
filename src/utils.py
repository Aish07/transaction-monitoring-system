import pandas as pd

REQUIRED_COLUMNS = ["user_id", "timestamp", "merchant_name", "amount"]

def load_transactions(csv_path: str) -> pd.DataFrame:
    """
    Load transactions CSV and parse timestamps.
    """
    df = pd.read_csv(csv_path, usecols=REQUIRED_COLUMNS)
    df["timestamp"] = pd.to_datetime(df["timestamp"], infer_datetime_format=True)
    return df
