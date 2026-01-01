import pandas as pd
from statax.core.exceptions import RegressionError

def handle_missing(X: pd.DataFrame, y: pd.Series, strategy: str):
    if strategy == "complete_case":
        combined = pd.concat([y, X], axis=1).dropna()
        if combined.empty:
            raise RegressionError("No complete cases available.")
        return combined.drop(columns=[y.name]), combined[y.name]

    if strategy == "drop_predictors_only":
        Xc = X.dropna()
        yc = y.loc[Xc.index]
        if Xc.empty:
            raise RegressionError("No rows with complete predictors.")
        return Xc, yc

    if strategy == "mean_impute_predictors":
        Xc = X.copy()
        for c in Xc.columns:
            if c != "const":
                Xc[c] = Xc[c].fillna(Xc[c].mean())
        valid = ~y.isna()
        Xf = Xc.loc[valid]
        yf = y.loc[valid]
        if Xf.empty:
            raise RegressionError("No valid outcome values.")
        return Xf, yf

    raise ValueError(f"Unknown missing strategy: {strategy}")
