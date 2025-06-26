import textwrap
from pathlib import Path
import pytest
from unittest.mock import patch
from poetry_version_exporter.exporter import export_version


def test_export_from_pyproject(tmp_path: Path):
    # Create dummy pyproject.toml
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_content = textwrap.dedent(
        """
        [project]
        name = "demo-project"
        version = "1.2.3"
    """
    )
    pyproject_path.write_text(pyproject_content, encoding="utf-8")

    output_path = tmp_path / "_version.py"

    version = export_version(
        "demo-project", pyproject_path=pyproject_path, output_path=output_path
    )

    assert version == "1.2.3"
    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == '__version__ = "1.2.3"\n'


def test_raises_missing_key_in_project(tmp_path: Path):
    # Create dummy pyproject.toml
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_content = textwrap.dedent(
        """
        [project]
        name = "demo-project"
    """
    )
    pyproject_path.write_text(pyproject_content, encoding="utf-8")
    with pytest.raises(KeyError):
        export_version("...", pyproject_path, output_path=tmp_path)


def test_export_missing_pyproject(tmp_path: Path):
    output_path = tmp_path / "_version.py"
    pyproject_path = tmp_path / "missing_pyproject.toml"

    try:
        export_version("...", pyproject_path=pyproject_path, output_path=output_path)
    except FileNotFoundError as e:
        assert "missing_pyproject.toml does not exist" in str(e)
    else:
        assert False, "Expected FileNotFoundError"


def test_export_from_metadata(tmp_path: Path):
    output_path = tmp_path / "_version.py"

    with patch("poetry_version_exporter.exporter.get_version", return_value="9.9.9"):
        version = export_version("...", tmp_path, output_path=output_path)
        assert version == "9.9.9"
        assert output_path.exists()
        assert output_path.read_text(encoding="utf-8") == '__version__ = "9.9.9"\n'
