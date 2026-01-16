import pandas as pd
from statax.core.stats import ols_with_data
from statax.artifacts.plot import PlotArtifact


def test_coef_plot_created(tmp_path):
    df = pd.DataFrame({
        "y": [1, 2, 3, 4, 5],
        "x": [1, 2, 3, 4, 5],
    })

    model, X, y = ols_with_data(
        df,
        outcome="y",
        predictors=["x"],
    )

    plot = PlotArtifact(
        artifact_id="coef_plot_test",
        kind="coef_plot",
        spec={"ci": 0.95},
    )

    out_dir = tmp_path / "plots"

    plot.render(
        df=df,
        model=model,
        cfg={
            "out_dir": out_dir,
            "formats": ["png"],
            "dpi": 100,
        },
        resolve=lambda x: x,
    )

    assert (out_dir / "coef_plot_test.png").exists()
