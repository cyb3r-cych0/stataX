import pandas as pd
from statax.core.missing import handle_missing

def test_complete_case():
    X = pd.DataFrame({"const":[1,1,1], "x":[1,None,3]})
    y = pd.Series([1,2,None], name="y")
    Xc, yc = handle_missing(X, y, "complete_case")
    assert len(Xc) == 1

def test_mean_impute_predictors():
    X = pd.DataFrame({"const":[1,1,1], "x":[1,None,3]})
    y = pd.Series([1,2,3], name="y")
    Xc, yc = handle_missing(X, y, "mean_impute_predictors")
    assert Xc.isna().sum().sum() == 0
