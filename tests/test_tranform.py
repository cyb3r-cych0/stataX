import pandas as pd
from statax.core.transform import apply_transforms
from statax.config.schema import Transform

def test_recode_basic():
    df = pd.DataFrame({"Gender": ["Male", "Female", "Other"]})

    transforms = [
        Transform(
            type="recode",
            column="Gender",
            mapping={"Male": 1, "Female": 0}
        )
    ]

    out = apply_transforms(df, transforms)

    assert list(out["Gender"]) == [1, 0, "Other"]
