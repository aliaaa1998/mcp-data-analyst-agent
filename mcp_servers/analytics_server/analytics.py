from __future__ import annotations

import pandas as pd


def calculate_growth(values: list[float]) -> dict:
    if len(values) < 2:
        return {"growth_pct": 0.0}
    base = values[0] or 1e-9
    return {"growth_pct": ((values[-1] - values[0]) / base) * 100}


def compare_periods(current: float, previous: float) -> dict:
    delta = current - previous
    pct = (delta / previous * 100) if previous else 0.0
    return {"delta": delta, "delta_pct": pct}


def summarize_dataset(rows: list[dict]) -> dict:
    df = pd.DataFrame(rows)
    return {"row_count": len(df), "columns": list(df.columns), "numeric_summary": df.describe(include="all").fillna("").to_dict()}


def detect_anomalies(values: list[float], threshold_std: float = 2.0) -> dict:
    s = pd.Series(values)
    mu = s.mean()
    std = s.std() or 1e-9
    anomalies = [i for i, v in enumerate(values) if abs((v - mu) / std) >= threshold_std]
    return {"mean": mu, "std": std, "anomaly_indices": anomalies}
