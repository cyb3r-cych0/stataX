## stataX v1.0.0 — Stable Core Release

statax v1.0.0 marks the first stable, frozen release of a CLI-first statistical analysis engine inspired by Stata/SPSS workflows, built for reproducible research and survey analysis.

This release focuses on statistical correctness, transparency, and reproducibility rather than automation or black-box behavior.

## Highlights
**Core Capabilities**

    YAML / JSON config files (do-file equivalent)
    
    Deterministic, step-by-step analysis pipeline
    
    Explicit variable transformations and recoding
    
    Human-readable descriptive statistics (CLI)
    
    OLS and Logit regression
    
    Robust standard errors (HC3)
    
    Clear regression diagnostics (rank deficiency, zero variance)
    
    Alias support for long survey variable names
    
    CSV and LaTeX export of results
    
    Full run metadata for reproducibility
    
    Windows- and CI-safe execution

## Designed For

    Survey and questionnaire analysis
    
    Academic and policy research
    
    Reproducible statistical workflows
    
    Google Forms and similar CSV-based datasets

## Design Philosophy

**stataX prioritizes:**

    Explicit statistical decisions over automation
    
    Honest failure modes instead of silent coercion
    
    Auditability and reproducibility by default
    
    If a model cannot be estimated, statax explains why.

## Outputs

**Each run can produce:**

    regression.csv
    
    regression.tex
    
    run_metadata.json (environment + config snapshot)

**These artifacts are suitable for:**

    replication packages
    
    journal submissions
    
    version-controlled analysis

## Explicit Non-Goals (v1.0.x)

    No automatic categorical encoding
    
    No survey weights
    
    No imputation of outcomes
    
    No GUI

    No machine learning models

 - These omissions are intentional to preserve statistical clarity.

## Stability

    Core API frozen for v1.x
    
    Backward-compatible config guaranteed within major version
    
    Bug fixes only in v1.0.x

## Versioning

    v1.0.0 — Stable core release
    
    Future features will be introduced incrementally and conservatively

## Documentation

**See:**

    README.md — overview and quick start
    
    docs/REPRODUCIBILITY.md — guarantees and metadata
    
    docs/CONFIG.md — authoritative config reference
    
    docs/ARCHITECTURE.md — system design

## License

MIT License