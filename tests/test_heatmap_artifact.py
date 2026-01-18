def test_heatmap_created(tmp_path):
    import pandas as pd
    from statax.output.plot_renderers import heatmap

    df = pd.DataFrame({
        "A": ["x", "x", "y", "y"],
        "B": ["u", "v", "u", "v"]
    })

    cfg = {
        "out_dir": tmp_path,
        "formats": ["png"],
        "dpi": 100
    }

    spec = {"x": "A", "y": "B", "normalize": "row"}

    heatmap(df, spec, cfg, "heatmap_test")

    assert (tmp_path / "heatmap_test.png").exists()
