import os
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .fetcher import get_concerts
from .models import ConcertList
from src.config import Config
from src.logger import logger

OutputData = tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]


@dataclass
class SetlistSource:
    """Interface for data sources."""

    name: str = "Setlists FM"

    def get_data(self, config: Config, max_pages: int | None = None) -> OutputData:
        """Function that returns the data to save"""
        apikey = os.environ["SETLIST_FM_API_KEY"]

        logger.info("Fetching concerts...")
        concerts = get_concerts(apikey, config.setlist_fm_mbid, max_pages=max_pages)
        return ConcertList(concerts=concerts).to_frames()

    def save_data(self, data: OutputData, output_dir: Path) -> None:
        """Function that saves the data"""
        concerts, venues, songs = data

        for name, df in zip(["Concerts", "Venues", "Songs"], [concerts, venues, songs]):
            file_name = output_dir / f"{self.name} - {name}.csv"
            df.to_csv(file_name, index=False)
