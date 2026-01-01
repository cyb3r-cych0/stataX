import pandas as pd
from statax.core.engine import run
from statax.config.schema import (
    Config, DataConfig, VariablesConfig,
    AnalysisConfig, OutputConfig, Transform
)

import pandas as pd
from statax.core.transform import apply_transforms
from statax.config.schema import Transform

def test_apply_recode_transform():
    df = pd.DataFrame({
        "Gender": ["Male", "Female"]
    })

    transforms = [
        Transform(
            type="recode",
            column="Gender",
            mapping={"Male": 1, "Female": 0}
        )
    ]

    out = apply_transforms(df, transforms)

    assert list(out["Gender"]) == [1, 0]

