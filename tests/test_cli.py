from typer.testing import CliRunner
from starter_project.cli import app

runner = CliRunner()


def test_hello_default() -> None:
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Hello, world!" in result.output
