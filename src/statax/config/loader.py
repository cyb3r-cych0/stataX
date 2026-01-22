import json
import yaml
from pathlib import Path
from .schema import (
    Config, DataConfig, VariablesConfig, AnalysisConfig, OutputConfig,
    Transform, DescriptivesConfig, MissingConfig, AliasConfig,
    ExportConfig, PlotSpec, ArtifactConfig, PlotOutputConfig,
    TimeSeriesConfig, ClusterConfig
)

class ConfigError(Exception):
    pass

def load_config(path: str) -> Config:
    p = Path(path)
    if not p.exists():
        raise ConfigError(f"Config file not found: {path}")

    if p.suffix.lower() in [".yaml", ".yml"]:
        raw = yaml.safe_load(p.read_text(encoding="utf-8"))
    elif p.suffix.lower() == ".json":
        raw = json.loads(p.read_text(encoding="utf-8"))
    else:
        raise ConfigError("Config must be YAML or JSON")

    try:
        return _parse(raw)
    except KeyError as e:
        raise ConfigError(f"Missing required key: {e}")
    except TypeError as e:
        raise ConfigError(f"Invalid config structure: {e}")

def _parse(raw: dict) -> Config:
    data_raw = raw["data"]

    if "encoding" in data_raw and not isinstance(data_raw["encoding"], str):
        raise ConfigError("data.encoding must be a string")

    data = DataConfig(**raw["data"])

    vars_raw = raw["variables"]
    variables = VariablesConfig(
        outcome=vars_raw["outcome"],
        predictors=vars_raw["predictors"],
        interactions=[(str(p[0]), str(p[1])) for p in vars_raw.get("interactions", [])],
        fixed_effects=[str(x) for x in vars_raw.get("fixed_effects", [])],
    )

    for p in vars_raw.get("interactions", []):
        if not isinstance(p, (list, tuple)) or len(p) != 2:
            raise ConfigError("Each interaction must be a pair of variable names")

    aliases = None
    if "aliases" in raw:
        aliases = AliasConfig(map=raw["aliases"])

    analysis_raw = raw["analysis"]
    missing_cfg = MissingConfig()
    if "missing" in analysis_raw:
        missing_cfg = MissingConfig(**analysis_raw["missing"])

    cluster = None
    if "cluster" in analysis_raw:
        cluster = ClusterConfig(
            by=analysis_raw["cluster"]["by"]
        )

    analysis = AnalysisConfig(
        model=analysis_raw["model"],
        robust_se=analysis_raw.get("robust_se", False),
        missing=missing_cfg,
        cluster=cluster,
    )

    output_raw = raw.get("output", {})
    export_cfg = ExportConfig()
    if "export" in output_raw:
        export_cfg = ExportConfig(**output_raw["export"])

    # print(OutputConfig.__annotations__) --verbose logging

    output = OutputConfig(
        table=output_raw.get("table", True),
        export=export_cfg,
    )

    transforms = [
        Transform(**t) for t in raw.get("transforms", [])
    ]

    descriptives = None
    if "descriptives" in raw:
        descriptives = DescriptivesConfig(**raw["descriptives"])

    artifacts = None
    if "artifacts" in raw:
        plot_specs = []
        for p in raw["artifacts"].get("plots", []):
            if "kind" not in p:
                raise ConfigError("Plot artifact missing 'kind'")
            plot_specs.append(
                PlotSpec(kind=p["kind"], spec=p)
            )
        artifacts = ArtifactConfig(plots=plot_specs)

    plots_cfg = PlotOutputConfig()
    if "plots" in raw:
        plots_cfg = PlotOutputConfig(**raw["plots"])

    timeseries = None
    if "timeseries" in raw:
        timeseries = TimeSeriesConfig(**raw["timeseries"])

    return Config(
        data=data,
        variables=variables,
        analysis=analysis,
        output=output,
        transforms=transforms,
        descriptives=descriptives,
        aliases=aliases,
        artifacts=artifacts,
        plots=plots_cfg,
        timeseries=timeseries
    )

