"""Unit tests for Typer CLI commands."""

from typer.testing import CliRunner

from pakdocling.cli import app

runner = CliRunner()


def test_cli_info_command() -> None:
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "Pakistani Document Intelligence Library" in result.stdout
    assert "Version:" in result.stdout
