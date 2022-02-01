from pathlib import Path
from typing import Any
from typing import Optional
from typing import Protocol
from typing import Union

import pandas as pd

from .logger import logger
from src.config import Config
from src.config import load_config

OutputData = Union[pd.DataFrame, dict]


CONFIG = load_config()


class DataSource(Protocol):
    """Interface for data sources."""

    name: str

    def get_data(self, config: Config, **kwargs: Optional[Any]) -> OutputData:
        """Function that returns the data to save"""

    def save_data(self, data: OutputData, output_dir: Path) -> None:
        """Function that saves the data"""


class Ingester:
    """Helper to ingest data from multiple source"""

    output_dir: Path
    sources: list[DataSource]

    def __init__(
        self,
        output_dir: Path,
        sources: list[DataSource],
        run_args: dict[str, Union[str, int]],
    ) -> None:
        self.output_dir = output_dir
        self.sources = sources
        self.run_args = run_args

    def ingest(self) -> None:
        """Ingest data from sources"""
        for source in self.sources:
            logger.info(f"Starting {source.name} ingestion")
            data = source.get_data(CONFIG, **self.run_args)

            logger.info(f"Exporting to {self.output_dir}")
            source.save_data(data, self.output_dir)
