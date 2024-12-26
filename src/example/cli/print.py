import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def reflect(name: Annotated[str, typer.Argument(help="Name to display.")]) -> None:
    print(f"Hello from example: {name}!")
