import pandas as pd

def summary_stats(df):
    total_tx = len(df)
    total_volume = df["amount"].sum()
    avg_amount = df["amount"].mean()
    median_amount = df["amount"].median()
    by_category = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    return {
        "total_transactions": total_tx,
        "total_volume": total_volume,
        "avg_amount": avg_amount,
        "median_amount": median_amount,
        "by_category": by_category
    }

def monthly_trends(df):
    s = df.set_index("date").resample("M")["amount"].sum().rename("monthly_amount")
    return s
