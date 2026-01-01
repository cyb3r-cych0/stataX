import numpy as np
import pandas as pd

def regression_diagnostics(X, y, exog_names=None):
    # Ensure DataFrame
    if isinstance(X, np.ndarray):
        if exog_names is None:
            raise ValueError("exog_names required when X is ndarray")
        X = pd.DataFrame(X, columns=exog_names)

    notes = []

    # Drop constant for variance checks
    Xn = X.drop(columns=["const"], errors="ignore")

    # Zero variance checks
    if pd.Series(y).nunique(dropna=True) <= 1:
        notes.append("Outcome has zero variance after filtering.")

    for c in Xn.columns:
        if Xn[c].nunique(dropna=True) <= 1:
            notes.append(f"Predictor '{c}' has zero variance after filtering.")

    # Rank / singularity check
    try:
        rank = np.linalg.matrix_rank(X.values)
        if rank < X.shape[1]:
            notes.append("Design matrix is rank-deficient (perfect collinearity).")
    except Exception:
        pass

    return notes
