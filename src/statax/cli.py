import argparse
from statax.config.loader import load_config
from statax.core.engine import run
from statax.core.inspect import inspect_columns, inspect_types, inspect_missing


def main():
    parser = argparse.ArgumentParser(prog="statax")
    sub = parser.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run")
    r.add_argument("config")

    inspect = sub.add_parser("inspect")
    inspect_sub = inspect.add_subparsers(dest="inspect_cmd")

    cols = inspect_sub.add_parser("columns")
    cols.add_argument("path")

    types = inspect_sub.add_parser("types")
    types.add_argument("path")

    missing = inspect_sub.add_parser("missing")
    missing.add_argument("path")

    args = parser.parse_args()

    if args.cmd == "run":
        config = load_config(args.config)
        run(config)
        print("✔ Analysis completed successfully")

    elif args.cmd == "inspect" and args.inspect_cmd == "columns":
        inspect_columns(args.path)
        return

    elif args.cmd == "inspect" and args.inspect_cmd == "types":
        inspect_types(args.path)
        return

    elif args.cmd == "inspect" and args.inspect_cmd == "missing":
        inspect_missing(args.path)
        return
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
