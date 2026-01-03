from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

def _numeric_series(df, column, plot_kind):
    s = pd.to_numeric(df[column], errors="coerce")
    if s.dropna().empty:
        raise ValueError(
            f"{plot_kind} requires numeric data, but column '{column}' "
            f"has no numeric values after coercion."
        )
    return s

def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

def save(fig, out_dir, name, formats, dpi):
    ensure_dir(out_dir)
    for f in formats:
        fig.savefig(Path(out_dir) / f"{name}.{f}", dpi=dpi, bbox_inches="tight")
    plt.close(fig)

def histogram(df, column, cfg, name):
    fig, ax = plt.subplots()
    s = _numeric_series(df, column, "Histogram")
    s.hist(ax=ax)
    ax.set_title(f"Histogram: {column}")
    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def bar(df, column, cfg, name):
    fig, ax = plt.subplots()
    df[column].value_counts(dropna=False).plot.bar(ax=ax)
    ax.set_title(f"Bar: {column}")
    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def box(df, y, by, cfg, name):
    fig, ax = plt.subplots()
    s = _numeric_series(df, y, "Boxplot")
    tmp = df.copy()
    tmp[y] = s
    tmp.boxplot(column=y, by=by, ax=ax)
    ax.set_title(f"Box: {y} by {by}")
    plt.suptitle("")
    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def scatter(df, x, y, cfg, name):
    fig, ax = plt.subplots()
    xs = _numeric_series(df, x, "Scatter")
    ys = _numeric_series(df, y, "Scatter")
    ax.scatter(xs, ys)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f"Scatter: {x} vs {y}")
    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def residuals_vs_fitted(model, cfg, name):
    fig, ax = plt.subplots()
    ax.scatter(model.fittedvalues, model.resid)
    ax.axhline(0, linestyle="--")
    ax.set_xlabel("Fitted values")
    ax.set_ylabel("Residuals")
    ax.set_title("Residuals vs Fitted")
    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def line(df, x, y, cfg, name):
    fig, ax = plt.subplots()
    # x is date, y must be numeric
    xs = df[x]
    ys = pd.to_numeric(df[y], errors="coerce")

    if ys.dropna().empty:
        raise ValueError(
            f"Line plot requires numeric data for '{y}', but no numeric values found."
        )
    ax.plot(xs, ys)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f"{y} over time")
    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def rolling_mean(df, x, y, window, cfg, name):
    fig, ax = plt.subplots()
    xs = df[x]
    ys = pd.to_numeric(df[y], errors="coerce")

    if ys.dropna().empty:
        raise ValueError(
            f"Rolling mean requires numeric data for '{y}', but no numeric values found."
        )
    ax.plot(xs, ys.rolling(window).mean())
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f"{y} ({window}-period rolling mean)")
    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])