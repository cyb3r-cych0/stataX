import pandas as pd

def regression_table(model, alias_map=None):
    """
    Build regression table directly from a fitted statsmodels result.
    model + model.model.exog_names
    """
    if model is None:
        raise ValueError("regression_table() called with model=None")

    # column names
    if hasattr(model.model, "exog_names"):
        cols = model.model.exog_names
    else:
        cols = [f"x{i}" for i in range(len(model.params))]

    # core statistics
    coef = pd.Series(model.params, index=cols)
    se = pd.Series(model.bse, index=cols)

    # t for OLS, z for Logit
    stat = (
        pd.Series(model.tvalues, index=cols)
        if hasattr(model, "tvalues")
        else pd.Series(model.zvalues, index=cols)
    )

    pval = pd.Series(model.pvalues, index=cols)

    df = pd.DataFrame({
        "coef": coef,
        "std_err": se,
        "t_or_z": stat,
        "p_value": pval,
    })

    # optional confidence intervals
    if hasattr(model, "conf_int"):
        ci = model.conf_int()
        if not isinstance(ci, pd.DataFrame):
            ci = pd.DataFrame(
                ci,
                index=cols,
                columns=["ci_low", "ci_high"],
            )
        else:
            ci.columns = ["ci_low", "ci_high"]
            ci.index = cols


        df = pd.concat([df, ci], axis=1)

    # alias labeling
    if alias_map:
        new_index = []
        for name in df.index:
            if name == "const":
                new_index.append("const")
            else:
                label = alias_map.get(name, name)
                new_index.append(f"{name} ({label})")
        df.index = new_index

    return df.round(4)
