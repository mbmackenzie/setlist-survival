import json
from pathlib import Path
from typing import Any
from typing import Optional
from typing import Protocol
from typing import Union

import pandas as pd


OutputData = Union[pd.DataFrame, dict]


class DataSource(Protocol):
    """Interface for data sources."""

    name: str

    def get_data(self, **kwargs: Optional[Any]) -> OutputData:
        """Function that returns the data to save"""
        ...

    def save_data(self, data: OutputData, output_dir: Path) -> None:
        """Function that saves the data"""
        ...


class Ingester:
    """Helper to ingest data from multiple source"""

    output_dir: Path
    sources: list[DataSource]

    def __init__(self, output_dir: Path, sources: list[DataSource]):
        self.output_dir = output_dir
        self.sources = sources

    def ingest(self) -> None:
        """Ingest data from sources"""
        for source in self.sources:
            data = source.get_data()
            source.save_data(data, self.output_dir)
