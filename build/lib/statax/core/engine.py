from statax.config.schema import Config
from statax.core.data import load_csv, validate_columns
from statax.core.transform import apply_transforms
from statax.core.descriptives import (
    summary_table, grouped_summary, frequency_table
)
from statax.output.tables import print_tables, print_table
from statax.core.stats import ols, logit
from statax.output.regression import regression_table
from statax.core.diagnostics import regression_diagnostics
from statax.core.alias import resolve, resolve_list, validate_aliases
from statax.output.export import export_regression, export_metadata
from statax.core.metadata import build_metadata





def run(config: Config):
    df = load_csv(
        config.data.path,
        config.data.delimiter,
        config.data.missing_values
    )

    alias_map = config.aliases.map if config.aliases else None

    if alias_map:
        validate_aliases(df.columns, alias_map)

    outcome = resolve(config.variables.outcome, alias_map)
    predictors = resolve_list(config.variables.predictors, alias_map)

    validate_columns(df, outcome, predictors)

    if config.transforms:
        df = apply_transforms(df, config.transforms)

    if config.descriptives:
        if config.descriptives.summary:
            tables = summary_table(df)
            print_tables(tables)

        if config.descriptives.group_by:
            print_table(
                f"Grouped by {config.descriptives.group_by}",
                grouped_summary(df, config.descriptives.group_by)
            )

        for col in config.descriptives.frequencies:
            print_table(
                f"Frequency: {col}",
                frequency_table(df, col)
            )

    if config.analysis.model == "ols":
        model, X_used, y_used = ols(
            df,
            outcome,
            predictors,
            config.analysis.robust_se,
            config.analysis.missing.strategy
        )

    elif config.analysis.model == "logit":
        model, X_used, y_used = logit(
            df,
            outcome,
            predictors,
            config.analysis.robust_se,
            config.analysis.missing.strategy
        )
    else:
        raise ValueError("Unsupported model")

    print("\n>>> RUNNING REGRESSION DIAGNOSTICS <<<")
    notes = regression_diagnostics(X_used, y_used)

    if not notes:
        print("✓ No regression diagnostics triggered")
    else:
        print("⚠ Regression diagnostics:")
        for n in notes:
            print(f" - {n}")

    reg_df = regression_table(model, alias_map)
    print_table("Regression Results", reg_df)

    print("Export formats:", config.output.export.format)

    exp = config.output.export
    if exp.format:
        export_regression(reg_df, exp)

        meta = build_metadata(config)
        export_metadata(meta, exp)

    print("Missing strategy:", config.analysis.missing.strategy)

