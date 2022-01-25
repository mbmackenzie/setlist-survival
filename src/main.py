from pathlib import Path

import click
from dotenv import find_dotenv
from dotenv import load_dotenv

from src.data.ingest import Ingester

load_dotenv(find_dotenv())


def make_path(path_str: str) -> Path:
    """Convert string path to Path object"""
    path = Path(path_str)
    return path.resolve()


@click.group()
def cli() -> None:
    """CLI for setlist-survival project"""
    pass


@cli.command()
@click.option("-o", "output_dir", help="Path to output ingested sources to")
def ingest(output_dir: str) -> None:
    """Save data from each source to disk."""
    from src.data.sources import SpotifySource

    output_dir_path: Path = make_path(output_dir)

    sources = [SpotifySource()]
    Ingester(output_dir_path, sources).ingest()
