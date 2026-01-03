import pandas as pd
import warnings
from statax.core.stats import ols, ols_with_data
from statax.output.regression import regression_table


def test_ols_runs():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)

        df = pd.DataFrame({
            "y": [1, 2, 3, 4],
            "x": [10, 20, 30, 40],
            "city": ["A", "B", "C", "D"]
        })

        model = ols(
            df,
            "y",
            ["x"],
            fixed_effects=["city"],
        )

        reg = regression_table(model)
        assert any("city_" in idx for idx in reg.index)


def test_clustered_se_runs():
    df = pd.DataFrame({
        "y": range(20),
        "x": range(20),
        "city": ["A"] * 10 + ["B"] * 10,
    })

    res, X_used, _ = ols_with_data(
        df,
        "y",
        ["x"],
        fixed_effects=["city"],
        cluster="city",
    )

    assert hasattr(res, "cov_params")
    assert any("city_" in col for col in X_used.columns)
