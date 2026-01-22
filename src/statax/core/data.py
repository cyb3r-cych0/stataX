import pandas as pd
from pathlib import Path

class DataError(Exception):
    pass

def load_csv(path, delimiter=",", missing_values=None, encoding="utf-8"):
    try:
        return pd.read_csv(
            path,
            delimiter=delimiter,
            na_values=missing_values,
            encoding=encoding,
        )
    except UnicodeDecodeError as e:
        raise DataError(
            f"Failed to decode CSV using encoding '{encoding}'. "
            "Try encoding='cp1252' or 'latin1'."
        ) from e

def validate_columns(df: pd.DataFrame, outcome: str, predictors: list[str]):
    missing = []
    for col in [outcome, *predictors]:
        if col not in df.columns:
            missing.append(col)

    if missing:
        raise DataError(f"Missing columns in CSV: {missing}")

def parse_dates(df, date_column):
    if date_column not in df.columns:
        raise DataError(f"Date column not found: {date_column}")

    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column], errors="coerce")

    if df[date_column].isna().all():
        raise DataError(f"Date column '{date_column}' could not be parsed")

    return df
