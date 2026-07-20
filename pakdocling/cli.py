import typer

app = typer.Typer()

@app.command()
def hello() -> None:
    typer.echo("pakdocling is installed")

if __name__ == "__main__":
    app()