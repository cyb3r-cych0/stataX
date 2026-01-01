# stataX v1.1.0 — Artifacts & Plotting Release

v1.1.0 introduces a universal artifact system and plotting support, completing the core vision of statax as a reproducible, Stata-like statistical CLI.

This release adds visual outputs without compromising determinism, transparency, or domain neutrality.

# What’s New
## Artifact System

- Introduced a first-class artifact abstraction

- Tables, plots, and metadata are handled uniformly

- Clear separation between:

  - statistical computation

  - output representation

  - file export

- Artifact-first design enables future extensions without core changes

# Plotting Support (Universal)

Added Stata-style statistical plots, configurable via YAML:

Supported plot kinds:

- `histogram` (numeric)

- `bar` (categorical)

- `box` (numeric by group)

- `scatter` (numeric x/y)

- `residuals_vs_fitted` (regression diagnostics)

Key properties:

- CLI-only (no GUI)

- Matplotlib backend

- Deterministic outputs

- Alias-aware

- Fully optional

# Plot Configuration

Plots are controlled via config:
```yaml
artifacts:
  plots:
    - kind: histogram
      column: concern

plots:
  out_dir: plots/
  formats: [png]
  dpi: 150
```

Defaults apply if omitted.

# Strict Data Semantics

- No silent coercion for plotting

- Numeric-only enforcement where required

- Clear, actionable error messages

- Behavior aligned with Stata/SPSS expectations

# Testing & Stability

- New integration tests for plot artifacts

- All existing tests remain passing

- Backward-compatible with v1.0.x configs

# Explicit Non-Goals

- No interactive plotting

- No domain-specific visuals

- No automatic type inference

- No GUI

These remain intentional design choices.

# Upgrade Notes

- Existing configs continue to work unchanged

- Plotting is opt-in via artifacts.plots

- No breaking API changes

# Documentation

New and updated documentation:

- Artifact & plotting overview in README.md

- Plotting rules (docs/PLOTTING_RULES.md)

- Authoritative config reference (docs/CONFIG.md)

- Ready-to-run examples in examples/

# Versioning

- v1.1.0 — Artifact system + plotting

- Core statistical API remains frozen

- Future work will focus on extensions, not core changes

# License

MIT License