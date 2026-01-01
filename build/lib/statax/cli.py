import argparse
from statax.config.loader import load_config
from statax.core.engine import run

def main():
    parser = argparse.ArgumentParser(prog="statax")
    sub = parser.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run")
    r.add_argument("config")

    args = parser.parse_args()

    if args.cmd == "run":
        config = load_config(args.config)
        run(config)
        print("✔ Analysis completed successfully")

if __name__ == "__main__":
    main()
