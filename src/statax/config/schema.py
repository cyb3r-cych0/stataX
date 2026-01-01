from typing import List, Dict, Optional, Literal
from dataclasses import dataclass, field

@dataclass(frozen=True)
class PlotOutputConfig:
    out_dir: str = "plots"
    formats: List[str] = field(default_factory=lambda: ["png"])
    dpi: int = 150

@dataclass(frozen=True)
class PlotSpec:
    kind: str
    spec: Dict

@dataclass(frozen=True)
class ArtifactConfig:
    plots: List[PlotSpec] = field(default_factory=list)

@dataclass(frozen=True)
class ExportConfig:
    format: List[str] = field(default_factory=list)  # csv, latex
    out_dir: str = "outputs"
    overwrite: bool = False

@dataclass(frozen=True)
class OutputConfig:
    table: bool = True
    export: ExportConfig = ExportConfig()

@dataclass(frozen=True)
class AliasConfig:
    map: Dict[str, str] = field(default_factory=dict)

@dataclass(frozen=True)
class MissingConfig:
    strategy: Literal[
        "complete_case",
        "drop_predictors_only",
        "mean_impute_predictors"
    ] = "complete_case"

@dataclass(frozen=True)
class DescriptivesConfig:
    summary: bool = False
    group_by: Optional[str] = None
    frequencies: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class DataConfig:
    path: str
    delimiter: str = ","
    missing_values: List[str] = field(default_factory=lambda: ["", "NA"])

@dataclass(frozen=True)
class VariablesConfig:
    outcome: str
    predictors: List[str]

@dataclass(frozen=True)
class Transform:
    type: Literal["recode"]
    column: str
    mapping: Dict[str, str] = field(default_factory=dict)

@dataclass(frozen=True)
class AnalysisConfig:
    model: Literal["ols", "logit"]
    robust_se: bool = True
    missing: Optional[MissingConfig] = MissingConfig()

@dataclass(frozen=True)
class Config:
    data: DataConfig
    variables: VariablesConfig
    analysis: AnalysisConfig
    output: OutputConfig
    transforms: List[Transform] = field(default_factory=list)
    descriptives: Optional[DescriptivesConfig] = None
    aliases: Optional[AliasConfig] = None
    artifacts: Optional[ArtifactConfig] = None
    plots: PlotOutputConfig = PlotOutputConfig()
