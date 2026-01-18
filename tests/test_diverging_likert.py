import pandas as pd
from statax.output.plot_renderers import diverging_likert

def test_diverging_likert_runs(tmp_path):
    df = pd.DataFrame({
        "x": [1, 2, 3, 4, 5, 5, 4, 3],
        "g": ["A", "A", "A", "B", "B", "B", "B", "B"],
    })

    cfg = {
        "out_dir": tmp_path,
        "formats": ["png"],
        "dpi": 100,
    }

    spec = {
        "scale": [1, 2, 3, 4, 5],
        "center": 3,
        "normalize": True,
    }

    diverging_likert(df, "x", spec, cfg, "test_plot", group_by="g")

    assert any(tmp_path.iterdir())
