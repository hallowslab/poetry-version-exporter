# poetry-version-exporter

[![Tests](https://github.com/hallowslab/poetry-version-exporter/actions/workflows/CI-CD.yml/badge.svg)](https://github.com/hallowslab/poetry-version-exporter/actions)

A lightweight CLI utility that exports your project's version (from
`pyproject.toml` or installed package metadata) into a `_version.py`
file.

This makes it easy to access the version inside your Python package at
runtime without parsing config files or depending on build tools.

## Features

- Extracts version from:
    - Installed package metadata (preferred)
    - `pyproject.toml` (`[tool.poetry]` or `[project]` section)
- Writes a simple `_version.py` file containing\
 `__version__ = "x.y.z"`
- Zero runtime dependencies on Python 3.11+ (One dependency (tomli) on Python < 3.11)
- Works with both Poetry and PEP 621 metadata
- Provides a clean CLI interface
- Useful for packaging, logging, debugging, and runtime version checks

## Installation

Install via pip:

```sh
pip install poetry-version-exporter
```

Or install from source:

```sh
pip install .
```

## How It Works

Running the CLI reads the version from your project and generates a file
such as:

```python
__version__ = "0.1.0"
```

You can then import it in your package:

```python
from ._version import __version__
```

This avoids runtime dependency on `pyproject.toml`, which won't exist
inside wheels or source artifacts.

## Usage

### Basic example

- Defaults to pyproject.toml

```sh
poetry-version-exporter -o mypackage/_version.py
```

### Including a package name

```sh
poetry-version-exporter --name mypackage -o mypackage/_version.py
```

### Custom pyproject.toml location

```sh
poetry-version-exporter --pyproject ./config/pyproject.toml -o src/_version.py
```

### Showing exporter version

```sh
poetry-version-exporter --version
```

## Output File Example

```python
__version__ = "0.3.1"
```

## Python API

```python
from poetry_version_exporter import export_version

version = export_version(
 package_name="mypackage",
 pyproject_path="pyproject.toml",
 output_path="mypackage/_version.py"
)
```

## Contributing

1. Fork the repo
2. Create a new branch
3. Submit a pull request
