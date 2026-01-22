# Architecture Overview

stataX is designed as a **deterministic analysis pipeline** with clear stage boundaries.

---

## Pipeline Order

1. Load CSV (explicit encoding)
2. Validate schema
3. Apply transforms
4. Resolve aliases
5. Descriptive statistics
6. Model fitting (optional)
7. Diagnostics
8. Artifact rendering
9. Export + metadata

---

## Execution Modes

### Statistical Mode
- `analysis.model: ols | logit`
- Produces regression tables + plots

### Visualization-Only Mode
- `analysis.model: none`
- No regression required
- Survey plots only

---

## Artifact System

Artifacts are:
- Declarative
- Independent
- Rendered post-analysis
- Deterministic

Each artifact:
- Receives raw `df`
- Receives resolved column names
- Never mutates data

---

## Design Principles

- No hidden state
- No silent failure
- No inference without declaration
- CLI-first
- API-second (to be implemented at v2.0)