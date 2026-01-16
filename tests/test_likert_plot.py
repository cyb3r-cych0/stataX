def test_likert_plot(tmp_path):
    import pandas as pd
    from statax.output.plot_renderers import likert

    df = pd.DataFrame({
        "Q": [
            "Low", "Medium", "High",
            "High", "Medium", "High"
        ]
    })

    spec = {
        "column": "Q",
        "scale": ["Low", "Medium", "High"],
        "normalize": True
    }

    cfg = {
        "out_dir": tmp_path,
        "formats": ["png"],
        "dpi": 100
    }

    likert(df, spec, cfg, "likert_test")

    assert (tmp_path / "likert_test.png").exists()
