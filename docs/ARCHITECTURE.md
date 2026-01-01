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

