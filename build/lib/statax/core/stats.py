import pandas as pd
import statsmodels.api as sm
from statax.core.missing import handle_missing
from statax.core.exceptions import RegressionError

def _prepare_xy(df: pd.DataFrame, outcome: str, predictors: list[str], missing_strategy: str):
    y = pd.to_numeric(df[outcome], errors="coerce")

    X = df[predictors].apply(
        lambda col: pd.to_numeric(col, errors="coerce")
    )

    X = sm.add_constant(X, has_constant="add")

    Xc, yc = handle_missing(X, y, missing_strategy)
    return Xc, yc

def ols(df, outcome, predictors, robust, missing_strategy):
    X, y = _prepare_xy(df, outcome, predictors, missing_strategy)
    model = sm.OLS(y, X).fit(cov_type="HC3" if robust else "nonrobust")
    return model, X, y

def logit(df, outcome, predictors, robust, missing_strategy):
    X, y = _prepare_xy(df, outcome, predictors, missing_strategy)
    if not set(y.dropna().unique()).issubset({0, 1}):
        raise RegressionError("Logit outcome must be binary (0/1)")
    model = sm.Logit(y, X).fit(disp=False)
    if robust:
        model = model.get_robustcov_results(cov_type="HC3")
    return model, X, y

