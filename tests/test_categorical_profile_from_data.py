def test_categorical_profile_from_data(tmp_path):
    import pandas as pd
    from statax.output.plot_renderers import categorical_profile

    df = pd.DataFrame({
        "gender": ["M", "F", "M", "M", "F"]
    })

    spec = {
        "from_data": {
            "column": "gender",
            "normalize": "percent",
        }
    }

    cfg = {"out_dir": tmp_path, "formats": ["png"], "dpi": 100}

    categorical_profile(
        spec,
        cfg,
        "profile_data",
        df=df,
        resolve=lambda x: x
    )

    assert any(p.name.startswith("profile_data") for p in tmp_path.iterdir())
