from statax.artifacts.base import Artifact
from statax.output import plot_renderers as R

class PlotArtifact(Artifact):
    def __init__(self, artifact_id: str, kind: str, spec: dict):
        super().__init__(artifact_id, kind="plot")
        self.plot_kind = kind
        self.spec = spec

    def render(self, *, df, model, cfg, resolve):
        name = self.id

        if self.plot_kind == "histogram":
            R.histogram(df, resolve(self.spec["column"]), cfg, name)

        elif self.plot_kind == "bar":
            R.bar(df, resolve(self.spec["column"]), cfg, name)

        elif self.plot_kind == "box":
            R.box(
                df,
                resolve(self.spec["y"]),
                resolve(self.spec["by"]),
                cfg,
                name,
            )

        elif self.plot_kind == "scatter":
            R.scatter(
                df,
                resolve(self.spec["x"]),
                resolve(self.spec["y"]),
                cfg,
                name,
            )

        elif self.plot_kind == "residuals_vs_fitted":
            R.residuals_vs_fitted(model, cfg, name)

        else:
            raise ValueError(f"Unsupported plot kind: {self.plot_kind}")
