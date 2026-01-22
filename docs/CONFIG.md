# Config Reference

## data
- `path` (required): CSV file path
- Paths are resolved relative to CWD

## variables
- `outcome`: dependent variable
- `predictors`: list of predictors

## transforms
- `recode`: explicit value mapping
- No implicit encoding

## artifacts.plots
- Declarative plot definitions.
- Aliases are not supported.

## plots
Controls plot output:
- `out_dir` (default: plots/)
- `formats` (default: [png])
- `dpi` (default: 300)
