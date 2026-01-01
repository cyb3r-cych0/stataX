import pandas as pd

class DescriptiveError(Exception):
    pass

def summary_table(df: pd.DataFrame) -> pd.DataFrame:
    numeric = df.select_dtypes(include="number")
    non_numeric = df.select_dtypes(exclude="number")

    tables = []

    if not numeric.empty:
        num_summary = (
            numeric.describe()
            .transpose()[["count", "mean", "std", "min", "max"]]
        )
        tables.append(("Numeric variables", num_summary))

    if not non_numeric.empty:
        non_num_summary = (
            non_numeric.describe()
            .transpose()[["count", "unique"]]
        )
        tables.append(("Non-numeric variables", non_num_summary))

    return tables

def grouped_summary(df: pd.DataFrame, group_by: str) -> pd.DataFrame:
    if group_by not in df.columns:
        raise DescriptiveError(f"Group column not found: {group_by}")

    return df.groupby(group_by).describe().transpose()

def frequency_table(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if column not in df.columns:
        raise DescriptiveError(f"Frequency column not found: {column}")

    counts = df[column].value_counts(dropna=False)
    perc = counts / counts.sum() * 100

    return pd.DataFrame({
        "count": counts,
        "percent": perc.round(2)
    })
