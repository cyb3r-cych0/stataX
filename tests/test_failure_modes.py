import pandas as pd
import pytest
from statax.core.stats import ols
from statax.core.exceptions import RegressionError
from statax.core.stats import logit
from statax.core.engine import run
from statax.config.loader import load_config
from statax.core.data import DataError


def test_empty_dataset_fails():
    df = pd.DataFrame()
    with pytest.raises(RegressionError, match="Dataset is empty"):
        ols(df, "y", ["x"])


def test_outcome_all_missing_fails():
    df = pd.DataFrame({
        "y": [None, None],
        "x": [1, 2],
    })
    with pytest.raises(RegressionError, match="Outcome has no valid"):
        ols(df, "y", ["x"])


def test_predictors_all_missing_fails():
    df = pd.DataFrame({
        "y": [1, 2, 3],
        "x": [None, None, None],
    })
    with pytest.raises(RegressionError, match="Predictors have no valid"):
        ols(df, "y", ["x"])


def test_zero_variance_predictor_fails():
    df = pd.DataFrame({
        "y": [1, 2, 3],
        "x": [5, 5, 5],
    })
    with pytest.raises(RegressionError, match="zero variance"):
        ols(df, "y", ["x"])


def test_interaction_requires_numeric():
    df = pd.DataFrame({
        "y": [1, 2, 3],
        "x1": [1, 2, 3],
        "x2": [1, 2, 3],
    })

    df["x2"] = df["x2"].astype(str)

    with pytest.raises(RegressionError, match="Interaction requires numeric"):
        ols(
            df,
            "y",
            ["x1", "x2"],
            interactions=[("x1", "x2")],
        )


def test_logit_requires_binary_outcome():
    df = pd.DataFrame({
        "y": [0, 1, 2],
        "x": [1, 2, 3],
    })
    with pytest.raises(RegressionError, match="binary"):
        logit(df, "y", ["x"])


def test_cluster_single_group_fails(tmp_path):
    csv = tmp_path / "d.csv"
    csv.write_text("y,x,grp\n1,1,A\n2,2,A\n3,3,A\n")

    yaml = tmp_path / "a.yaml"
    yaml.write_text(
        f"""
        data:
          path: "{csv.as_posix()}"
        variables:
          outcome: y
          predictors: [x]
        analysis:
          model: ols
          cluster:
            by: grp
        """
            )

    config = load_config(yaml)
    with pytest.raises(DataError, match="at least 2 groups"):
        run(config)
