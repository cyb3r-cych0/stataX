def test_categorical_profile_style(tmp_path):
    from statax.output.plot_renderers import categorical_profile

    spec = {
        "y_label": "%",
        "style": {"theme": "grayscale", "show_values": True, "font_scale": 1.1},
        "groups": [
            {"name": "3. Gender", "values": {"Men": 40, "Women": 60}},
        ],
    }

    cfg = {"out_dir": tmp_path, "formats": ["png"], "dpi": 120}
    categorical_profile(spec, cfg, "profile_style")

    assert any(p.name.startswith("profile_style") for p in tmp_path.iterdir())
