# poetry-version-exporter

[![Tests](https://github.com/hallowslab/poetry-version-exporter/actions/workflows/CI-CD.yml/badge.svg)](https://github.com/hallowslab/poetry-version-exporter/actions)

A simple utility to export your Python package version into a `_version.py` file.

---

## 🔧 Use Case

Use this when you want to embed your package version (from `pyproject.toml` or installed metadata) into your source code as:

```python
__version__ = "0.1.0"
