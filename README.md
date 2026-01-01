# stataX

A CLI-first, reproducible statistical analysis engine in Python, inspired by Stata/SPSS workflows.

## Key Features
- YAML/JSON config files (do-file equivalent)
- Deterministic data pipeline
- Explicit transformations and missing-data strategies
- Human-readable tables (CLI)
- OLS and Logit regression with diagnostics
- Alias support for long survey variables
- CSV & LaTeX exports
- Full run metadata for reproducibility
- Windows- and CI-safe

## Installation
```bash
pip install -e .
```

## Basic Usage
```bash
statax run analysis.yaml
```

## Example Config
```yaml
data:
  path: survey.csv

aliases:
  gender: "3. Gender "

variables:
  outcome: concern
  predictors: [gender]

analysis:
  model: ols
  missing:
    strategy: drop_predictors_only

output:
  table: true
  export:
    format: [csv, latex]
    out_dir: outputs/
```
**Outputs**
- `regression.csv`
- `regression.tex`
- `run_metadata.json`

## Philosophy
**stataX favors explicit statistical decisions, honest failures, and reproducibility over automation.**

## Reproducibility

### `docs/REPRODUCIBILITY.md`
```yaml
# Reproducibility

stataX guarantees reproducibility under the following conditions:

- Same input CSV
- Same config file
- Same statax version

Each run produces `run_metadata.json` containing:
- Timestamp
- Python version
- OS/platform
- Full config used

This file can be included in:
- replication packages
- journal submissions
- audit trails
```

## Architecture Overview

### `docs/ARCHITECTURE.md`
```md
# Architecture

Pipeline order:
1. Load CSV
2. Validate schema
3. Apply transforms
4. Descriptives
5. Missing-data handling
6. Regression
7. Diagnostics
8. Export + metadata

Design principles:
- No silent coercion
- No implicit encoding
- CLI-first
- Engine reusable by API
```

## CLI Reference

### `docs/CLI.md`
```md
# CLI Reference

## Run analysis
```bash
statax run analysis.yaml
```
**Exit Behaviour**
- Non-zero exit on config or data errors
- Clear diagnostics for statistical failures
- 
## Config Reference

### `docs/CONFIG.md`
```yaml
# Config Reference

## analysis.missing.strategy
- complete_case (default)
- drop_predictors_only
- mean_impute_predictors

## aliases
Maps short names → raw CSV headers

## output.export.format
- csv
- latex
```

## CI Hardening

### `.github/workflows/ci.yml`
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -e .
      - run: pip install pytest
      - run: pytest

```

## Release Notes

### `CHANGELOG.md`
```md
# Changelog

## v1.0.0
- Stable statistical core
- Explicit missing-data strategies
- Alias support
- CSV and LaTeX export
- Reproducible run metadata
```

## License

`LCENSE`

**What v1.0 explicitly does NOT do** 
```md
- No automatic encoding
- No survey weights
- No ML models
- No GUI
```


