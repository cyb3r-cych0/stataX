
# Reproducibility

stataX guarantees reproducibility under the following conditions:

- Same input CSV
- Same config file
- Same stataX version

Each run produces `run_metadata.json` containing:
- Timestamp
- Python version
- OS/platform
- Full config used

This file can be included in:
- replication packages
- journal submissions
- audit trails
