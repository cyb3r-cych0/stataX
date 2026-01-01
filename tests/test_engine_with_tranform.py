import pandas as pd
from statax.core.engine import run
from statax.config.schema import (
    Config, DataConfig, VariablesConfig,
    AnalysisConfig, OutputConfig, Transform
)

def test_engine_applies_transform(tmp_path):
    csv = tmp_path / "d.csv"
    csv.write_text("Y,Gender\n1,Male\n2,Female\n")

    config = Config(
        data=DataConfig(path=str(csv)),
        variables=VariablesConfig(outcome="Y", predictors=["Gender"]),
        analysis=AnalysisConfig(model="ols"),
        output=OutputConfig(),
        transforms=[
            Transform(
                type="recode",
                column="Gender",
                mapping={"Male": 1, "Female": 0}
            )
        ]
    )

    df = run(config)
    assert list(df["Gender"]) == [1, 0]
