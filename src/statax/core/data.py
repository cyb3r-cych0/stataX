import pandas as pd
from pathlib import Path

class DataError(Exception):
    pass

def load_csv(path: str, delimiter: str, missing_values: list[str]) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise DataError(f"CSV not found: {path}")

    df = pd.read_csv(
        p,
        delimiter=delimiter,
        na_values=missing_values,
        encoding="utf-8"
    )

    if df.columns.duplicated().any():
        raise DataError("Duplicate column names detected")

    return df

def validate_columns(df: pd.DataFrame, outcome: str, predictors: list[str]):
    missing = []
    for col in [outcome, *predictors]:
        if col not in df.columns:
            missing.append(col)

    if missing:
        raise DataError(f"Missing columns in CSV: {missing}")
