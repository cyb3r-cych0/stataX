import pandas as pd
import statsmodels.api as sm
from statax.core.missing import handle_missing
from statax.core.exceptions import RegressionError


def labeled_params(res, columns):
    return pd.Series(res.params, index=columns)

def labeled_bse(res, columns):
    return pd.Series(res.bse, index=columns)


def add_fixed_effects(df, fixed_effects):
    df = df.copy()
    fe_cols = []
    for col in fixed_effects:
        dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
        if dummies.empty:
            print(f"Skipping fixed effect '{col}' (single category)")
            continue
        df = pd.concat([df, dummies], axis=1)
        fe_cols.extend(dummies.columns.tolist())
    return df, fe_cols


def add_interactions(df, interactions):
    df = df.copy()
    cols = []
    for a, b in interactions:
        if not pd.api.types.is_numeric_dtype(df[a]) or not pd.api.types.is_numeric_dtype(df[b]):
            raise RegressionError("Interaction requires numeric variables")
        name = f"{a}:{b}"
        df[name] = df[a] * df[b]
        cols.append(name)
    return df, cols


def _prepare_xy(
    df: pd.DataFrame,
    outcome: str,
    predictors: list[str],
    interactions: list[tuple[str, str]],
    fixed_effects: list[str],
    missing_strategy: str,
):
    if df.empty:
        raise RegressionError("Dataset is empty.")

    y = pd.to_numeric(df[outcome], errors="coerce")
    if y.dropna().empty:
        raise RegressionError("Outcome has no valid numeric observations.")

    X = df[predictors].apply(lambda col: pd.to_numeric(col, errors="coerce"))
    if X.dropna(how="all").empty:
        raise RegressionError("Predictors have no valid numeric observations.")

    zero_var = [c for c in X.columns if X[c].nunique(dropna=True) <= 1]
    if zero_var:
        raise RegressionError(f"Predictors have zero variance: {zero_var}")

    if interactions:
        df, inter_cols = add_interactions(df, interactions)
        X = df[predictors + inter_cols]

    if fixed_effects:
        df, fe_cols = add_fixed_effects(df, fixed_effects)
        X = df[X.columns.tolist() + fe_cols]

    # Force numeric
    X = X.apply(pd.to_numeric, errors="coerce")
    y = pd.to_numeric(y, errors="coerce")

    # missing strategy
    X, y = handle_missing(X, y, missing_strategy)

    X = sm.add_constant(X, has_constant="add")

    return X.astype(float), y.astype(float)


# Public simple API used by tests: returns only the fitted model object.
def ols(
        df,
        outcome,
        predictors,
        *,
        interactions=None,
        fixed_effects=None,
        robust=False,
):
    interactions = interactions or []
    fixed_effects = fixed_effects or []
    missing_strategy = "complete_case"

    Xc, yc = _prepare_xy(
        df,
        outcome,
        predictors,
        interactions,
        fixed_effects,
        missing_strategy
    )

    model = sm.OLS(yc, Xc).fit(
        cov_type="HC3" if robust else "nonrobust"
    )

    return model


# Full API for callers that need X and y (engine.run needs these for diagnostics)
def ols_with_data(
        df,
        outcome,
        predictors,
        interactions=None,
        fixed_effects=None,
        *,
        robust=True,
        cluster=None,
        missing_strategy="complete_case"
):
    interactions = interactions or []
    fixed_effects = fixed_effects or []

    Xc, yc = _prepare_xy(
        df,
        outcome,
        predictors,
        interactions,
        fixed_effects,
        missing_strategy
    )

    res = sm.OLS(yc, Xc).fit()

    if cluster is not None:
        groups = df.loc[Xc.index, cluster]
        res = res.get_robustcov_results(cov_type="cluster", groups=groups)
    elif robust:
        res = res.get_robustcov_results(cov_type="HC3")

    return res, Xc, yc


# Logit: simple API
def logit(
        df,
        outcome,
        predictors,
        *,
        interactions=None,
        fixed_effects=None,
        robust=False,
):
    interactions = interactions or []
    fixed_effects = fixed_effects or []
    missing_strategy = "complete_case"

    Xc, yc = _prepare_xy(
        df,
        outcome,
        predictors,
        interactions,
        fixed_effects,
        missing_strategy
    )

    if not set(yc.dropna().unique()).issubset({0, 1}):
        raise RegressionError("Logit outcome must be binary (0/1)")

    model = sm.Logit(yc, Xc).fit(disp=False)

    if robust:
        model = model.get_robustcov_results(cov_type="HC3")

    return model


# Full logit API returning model, X, y
def logit_with_data(
        df,
        outcome,
        predictors,
        interactions=None,
        fixed_effects=None,
        *,
        robust=True,
        cluster=None,
        missing_strategy="complete_case"
):
    interactions = interactions or []
    fixed_effects = fixed_effects or []

    Xc, yc = _prepare_xy(
        df,
        outcome,
        predictors,
        interactions,
        fixed_effects,
        missing_strategy,
    )

    if not set(yc.dropna().unique()).issubset({0, 1}):
        raise RegressionError("Logit outcome must be binary (0/1)")

    res = sm.Logit(yc, Xc).fit(disp=False)

    if cluster is not None:
        groups = df.loc[Xc.index, cluster]
        res = res.get_robustcov_results(cov_type="cluster", groups=groups)
    elif robust:
        res = res.get_robustcov_results(cov_type="HC3")

    return res, Xc, yc
