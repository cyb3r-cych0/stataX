# Changelog

All notable changes to this project are documented here.

This project follows semantic versioning.

---

## v1.3.0 — Visualization & Survey Analytics Freeze (2026-01)

### Added
- Survey-first visualization artifacts:
  - `categorical_profile`
  - `multiselect_profile`
  - `likert`
  - `diverging_likert`
  - `coef_plot`
- Visualization-only execution mode (`analysis.model: none`)
- Encoding-aware CSV loading (Windows / Excel compatible)
- Explicit artifact styling via YAML (`style:` blocks)
- Publication-ready PNG outputs (300 DPI)
- Figure metadata embedding support (captions + spec tracking)

### Improved
- Alias resolution across plots and statistics
- Robust fixed-effects handling
- Clear failure modes for invalid survey scales
- Deterministic plot rendering (no silent reordering)

### Fixed
- Clustered SE validation (minimum group checks)
- Numeric coercion edge cases
- Likert scale mismatches
- UTF-8 / cp1252 decoding issues
- Artifact rendering order stability

### Removed
- Implicit statistical assumptions
- Silent missing-data coercion
- Auto-detection of Likert scales (must be explicit)

### Status
✔ Stable  
✔ Feature complete for survey + exploratory analysis  
✔ Frozen for v1.x  

---

## v1.2.0
- Statistical core hardening
- OLS + Logit stabilized
- Regression diagnostics added
- CSV / LaTeX export

---

## v1.1.0
- Alias system introduced
- Missing-data strategies formalized

---

## v1.0.0
- Initial release
- CLI-driven statistical engine
- Deterministic pipeline
