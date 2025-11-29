import pytest
from unittest.mock import patch
from poetry_version_exporter.cli import main


def test_cli_version(capsys):
    import sys

    sys.argv = ["poetry-version-exporter", "--version"]

    # Expect SystemExit because argparse exits after printing version
    with pytest.raises(SystemExit) as e:
        main()

    captured = capsys.readouterr()
    assert "poetry-version-exporter v" in captured.out

    # Ensure it exited with code
    assert e.value.code == 0


@patch("poetry_version_exporter.cli.export_version")
def test_cli_runs_export(mock_export, capsys):
    mock_export.return_value = "1.2.3"
    import sys

    sys.argv = ["poetry-version-exporter", "--output", "dummy.py"]
    main()
    captured = capsys.readouterr()
    mock_export.assert_called_once()
    assert "Exported version 1.2.3" in captured.out
