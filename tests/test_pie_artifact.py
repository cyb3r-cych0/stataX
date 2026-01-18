def test_pie_created(tmp_path):
    import pandas as pd
    from statax.output.plot_renderers import pie

    df = pd.DataFrame({
        "Gender": ["M", "F", "M", "F", "M"]
    })

    cfg = {
        "out_dir": tmp_path,
        "formats": ["png"],
        "dpi": 100
    }

    spec = {"column": "Gender", "donut": True}

    pie(df, spec, cfg, "pie_test")

    assert (tmp_path / "pie_test.png").exists()
