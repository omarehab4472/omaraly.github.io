import pandas as pd
from datetime import datetime

def load_transactions(path):
    df = pd.read_csv(path, parse_dates=["date"])
    # Ensure amount is numeric
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    # Normalize column names
    df.columns = [c.strip() for c in df.columns]
    return df

def add_features(df):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["weekday"] = df["date"].dt.weekday
    df["is_credit"] = df["amount"] > 0
    df["abs_amount"] = df["amount"].abs()
    return df
