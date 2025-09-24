import typer

app = typer.Typer(help="Starter Project CLI")


@app.command()
def hello(name: str = "world") -> None:
    print(f"Hello, {name}!")


if __name__ == "__main__":
    app()
