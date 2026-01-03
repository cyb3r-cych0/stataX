# stataX

**stataX** is a CLI-first, reproducible statistical analysis engine in Python, inspired by Stata/SPSS-style workflows but designed for modern, configuration-driven research.

It prioritizes **explicit statistical decisions, honest failures, and reproducibility** over automation or black-box convenience.

---

## Why stataX?

Most Python statistical workflows are:
- notebook-heavy
- implicit about data handling
- difficult to reproduce exactly

stataX is different.

**stataX is a “do-file engine” for Python.**

You describe *what* you want in a YAML/JSON file, and stataX executes it deterministically.

---

## Core Features

-  **YAML / JSON configs** (Stata do-file equivalent)
-  **Deterministic execution pipeline**
-  **Explicit missing-data strategies**
-  **Alias system** for long / survey-style column names
-  **OLS & Logit regression**
    - interactions
    - fixed effects
    - robust & clustered standard errors
-  **Regression diagnostics**
-  **Artifact-based plotting** (histograms, residuals, rolling means, etc.)
-  **CSV & LaTeX exports**
-  **Full run metadata for reproducibility**
-  **CLI-first, CI-safe, Windows-safe**

---

## Installation

**python >= 3.14** recommended
```bash
pip install -e .
```

---

## Usage
```bash
statax run analysis.yaml
```
**stataX will:**
1. Load data
2. Validate schema
3. Apply transforms
4. Run descriptives
5. Handle missing data
6. Fit model
7. Run diagnostics
8. Export results + metadata

---

### Minimal Example
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

### Outputs

- `regression.csv`
- `regression.tex`
- `run_metadata.json` 

---

## Reproducibility Guarantees

stataX guarantees bit-for-bit reproducibility given:

 - same input CSV
 - same config file
 - same stataX version

Each run produces run_metadata.json containing:
- timestamp
- OS & Python version
- stataX version
- full resolved configuration

This file is suitable for:
- replication packages
- audit trails

---

## Architecture Overview

Pipeline order:
1. Load CSV
2. Validate columns & aliases
3. Apply transforms
4. Descriptive statistics
5. Missing-data handling
6. Model fitting
7. Diagnostics
8. Artifact rendering
9. Export & metadata

The engine is reusable programmatically, but the CLI is the primary interface.

---

## What stataX Does NOT Do (by design)

- No automatic categorical encoding
- No survey weights
- No ML models
- No GUI
- No notebook dependency

stataX is not a replacement for pandas or statsmodels —
it is an execution layer above them.

---

## Project Status
- v1.2.0 — Stable core
- Statistical core hardened
- Extensive failure-mode tests
- Safe for applied research & analysis

---

## License

See LICENSE.

---

## Roadmap

- v1.3.x — extended plotting & summaries
- v1.4.x — panel / time-series models
- v2.0 — long-term API stabilization