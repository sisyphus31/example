"""Parse bookcision json file.

./example-cli parse --help

uv run example-cli explain --verbose
./example-cli parse ~/Downloads/1735186115029.json ~/Downloads/output.html
"""

import typer
from typing_extensions import Annotated

import logging
import json

from .print import app as print_app


logging.basicConfig(level=logging.INFO)

app = typer.Typer()
app.add_typer(print_app, name="print")


@app.command()
def explain(
    verbose: Annotated[bool, typer.Option(help="Show additional info.")] = True,
) -> None:
    logging.info(
        "The purpose of this app is to show how uv and typer work. And parse bookcision jsons."
    )
    if verbose:
        logging.info("Typer seems cool!")
        logging.info(
            "For more information on boolean CLI options, see here: https://typer.tiangolo.com/tutorial/parameter-types/bool/?h=bool"
        )


@app.command()
def parse(
    file: Annotated[str, typer.Argument(help="Path to bookcision json file.")],
    output_path: Annotated[
        str, typer.Argument(help="path to save the formatted results to.")
    ],
) -> None:
    """Convert bookcision json into a html file that can be imported into notes."""
    with open(file, "r") as fs:
        data = json.load(fs)

    highlights = data["highlights"]
    title = data["title"]
    logging.info(highlights[0].keys())
    reformatted_text = []
    notes_count = 0

    reformatted_text.append(f"""
        <header><h1>{title}</h1><header>
        <br/>
        <p>#book-notes</p>
        <br/>
        <ul>
    """)
    for record in highlights:
        text, note = record["text"], record["note"]
        reformatted_text.append(f"<li>{text}</li>")
        if note:
            reformatted_text.append(f"<ul><li><b>NOTE:</b><u>{note}</u></li></ul>")
            notes_count += 1
    reformatted_text.append("</ul>")

    with open(output_path, mode="wt", encoding="utf-8") as myfile:
        myfile.write("".join(reformatted_text))
    logging.info(f"{len(highlights)=}, {notes_count=}")


def entrypoint() -> None:
    """Entry point into the CLI application."""
    app()
