def test_categorical_profile_creates_file(tmp_path):
    from statax.output.plot_renderers import categorical_profile

    spec = {
        "groups": [
            {"name": "3. Gender ", "values": {"Men": 40, "Women": 60}},
            {"name": "2. Age Range ", "values": {"Young": 30, "Old": 70}},
        ]
    }

    cfg = {
        "out_dir": tmp_path,
        "formats": ["png"],
        "dpi": 100,
    }

    categorical_profile(spec, cfg, "profile_test")

    files = list(tmp_path.iterdir())
    assert any(f.name.startswith("profile_test") for f in files)
