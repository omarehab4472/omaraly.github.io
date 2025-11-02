import numpy as np
import pandas as pd

def zscore_anomalies(df, column="amount", threshold=3.0):
    """
    Simple z-score anomaly detector. Flags rows where z-score of the column exceeds threshold.
    """
    s = df[column]
    mu = s.mean()
    sigma = s.std(ddof=0) if s.std(ddof=0) != 0 else 1e-9
    z = (s - mu) / sigma
    res = df.copy()
    res["z_score"] = z
    res["anomaly_zscore"] = z.abs() > threshold
    return res.sort_values("z_score", key=abs, ascending=False)

def iqr_anomalies(df, column="amount", k=1.5):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    res = df.copy()
    res["anomaly_iqr"] = (df[column] < lower) | (df[column] > upper)
    return res
