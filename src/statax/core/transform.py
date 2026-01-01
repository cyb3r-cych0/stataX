import pandas as pd

class TransformError(Exception):
    pass

def apply_transforms(df: pd.DataFrame, transforms: list) -> pd.DataFrame:
    out = df.copy()

    for t in transforms:
        if t.type == "recode":
            out = _recode(out, t.column, t.mapping)
        else:
            raise TransformError(f"Unsupported transform type: {t.type}")

    return out

def _recode(df: pd.DataFrame, column: str, mapping: dict) -> pd.DataFrame:
    if column not in df.columns:
        raise TransformError(f"Recode column not found: {column}")

    df[column] = df[column].apply(
        lambda x: mapping.get(x, x)
    )
    return df
