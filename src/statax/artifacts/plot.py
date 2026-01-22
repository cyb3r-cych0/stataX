from statax.artifacts.base import Artifact
from statax.output import plot_renderers as R
from statax.output.plot_theme import apply_theme
from statax.output.export import export_plot_metadata


class PlotArtifact(Artifact):
    def __init__(self, artifact_id: str, kind: str, spec: dict):
        super().__init__(artifact_id, kind="plot")
        self.plot_kind = kind
        self.spec = spec

    def render(self, *, df, model, cfg, resolve):
        name = self.id
        theme = self.spec.get("style", {}).get("theme")
        apply_theme(theme)

        if self.plot_kind == "histogram":
            R.histogram(
                df,
                resolve(self.spec["column"]),
                cfg,
                name
            )

        elif self.plot_kind == "bar":
            R.bar(
                df,
                resolve(self.spec["column"]),
                cfg,
                name
            )

        elif self.plot_kind == "box":
            R.box(
                df,
                resolve(self.spec["y"]),
                resolve(self.spec["by"]),
                cfg,
                name
            )

        elif self.plot_kind == "scatter":
            R.scatter(
                df,
                resolve(self.spec["x"]),
                resolve(self.spec["y"]),
                cfg,
                name
            )

        elif self.plot_kind == "residuals_vs_fitted":
            R.residuals_vs_fitted(
                model,
                cfg,
                name
            )

        elif self.plot_kind == "line":
            R.line(
                df,
                resolve(self.spec["x"]),
                resolve(self.spec["y"]),
                cfg,
                name
            )

        elif self.plot_kind == "rolling_mean":
            R.rolling_mean(
                df,
                resolve(self.spec["x"]),
                resolve(self.spec["y"]),
                self.spec.get("window", 7),
                cfg,
                name
            )

        elif self.plot_kind == "categorical_profile":
            R.categorical_profile(
                self.spec,
                cfg,
                name,
                df=df,
                resolve=resolve
            )

        elif self.plot_kind == "coef_plot":
            R.coef_plot(
                self.spec,
                cfg,
                name,
                model=model
            )

        elif self.plot_kind == "heatmap":
            R.heatmap(
                df,
                self.spec,
                cfg,
                name
            )

        elif self.plot_kind == "pie":
            R.pie(
                df,
                self.spec,
                cfg,
                name
            )

        elif self.plot_kind == "likert":
            R.likert(
                df,
                self.spec,
                cfg,
                name
            )

        elif self.plot_kind == "diverging_likert":
            R.diverging_likert(
                df,
                resolve(self.spec["column"]),
                self.spec,
                cfg,
                name,
                group_by=resolve(self.spec["group_by"]) if "group_by" in self.spec else None,
            )

        elif self.plot_kind == "multiselect_profile":
            R.multiselect_profile(
                df,
                self.spec,
                cfg,
                name
            )

        else:
            raise ValueError(f"Unsupported plot plot_kind: {self.plot_kind}")

        export_plot_metadata(
            cfg["out_dir"],
            name,
            self.spec
        )
