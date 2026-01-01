class AliasError(Exception):
    pass

def resolve(name: str, aliases: dict | None):
    if not aliases:
        return name
    return aliases.get(name, name)

def resolve_list(names: list[str], aliases: dict | None):
    return [resolve(n, aliases) for n in names]

def validate_aliases(df_columns, aliases: dict):
    for alias, raw in aliases.items():
        if raw not in df_columns:
            raise AliasError(f"Alias '{alias}' maps to missing column '{raw}'")
