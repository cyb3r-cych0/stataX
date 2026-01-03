import pandas as pd
from statax.core.data import DataError

def inspect_columns(path: str):
    try:
        df = pd.read_csv(path, nrows=0)
    except FileNotFoundError:
        raise DataError(f"CSV not found: {path}")

    cols = list(df.columns)
    print(f"Columns ({len(cols)}):")
    for c in cols:
        print(f"- {c}")

def inspect_types(path: str):
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise DataError(f"CSV not found: {path}")

    print("Column types:")
    for col in df.columns:
        dtype = df[col].dtype
        non_null = df[col].notna().sum()
        print(f"- {col}: {dtype} (non-null: {non_null})")

def inspect_missing(path: str):
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise DataError(f"CSV not found: {path}")

    n = len(df)
    print("Missing values:")
    for col in df.columns:
        miss = df[col].isna().sum()
        pct = (miss / n * 100) if n else 0
        print(f"- {col}: {miss} ({pct:.2f}%)")
