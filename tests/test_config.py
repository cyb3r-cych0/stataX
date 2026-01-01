from statax.config.loader import load_config

def test_yaml_load(tmp_path):
    cfg = tmp_path / "a.yaml"
    cfg.write_text("""
data:
  path: test.csv
variables:
  outcome: y
  predictors: [x]
analysis:
  model: ols
output:
  table: true
""")
    c = load_config(str(cfg))
    assert c.variables.outcome == "y"
