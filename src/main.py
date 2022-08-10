from importlib import import_module
from pathlib import Path

import click
from dotenv import load_dotenv

from src.config import load_config
from src.ingester import Ingester

load_dotenv()


def parse_run_args(arguments_list: list[str]) -> dict[str, str | int]:
    run_args: dict[str, str | int] = {}
    for run_arg in arguments_list:
        arg_name, value = run_arg.split("=")
        try:
            send_value: int | str = int(value)
        except ValueError:
            send_value = value

        run_args[arg_name] = send_value

    return run_args


@click.group()
def cli() -> None:
    """CLI for setlist-survival project"""
    pass


@cli.command()
def init() -> None:
    """Set up project to defaults"""
    pass


@cli.command()
@click.option("-o", "output_dir", help="Path to output dir")
@click.option("-s", "use_sources", multiple=True, help="Sources to ingest")
@click.option("--arg", "use_arguments", multiple=True, help="Any ingest arguments")
def ingest(output_dir: str, use_sources: list[str], use_arguments: list[str]) -> None:
    """Save data from each source to disk."""

    if output_dir is None:
        raise click.UsageError("Output directory is required")

    if len(use_sources) == 0:
        conf = click.confirm("All sources will be ingested. Continue?")
        if not conf:
            click.echo("Exiting...")
            return

    config = load_config()
    run_args = parse_run_args(use_arguments)

    sources = []
    for short_name, source_path in config.sources.items():
        if short_name in use_sources or len(use_sources) == 0:
            module_name, class_name = source_path.split("::")
            cls = getattr(import_module(module_name), class_name)
            sources.append(cls())

    output_dir_path: Path = Path(output_dir)
    Ingester(output_dir_path, sources, run_args).ingest()
