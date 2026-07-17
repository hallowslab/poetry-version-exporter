from enum import Enum
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as get_version


class VersionSource(str, Enum):
    AUTO = "auto"
    METADATA = "metadata"
    PYPROJECT = "pyproject"


def _read_from_metadata(package_name: str) -> str:
    if package_name == "":
        raise ValueError("package name required to read from metadata")
    version = get_version(package_name)
    print(f"Got version from metadata: {version}")
    return version


def _read_from_pyproject(pyproject_path: Path) -> str:
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
    return str(version)


def export_version(
    package_name: str,
    pyproject_path: Path,
    output_path: Path,
    source: VersionSource = VersionSource.AUTO,
) -> str:
    if source is VersionSource.METADATA:
        try:
            version = _read_from_metadata(package_name)
        except PackageNotFoundError as e:
            raise PackageNotFoundError(
                f"Version from metadata unavailable for '{package_name}': {e}"
            ) from e
    elif source is VersionSource.PYPROJECT:
        version = _read_from_pyproject(pyproject_path)
    else:
        resolved: str | None = None
        # 1. Try getting from installed metadata
        if package_name != "":
            try:
                resolved = _read_from_metadata(package_name)
            except Exception as e:
                print(f"Failed to get version from metadata: {e}")

        # 2. Fallback to pyproject.toml
        if resolved is None:
            resolved = _read_from_pyproject(pyproject_path)
        version = resolved

    # 3. Write the version to output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        fh.write(f'__version__ = "{version}"\n')
    print(f"Wrote version to {output_path}")

    return version
