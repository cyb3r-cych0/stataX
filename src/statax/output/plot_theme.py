import matplotlib.pyplot as plt

DEFAULT_THEME = {
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
}

THEMES = {
    "classic": DEFAULT_THEME,
    "clean": {
        **DEFAULT_THEME,
        "axes.grid": False,
    },
    "journal": {
        **DEFAULT_THEME,
        "font.family": "serif",
        "font.size": 10,
        "axes.grid": False,
    },
}

PALETTES = {
    "likert": [
        "#d73027",  # strong negative
        "#fc8d59",
        "#fee08b",
        "#91bfdb",
        "#4575b4",  # strong positive
    ],
    "categorical": [
        "#4e79a7",
        "#f28e2b",
        "#e15759",
        "#76b7b2",
        "#59a14f",
        "#edc948",
    ],
    "binary": ["#4e79a7", "#e15759"],
}

def apply_theme(name: str | None):
    if not name:
        return

    theme = THEMES.get(name)
    if not theme:
        raise ValueError(f"Unknown plot theme: {name}")

    plt.rcParams.update(theme)
