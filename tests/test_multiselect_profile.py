import pandas as pd
from pathlib import Path

from statax.output.plot_renderers import multiselect_profile


def test_multiselect_profile_creates_plot(tmp_path: Path):
    # Minimal fake multiselect data (semicolon-separated)
    df = pd.DataFrame({
        "Q13": [
            "Social Media;Television",
            "Television",
            "Scientific publications;NGOs",
            "Social Media;Scientific publications",
            None,
        ]
    })

    spec = {
        "column": "Q13",
        "separator": ";",
        "top_n": 5,
        "normalize": True,
    }

    cfg = {
        "out_dir": tmp_path,
        "formats": ["png"],
        "dpi": 100,
    }

    name = "test_multiselect_profile"

    multiselect_profile(df, spec, cfg, name)

    # Assert file created
    out_file = tmp_path / f"{name}.png"
    assert out_file.exists(), "multiselect_profile did not create output file"
