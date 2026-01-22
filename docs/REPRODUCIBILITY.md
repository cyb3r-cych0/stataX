# Reproducibility 

stataX guarantees reproducibility when:

- Input CSV is unchanged
- YAML config is unchanged
- stataX version is unchanged

---

## What Is Recorded

Each run emits `run_metadata.json` containing:

- Timestamp
- Python version
- OS / platform
- Full resolved config
- Artifact list
- Version hash

---

## Intended Use

- Academic replication packages
- Journal submissions
- Audit trails
- Internal analytics reviews

---

## What Is Not Guaranteed

- Floating-point equality across platforms
- Identical font rendering across OS
- Automatic encoding normalization

These are explicitly out of scope.
