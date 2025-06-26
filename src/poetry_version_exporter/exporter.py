from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib

try:
    from importlib.metadata import version as get_version
except ImportError:
    from importlib_metadata import version as get_version  # for Python <3.8


def export_version(
    package_name: str,
    pyproject_path: Path,
    output_path: Path,
) -> str:
    version = None

    # 1. Try getting from installed metadata
    if package_name != "":
        try:
            version = get_version(package_name)
            print(f"Got version from metadata: {version}")
        except Exception as e:
            print(f"Failed to get version from metadata: {e}")

    # 2. Fallback to pyproject.toml
    if version is None:
        if not pyproject_path.exists():
            raise FileNotFoundError(f"{pyproject_path} does not exist")

        with pyproject_path.open("rb") as f:
            pyproject = tomllib.load(f)

        version = pyproject.get("tool", {}).get("poetry", {}).get(
            "version"
        ) or pyproject.get("project", {}).get("version")
        if not version:
            raise KeyError(
                "Missing version in [tool.poetry] or [project] section of pyproject.toml"
            )
        print(f"Got version from pyproject.toml: {version}")

    # 3. Write the version to output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        fh.write(f'__version__ = "{version}"\n')
    print(f"Wrote version to {output_path}")

    return version
