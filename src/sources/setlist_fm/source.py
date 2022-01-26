from dataclasses import dataclass
from pathlib import Path


@dataclass
class SetlistSource:
    """Interface for data sources."""

    name: str = "Setlist"

    def get_data(self) -> dict[str, str]:
        """Function that returns the data to save"""

    def save_data(self, data: dict[str, str], output_dir: Path) -> None:
        """Function that saves the data"""
