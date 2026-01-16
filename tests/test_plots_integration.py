def test_plot_files_created(tmp_path):
    from statax.core.engine import run
    from statax.config.loader import load_config

    csv = tmp_path / "d.csv"
    csv.write_text("y,x\n1,1\n2,2\n3,3\n")

    yaml = tmp_path / "a.yaml"
    plots_dir = tmp_path / "plots"

    yaml.write_text(
            f"""
        data:
          path: "{csv.as_posix()}"
        variables:
          outcome: y
          predictors: [x]
        analysis:
          model: ols
        artifacts:
          plots:
            - kind: histogram
              column: y
        plots:
          out_dir: "{plots_dir.as_posix()}"
        """
    )

    config = load_config(yaml)
    run(config)

    assert (tmp_path / "plots").exists()
