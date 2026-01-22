# stataX

**stataX** is a CLI-first, reproducible statistical analysis and visualization engine in Python, inspired by Stata/SPSS workflows but designed for modern, config-driven research pipelines.

It emphasizes **explicit decisions, honest failures, and publication-ready outputs**.

---

## Current Status

**v1.3.0 — Stable**  
✔ Statistical core  
✔ Visualization system  
✔ Survey / questionnaire workflows supported  
✔ Encoding-safe (Windows / Excel compatible)  

---

## Key Features

### Core
- YAML-based analysis configs
- Deterministic, reproducible pipeline
- Explicit missing-data strategies
- Robust error handling (no silent coercion)
- Alias system for messy survey headers
- Run metadata export

### Models
- OLS (robust + clustered SE)
- Logit (binary outcomes)
- None (plots only)
- Full diagnostics & inference tables

### Visualization (Artifacts)
- Histogram, bar, box, scatter, line
- **Categorical profile**
- **Multiselect profile (survey questions)**
- **Likert (stacked)**
- **Diverging Likert (centered)**
- Heatmaps
- Pie / donut charts
- Coefficient plots (CI-aware)

All figures are **PNG export-ready** for reports and papers.

---

## Installation

`python >= 3.14` recommended

**Clone the repository** `git clone https://github.com/cyb3r-cych0/stataX.git`

```bash
cd path/to/stataX/
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
  path: datasets/example.csv
  encoding: latin1   # Excel-safe

aliases:
  gender: "Gender"
  concern: "How concerned are you about the environmental and health impacts of microplastics?"

analysis:
  model: none    # visualization-only mode

artifacts:
  plots:
    - kind: categorical_profile
      from_data:
        column: gender
        normalize: percent

    - kind: multiselect_profile
      column: "In what environmental settings do you most often encounter plastic waste? (Select all that apply) "
      normalize: percent

    - kind: diverging_likert
      column: concern
      scale:
        - Not concerned
        - Slightly concerned
        - I don’t know enough to answer
        - Moderately concerned
        - Extremely concerned
      neutral: "I don’t know enough to answer"
      normalize: true

plots:
  out_dir: plots/
  formats: [png]
  dpi: 300
```

### Outputs

- `plots/*.png`
- `regression.csv`/`.tex` (if model enabled)
- `run_metadata.json`

---

## Philosophy

**stataX favors:**

- Explicit assumptions
- Readable failures
- Reproducibility over automation
- Survey-aware visual analytics

---

## Known Constraints

- No automatic encoding detection (must be explicit)
- No survey weights (yet)
- No GUI
- No ML models
- No silent category collapsing

---

## CI & Stability

- Pytest-based regression suite
- Windows-safe paths & encodings
- Deterministic plot rendering

---

## Versioning Note

### `stataX v1.3.0`

**Check the `docs` folder to read more**

---

## Roadmap

- v1.4.x — PDF / LaTeX figure export
- v1.5.x — Weighted survey analysis
- v1.6.x — Faceted Likert by group
- v1.7.x — Report Templates
- v2.0 — long-term API stabilization

---

## License

See LICENSE.

---