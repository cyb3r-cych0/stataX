import pandas as pd

def regression_table(model, alias_map=None):
    # Build base regression table
    df = pd.DataFrame({
        "coef": model.params,
        "std_err": model.bse,
        "t_or_z": model.tvalues,
        "p_value": model.pvalues,
    })

    # Apply alias labels if provided
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
