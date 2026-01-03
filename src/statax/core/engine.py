from statax.config.schema import Config
from statax.core.data import load_csv, validate_columns
from statax.core.transform import apply_transforms
from statax.core.descriptives import (
    summary_table, grouped_summary, frequency_table
)
from statax.output.tables import print_tables, print_table
from statax.core.stats import ols_with_data, logit_with_data
from statax.output.regression import regression_table
from statax.core.diagnostics import regression_diagnostics
from statax.core.alias import resolve, resolve_list, validate_aliases
from statax.output.export import export_regression, export_metadata
from statax.core.metadata import build_metadata
from statax.core.data import parse_dates, DataError
from statax.artifacts.registry import ArtifactRegistry
from statax.artifacts.table import TableArtifact
from statax.artifacts.plot import PlotArtifact


def run(config: Config):
    df = load_csv(
        config.data.path,
        config.data.delimiter,
        config.data.missing_values
    )

    registry = ArtifactRegistry()

    alias_map = config.aliases.map if config.aliases else None
    if alias_map:
        validate_aliases(
            df.columns,
            alias_map
        )

    outcome = resolve(
        config.variables.outcome,
        alias_map
    )

    cluster_col = None
    if config.analysis.cluster:
        col = resolve(config.analysis.cluster.by, alias_map)
        if col not in df.columns:
            raise DataError(f"Cluster column not found: {col}")

        n_groups = df[col].nunique(dropna=True)
        if n_groups < 2:
            raise DataError("Clustered SE requires at least 2 groups.")

        cluster_col = col

    predictors = resolve_list(
        config.variables.predictors,
        alias_map
    )

    validate_columns(
        df,
        outcome,
        predictors
    )

    interactions = [
        (
            resolve(a, alias_map),
            resolve(b, alias_map),
        )
        for a, b in config.variables.interactions
    ]

    fixed_effects = [
        resolve(x, alias_map)
        for x in config.variables.fixed_effects
    ]

    if config.timeseries:
        date_col = config.timeseries.date_column

        if config.aliases and date_col in config.aliases.map:
            date_col = config.aliases.map[date_col]

        df = parse_dates(
            df,
            date_col
        )
        df = df.sort_values(date_col)

    if config.transforms:
        df = apply_transforms(
            df,
            config.transforms
        )

    if config.descriptives:
        if config.descriptives.summary:
            tables = summary_table(df)
            print_tables(tables)

        if config.descriptives.group_by:
            print_table(
                f"Grouped by {config.descriptives.group_by}",
                grouped_summary(
                    df,
                    config.descriptives.group_by
                )
            )
        for col in config.descriptives.frequencies:
            print_table(
                f"Frequency: {col}",
                frequency_table(
                    df,
                    col
                )
            )

    if config.analysis.model == "ols":
        model, X_used, y_used = ols_with_data(
            df,
            outcome,
            predictors,
            interactions,
            fixed_effects,
            robust=config.analysis.robust_se,
            cluster=cluster_col,
            missing_strategy=config.analysis.missing.strategy
        )

    elif config.analysis.model == "logit":
        model, X_used, y_used = logit_with_data(
            df,
            outcome,
            predictors,
            interactions,
            fixed_effects,
            robust=config.analysis.robust_se,
            cluster=cluster_col,
            missing_strategy=config.analysis.missing.strategy
        )

    else:
        raise ValueError("Unsupported model")

    notes = regression_diagnostics(X_used, y_used)
    if not notes:
        print("✓ No regression diagnostics triggered")
    else:
        print("⚠ Regression diagnostics:")
        for n in notes:
            print(f" - {n}")

    reg_df = regression_table(
        model,
        alias_map
    )

    registry.add(
        TableArtifact(
            "regression",
            reg_df
        )
    )
    print_table(
        "Regression Results",
        reg_df
    )

    if config.artifacts and config.artifacts.plots:
        for i, p in enumerate(config.artifacts.plots):
            registry.add(
                PlotArtifact(
                    artifact_id=f"plot_{i}_{p.kind}",
                    kind=p.kind,
                    spec=p.spec,
                )
            )

    if config.artifacts:
        plot_cfg = {
            "out_dir": config.plots.out_dir,
            "formats": config.plots.formats,
            "dpi": config.plots.dpi,
        }

        for a in registry.all():
            if a.kind == "plot":
                print("RENDERING:", a.id)
                a.render(
                    df=df,
                    model=model,
                    cfg=plot_cfg,
                    resolve=lambda x: resolve(x, alias_map),
                )

    print("Export formats:", config.output.export.format)

    exp = config.output.export
    if exp.format:
        export_regression(
            reg_df,
            exp
        )
        meta = build_metadata(config)
        export_metadata(
            meta,
            exp
        )

    print("Missing strategy:", config.analysis.missing.strategy)
