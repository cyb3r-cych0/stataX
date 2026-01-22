def test_data_encoding_config():
    from statax.config.schema import DataConfig
    cfg = DataConfig(path="x.csv", encoding="cp1252")
    assert cfg.encoding == "cp1252"
