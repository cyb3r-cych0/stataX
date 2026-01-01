import pandas as pd
from typing import Optional


class TransformError(Exception):
    pass

def apply_transforms(df: pd.DataFrame, transforms: Optional[list]) -> pd.DataFrame:
    out = df.copy()

    for t in transforms or []:
        if t.type == "recode":
            mapping = getattr(t, "mapping", {}) or {}
            if not isinstance(mapping, dict):
                raise TransformError("Transform mapping must be a dict")
            out = _recode(out, t.column, mapping)
        else:
            raise TransformError(f"Unsupported transform type: {t.type}")

    return out

def _recode(df: pd.DataFrame, column: str, mapping: dict) -> pd.DataFrame:
    if column not in df.columns:
        raise TransformError(f"Recode column not found: {column}")

    s = df[column].map(mapping).where(
        df[column].map(mapping).notna(),
        df[column]
    )
    df[column] = s.infer_objects(copy=False)
    return df
