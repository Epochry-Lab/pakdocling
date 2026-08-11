"""Command Line Interface for pakdocling using Typer."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from pakdocling import __version__
from pakdocling.pipeline import DocumentConverter

app = typer.Typer(
    name="pakdocling",
    help="Pakistani Document Intelligence Library - Docling-aligned CLI",
    add_completion=False,
)

console = Console()


@app.command()
def convert(
    image_path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="Path to Pakistani document image (JPG, PNG, WebP, TIFF)",
    ),
    doc_type: str = typer.Option(
        "auto",
        "--doc-type",
        "-t",
        help="Document type: auto, cnic, matric, intermediate, degree",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Path to output JSON file to save extraction results",
    ),
    pretty: bool = typer.Option(
        True,
        "--pretty/--compact",
        help="Format output JSON with pretty printing",
    ),
    preprocess: bool = typer.Option(
        True,
        "--preprocess/--no-preprocess",
        help="Enable OpenCV deskewing and image enhancement",
    ),
) -> None:
    """Convert document image into structured JSON format (Docling API)."""
    console.print(f"[bold blue]Converting document:[/bold blue] {image_path}")

    try:
        converter = DocumentConverter()
        result = converter.convert(
            source=str(image_path),
            doc_type=doc_type,
            do_preprocess=preprocess,
        )

        json_data = result.export_to_json(indent=2 if pretty else None)

        if output:
            output.write_text(json_data, encoding="utf-8")
            console.print(f"[bold green]✓ Structured JSON saved to:[/bold green] {output}")
        else:
            typer.echo(json_data)

    except Exception as e:
        console.print(f"[bold red]Conversion Error:[/bold red] {e}")
        raise typer.Exit(code=1) from e


@app.command()
def extract(
    image_path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="Path to Pakistani document image (JPG, PNG, WebP, TIFF)",
    ),
    doc_type: str = typer.Option(
        "auto",
        "--doc-type",
        "-t",
        help="Document type: auto, cnic, matric, intermediate, degree",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Path to output JSON file to save extraction results",
    ),
    pretty: bool = typer.Option(
        True,
        "--pretty/--compact",
        help="Format output JSON with pretty printing",
    ),
    preprocess: bool = typer.Option(
        True,
        "--preprocess/--no-preprocess",
        help="Enable OpenCV deskewing and image enhancement",
    ),
) -> None:
    """Alias command for convert."""
    convert(
        image_path=image_path,
        doc_type=doc_type,
        output=output,
        pretty=pretty,
        preprocess=preprocess,
    )


@app.command()
def info() -> None:
    """Display pakdocling installation details and supported document models."""
    info_panel = Panel.fit(
        f"[bold cyan]Pakistani Document Intelligence Library (pakdocling)[/bold cyan]\n"
        f"[bold white]Version:[/bold white] {__version__}\n\n"
        f"[bold yellow]Supported Documents (v1):[/bold yellow]\n"
        f"  • CNIC (Computerized National Identity Card - Old Green & New Blue Smart Cards)\n"
        f"  • Matriculation Certificate (BISE 10th Grade / SSC)\n"
        f"  • Intermediate Certificate (BISE 12th Grade / HSSC / FSc / ICS)\n"
        f"  • University Degree & Transcript (HEI Degrees & Transcripts)\n\n"
        f"[bold green]Core Technology Stack:[/bold green]\n"
        f"  • EasyOCR & OpenCV Image Preprocessing\n"
        f"  • Pydantic Schema Validation & Typer CLI",
        title="Pakdocling Info",
        border_style="cyan",
    )
    console.print(info_panel)


if __name__ == "__main__":
    app()
