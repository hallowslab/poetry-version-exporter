import argparse
from pathlib import Path
from .exporter import export_version


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="poetry-version-exporter",
        description="Export version from pyproject.toml to _version.py",
    )
    parser.add_argument("-n","--name", type=str, default="")
    parser.add_argument(
        "-p", "--pyproject", type=Path, default=Path("pyproject.toml"),
        help="Path to pyproject.toml"
    )
    parser.add_argument(
        "-o","--output", type=Path, required=True,
        help="Path to write the _version.py file"
    )
    args = parser.parse_args()

    try:
        version = export_version(args.name, args.pyproject, Path(args.output))
        print(f"Exported version {version} to {args.output}")
    except Exception as e:
        print(f"Error[{e.__class__.__name__}]: {e}")
        exit(1)
