import pandas as pd
from statax.core.stats import ols

def test_ols_runs():
    df = pd.DataFrame({
        "y": [1, 2, 3, 4],
        "x": [10, 20, 30, 40]
    })
    model = ols(df, "y", ["x"], robust=True)
    assert "x" in model.params.index
