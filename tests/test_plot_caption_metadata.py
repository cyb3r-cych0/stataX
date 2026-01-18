def test_plot_caption_metadata(tmp_path):
    from statax.output.export import export_plot_metadata

    spec = {
        "kind": "likert",
        "column": "x",
        "caption": "Test caption",
    }

    export_plot_metadata(tmp_path, "fig1", spec)

    meta = (tmp_path / "fig1.meta.json").read_text()
    assert "Test caption" in meta
