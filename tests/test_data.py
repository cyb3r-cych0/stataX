import pandas as pd
from statax.core.data import validate_columns

def test_missing_column_raises():
    df = pd.DataFrame({"a": [1]})
    try:
        validate_columns(df, "y", ["x"])
    except Exception as e:
        assert "Missing columns" in str(e)
