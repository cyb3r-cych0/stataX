import pandas as pd
from statax.core.stats import ols_with_data
import warnings


def test_interaction_added():
    warnings.filterwarnings("ignore", category=RuntimeWarning)

    df = pd.DataFrame({
        "y": [1, 2, 3, 4],
        "x1": [1, 2, 3, 4],
        "x2": [2, 3, 4, 5]
    })

    res, X, y = ols_with_data(
        df,
        outcome="y",
        predictors=["x1", "x2"],
        interactions=[("x1", "x2")],
    )

    assert "x1:x2" in X.columns


def test_fixed_effects_added():
    warnings.filterwarnings("ignore", category=RuntimeWarning)

    df = pd.DataFrame({
        "y": [1, 2, 3, 4],
        "x": [10, 20, 30, 40],
        "city": ["A", "B", "C", "D"],
    })

    res, X, y = ols_with_data(
        df,
        outcome="y",
        predictors=["x"],
        fixed_effects=["city"],
    )

    assert any(c.startswith("city_") for c in X.columns)


def test_interactions_and_fe_together():
    warnings.filterwarnings("ignore", category=RuntimeWarning)

    df = pd.DataFrame({
        "y": [1, 2, 3, 4],
        "x1": [1, 2, 3, 4],
        "x2": [2, 3, 4, 5],
        "city": ["A", "A", "B", "B"],
    })

    res, X, y = ols_with_data(
        df,
        "y",
        ["x1", "x2"],
        interactions=[("x1", "x2")],
        fixed_effects=["city"],
    )

    assert "x1:x2" in X.columns
    assert any(c.startswith("city_") for c in X.columns)


def test_complete_case_drops_rows():
    warnings.filterwarnings("ignore", category=RuntimeWarning)

    df = pd.DataFrame({
        "y": [1, None, 3],
        "x": [1, 2, None],
    })

    _, X, y = ols_with_data(
        df,
        "y",
        ["x"],
        missing_strategy="complete_case",
    )

    assert len(X) == 1


def test_mean_impute_predictors_keeps_rows():
    df = pd.DataFrame({
        "y": [1, 2, 3],
        "x": [1, None, 3],
    })

    _, X, y = ols_with_data(
        df,
        "y",
        ["x"],
        missing_strategy="mean_impute_predictors",
    )

    assert len(X) == 3


def test_drop_predictors_only():
    warnings.filterwarnings("ignore", category=RuntimeWarning)

    df = pd.DataFrame({
        "y": [1, 2, 3],
        "x": [1, None, 3],
    })

    _, X, y = ols_with_data(
        df,
        "y",
        ["x"],
        missing_strategy="drop_predictors_only",
    )

    assert y.notnull().all()
