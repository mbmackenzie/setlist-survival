from importlib import import_module
from pathlib import Path

import click
import yaml
from dotenv import load_dotenv

from src.ingest import Ingester

load_dotenv()


@click.group()
def cli() -> None:
    """CLI for setlist-survival project"""
    pass


@cli.command()
@click.option("-o", "output_dir", help="Path to output dir")
@click.option("-s", "use_sources", multiple=True, help="Sources to ingest")
def ingest(output_dir: str, use_sources: list[str]) -> None:
    """Save data from each source to disk."""
    config = yaml.safe_load(open("config.yaml"))

    sources = []
    for short_name, source_path in config["sources"].items():
        if short_name in use_sources:
            module_name, class_name = source_path.split(":")
            cls = getattr(import_module(module_name), class_name)
            sources.append(cls())

    output_dir_path: Path = Path(output_dir)
    Ingester(output_dir_path, sources).ingest()
