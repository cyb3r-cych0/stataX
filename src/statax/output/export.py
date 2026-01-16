from pathlib import Path
import json
import pandas as pd

def ensure_outdir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

def export_regression(df: pd.DataFrame, cfg):
    ensure_outdir(cfg.out_dir)

    if "csv" in cfg.format:
        p = Path(cfg.out_dir) / "regression.csv"
        if p.exists() and not cfg.overwrite:
            raise FileExistsError(p)
        df.to_csv(p)

    if "latex" in cfg.format:
        p = Path(cfg.out_dir) / "regression.tex"
        if p.exists() and not cfg.overwrite:
            raise FileExistsError(p)
        p.write_text(df.to_latex())

def export_metadata(meta: dict, cfg):
    ensure_outdir(cfg.out_dir)
    p = Path(cfg.out_dir) / "run_metadata.json"
    if p.exists() and not cfg.overwrite:
        raise FileExistsError(p)
    p.write_text(json.dumps(meta, indent=2))

def export_plot_metadata(out_dir, name, spec):
    meta = {
        "kind": spec.get("kind"),
        "caption": spec.get("caption"),
        "source_column": spec.get("column"),
        "group_by": spec.get("group_by"),
        "scale": spec.get("scale"),
        "normalize": spec.get("normalize"),
    }

    path = Path(out_dir) / f"{name}.meta.json"
    path.write_text(json.dumps(meta, indent=2))