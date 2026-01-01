import pandas as pd
from statax.core.descriptives import frequency_table

def test_frequency_table():
    df = pd.DataFrame({"A": ["x", "x", "y"]})
    out = frequency_table(df, "A")
    assert out.loc["x", "count"] == 2
    assert round(out.loc["x", "percent"], 1) == 66.7
