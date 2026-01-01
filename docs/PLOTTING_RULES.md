# Plotting Rules

statax enforces strict data compatibility.

- Histogram / Box / Scatter require numeric data
- Bar plots accept categorical data
- No silent coercion is performed

If a column contains mixed types, plotting will fail
with a clear error message.
