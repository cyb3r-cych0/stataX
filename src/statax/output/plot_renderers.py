import matplotlib
matplotlib.use("Agg")
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statax.output.plot_theme import PALETTES

def apply_caption(fig, caption):
    if not caption:
        return

    fig.text(
        0.5,
        -0.15,
        caption,
        ha="center",
        va="top",
        wrap=True,
        fontsize=10,
    )

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
    ax.set_title(f"Histogram: {column}", pad=12)
    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def bar(df, column, cfg, name):
    fig, ax = plt.subplots()
    df[column].value_counts(dropna=False).plot.bar(ax=ax)
    ax.set_title(f"Bar: {column}", pad=12)
    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def box(df, y, by, cfg, name):
    fig, ax = plt.subplots()
    s = _numeric_series(df, y, "Boxplot")
    tmp = df.copy()
    tmp[y] = s
    tmp.boxplot(column=y, by=by, ax=ax)
    ax.set_title(f"Box: {y} by {by}", pad=12)
    plt.suptitle("")
    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def scatter(df, x, y, cfg, name):
    fig, ax = plt.subplots()
    xs = _numeric_series(df, x, "Scatter")
    ys = _numeric_series(df, y, "Scatter")
    ax.scatter(xs, ys)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f"Scatter: {x} vs {y}", pad=12)
    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def residuals_vs_fitted(model, cfg, name):
    fig, ax = plt.subplots()
    ax.scatter(model.fittedvalues, model.resid)
    ax.axhline(0, linestyle="--")
    ax.set_xlabel("Fitted values")
    ax.set_ylabel("Residuals")
    ax.set_title("Residuals vs Fitted", pad=12)
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
    ax.set_title(f"{y} over time", pad=12)
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
    ax.set_title(f"{y} ({window}-period rolling mean)", pad=12)
    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def categorical_profile(spec, cfg, name, df=None, resolve=None):
    """Data driven mode"""
    if "from_data" in spec:
        if df is None or resolve is None:
            raise ValueError("from_data requires dataframe and resolver")

        fd = spec["from_data"]
        col = resolve(fd["column"])
        normalize = fd.get("normalize", "percent")
        dropna = fd.get("dropna", True)

        if col not in df.columns:
            raise ValueError(f"Column not found for categorical_profile: {col}")

        s = df[col]
        if dropna:
            s = s.dropna()

        counts = s.value_counts(sort=False)

        if normalize == "percent":
            values = (counts / counts.sum() * 100).round(2).to_dict()
            y_label = "%"
        elif normalize == "count":
            values = counts.to_dict()
            y_label = "Count"
        else:
            raise ValueError("normalize must be 'percent' or 'count'")

        spec = {
            "y_label": y_label,
            "groups": [
                {
                    "name": col,
                    "values": values,
                }
            ],
            "style": spec.get("style", {}),
        }

    """Manual Mode"""
    style = spec.get("style", {})
    theme = style.get("theme", "classic")
    show_values = style.get("show_values", False)
    font_scale = float(style.get("font_scale", 1.0))

    if theme == "grayscale":
        plt.style.use("grayscale")
    else:
        plt.style.use("default")

    groups = spec.get("groups")
    if not groups:
        raise ValueError("categorical_profile requires non-empty 'groups'")

    y_label = spec.get("y_label", "%")

    fig, ax = plt.subplots(figsize=(14, 5))
    for item in ([ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels()):
        item.set_fontsize(item.get_fontsize() * font_scale)

    x, y, labels, group_centers = [], [], [], []
    pos = 0

    for g in groups:
        if "name" not in g or "values" not in g:
            raise ValueError("Each group must define 'name' and 'values'")
        values = g["values"]
        if not isinstance(values, dict) or not values:
            raise ValueError(f"Group '{g.get('name')}' has invalid values")

        start = pos
        for label, val in values.items():
            if not isinstance(val, (int, float)):
                raise ValueError(
                    f"Non-numeric value in group '{g['name']}': {label}"
                )
            x.append(pos); y.append(val); labels.append(label)
            pos += 1
        group_centers.append((start + pos - 1) / 2)
        pos += 1  # gap

    bars = ax.bar(x, y)
    ax.set_ylabel(y_label)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=90)
    ax.set_title(col, pad=14)

    # Only draw group labels if explicitly requested AND multiple groups exist
    show_group_labels = style.get("show_group_labels", False)

    if show_group_labels and len(groups) > 1:
        for center, g in zip(group_centers, groups):
            ax.text(
                center,
                -0.12 * max(y),
                g["name"],
                ha="center",
                va="top",
                fontsize=10 * font_scale
            )

    if show_values:
        for b in bars:
            ax.text(
                b.get_x() + b.get_width() / 2,
                b.get_height(),
                f"{b.get_height():.0f}",
                ha="center", va="bottom", fontsize=9 * font_scale
            )

    ax.grid(axis="y", alpha=0.3)
    ax.margins(x=0.01)

    caption = spec.get("caption")
    apply_caption(fig, caption)

    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def coef_plot(spec, cfg, name, model=None):
    if model is None:
        raise ValueError("coef_plot requires fitted model")

    ci_level = float(spec.get("ci", 0.95))
    drop = set(spec.get("drop", []))

    # Extract parameters safely
    params = np.asarray(model.params)
    conf = model.conf_int(alpha=1 - ci_level)

    # Resolve coefficient names
    names = getattr(model.model, "exog_names", None)
    if names is None:
        names = [f"x{i}" for i in range(len(params))]

    conf_df = pd.DataFrame(conf, index=names, columns=["low", "high"])

    labels, coef, low, high = [], [], [], []

    for name_, val in zip(names, params):
        if name_ in drop:
            continue
        labels.append(name_)
        coef.append(float(val))
        low.append(float(conf_df.loc[name_, "low"]))
        high.append(float(conf_df.loc[name_, "high"]))

    if not coef:
        raise ValueError("No coefficients left to plot after applying drop filters")

    # Sort by absolute coefficient magnitude (descending)
    order = sorted(range(len(coef)), key=lambda i: abs(coef[i]), reverse=True)

    labels = [labels[i] for i in order]
    coef = [coef[i] for i in order]
    low = [low[i] for i in order]
    high = [high[i] for i in order]

    y = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(6, 0.5 * len(labels) + 1))

    ax.errorbar(
        coef,
        y,
        xerr=[
            [c - l for c, l in zip(coef, low)],
            [h - c for h, c in zip(high, coef)],
        ],
        fmt="o",
        color="black",
        ecolor="black",
        capsize=3,
    )

    # Zero reference line
    ax.axvline(0, color="black", linestyle="--", linewidth=1)

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Coefficient estimate")
    ax.invert_yaxis()
    ax.set_title("Regression Coefficients", pad=12)

    ax.grid(axis="x", alpha=0.3)

    caption = spec.get("caption")
    apply_caption(fig, caption)

    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def heatmap(df, spec, cfg, name):

    x = spec["x"]
    y = spec["y"]
    normalize = spec.get("normalize", "none")
    cmap = spec.get("cmap", "Blues")

    ct = pd.crosstab(df[y], df[x])

    if normalize == "row":
        ct = ct.div(ct.sum(axis=1), axis=0)
    elif normalize == "col":
        ct = ct.div(ct.sum(axis=0), axis=1)

    fig, ax = plt.subplots(figsize=(1 + ct.shape[1], 1 + ct.shape[0]))

    im = ax.imshow(ct.values, cmap=cmap)

    ax.set_xticks(range(ct.shape[1]))
    ax.set_yticks(range(ct.shape[0]))
    ax.set_xticklabels(ct.columns, rotation=45, ha="right")
    ax.set_yticklabels(ct.index)

    for i in range(ct.shape[0]):
        for j in range(ct.shape[1]):
            ax.text(
                j, i,
                f"{ct.iloc[i, j]:.2f}" if normalize != "none" else int(ct.iloc[i, j]),
                ha="center", va="center",
                fontsize=8
            )

    ax.set_xlabel(x)
    ax.set_ylabel(y)
    fig.colorbar(im, ax=ax)

    caption = spec.get("caption")
    apply_caption(fig, caption)

    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def pie(df, spec, cfg, name):

    col = spec["column"]
    top_n = spec.get("top_n")
    other_label = spec.get("other_label", "Other")
    donut = spec.get("donut", False)

    counts = df[col].value_counts(dropna=True)

    if top_n and len(counts) > top_n:
        top = counts.iloc[:top_n]
        rest = counts.iloc[top_n:].sum()
        counts = top.copy()
        counts[other_label] = rest

    fig, ax = plt.subplots(figsize=(6, 6))

    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=90,
        counterclock=False
    )

    if donut:
        centre = plt.Circle((0, 0), 0.70, fc="white")
        ax.add_artist(centre)

    ax.set_title(col, pad=12)
    ax.axis("equal")

    caption = spec.get("caption")
    apply_caption(fig, caption)

    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def likert(df, spec, cfg, name):

    col = spec["column"]
    scale = spec["scale"]
    normalize = spec.get("normalize", True)

    counts = (
        df[col]
        .value_counts()
        .reindex(scale, fill_value=0)
    )

    if normalize:
        values = counts / counts.sum() * 100
        xlabel = "Percentage"
    else:
        values = counts
        xlabel = "Count"

    left = 0
    fig, ax = plt.subplots(figsize=(8, 2))

    colors = PALETTES.get("likert")

    for i, (label, val) in enumerate(zip(scale, values)):
        color = colors[i] if colors and i < len(colors) else None

        ax.barh(
            [col],
            [val],
            left=left,
            label=label,
            color=color
        )
        left += val

    ax.set_xlabel(xlabel)
    ax.set_yticks([])
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.25),
        ncol=3,
        frameon=False
    )

    ax.set_title(col, pad=12)
    ax.set_xlim(0, values.sum())

    caption = spec.get("caption")
    apply_caption(fig, caption)

    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def diverging_likert(df, column, spec, cfg, name, group_by=None):

    scale = spec["scale"]
    center = spec.get("center")
    labels = spec.get("labels", {})
    normalize = spec.get("normalize", True)

    if center not in scale:
        raise ValueError("Center value must be part of scale")

    def compute(series):
        counts = series.value_counts().reindex(scale, fill_value=0)
        if normalize:
            counts = counts / counts.sum() * 100
        return counts

    if group_by:
        groups = df[group_by].dropna().unique()
        data = {g: compute(df[df[group_by] == g][column]) for g in groups}
    else:
        data = {"All": compute(df[column])}

    fig, ax = plt.subplots(figsize=(8, 0.6 * len(data) + 2))

    y = np.arange(len(data))
    left_vals, right_vals, center_vals = [], [], []

    for vals in data.values():
        left = vals[vals.index < center].sum()
        right = vals[vals.index > center].sum()
        mid = vals.get(center, 0)
        left_vals.append(-left)
        right_vals.append(right)
        center_vals.append(mid)

    neg, _, _, _, pos = PALETTES["likert"]
    ax.barh(y, left_vals, color=neg, label="Negative")
    ax.barh(y, right_vals, color=pos, label="Positive")

    if center_vals:
        ax.barh(y, center_vals, left=left_vals, color="#cccccc", label="Neutral")

    ax.axvline(0, color="black", linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels(data.keys())
    ax.set_xlabel("Percentage")
    ax.set_title(column, pad=12)
    ax.legend()

    caption = spec.get("caption")
    apply_caption(fig, caption)

    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

def multiselect_profile(df, spec, cfg, name):
    col = spec["column"]
    sep = spec.get("separator", ";")
    normalize = spec.get("normalize", "percent")
    sort = spec.get("sort", "desc")
    top_n = spec.get("top_n")
    orientation = spec.get("style", {}).get("orientation", "horizontal")
    show_values = spec.get("style", {}).get("show_values", True)

    # explode multiselect column
    exploded = (
        df[col]
        .dropna()
        .astype(str)
        .str.split(sep)
        .explode()
        .str.strip()
    )

    counts = exploded.value_counts()

    if normalize == "percent":
        values = counts / counts.sum() * 100
        xlabel = "Percentage"
    else:
        values = counts
        xlabel = "Count"

    if sort == "desc":
        values = values.sort_values(ascending=False)
    elif sort == "asc":
        values = values.sort_values(ascending=True)

    if top_n:
        values = values.head(int(top_n))

    labels = values.index.tolist()
    nums = values.values

    fig, ax = plt.subplots(
        figsize=(8, 0.5 * len(labels) + 1)
    )

    if orientation == "horizontal":
        ax.barh(labels, nums)
        ax.invert_yaxis()
        ax.set_xlabel(xlabel)
        if show_values:
            for i, v in enumerate(nums):
                ax.text(v, i, f"{v:.1f}", va="center", ha="left")
    else:
        ax.bar(labels, nums)
        ax.set_ylabel(xlabel)
        if show_values:
            for i, v in enumerate(nums):
                ax.text(i, v, f"{v:.1f}", ha="center", va="bottom")

    ax.set_title(col, pad=12)

    save(fig, cfg["out_dir"], name, cfg["formats"], cfg["dpi"])

