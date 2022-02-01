from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .auth import get_access_token
from .fetcher import get_albums
from .fetcher import get_audio_features
from .fetcher import get_tracks
from .models import AlbumList
from src.config import Config
from src.logger import logger


@dataclass
class SpotifySource:
    """Helper to ingest data from Spotify"""

    name: str = "Spotify"

    def get_data(self, config: Config) -> pd.DataFrame:
        access_token = get_access_token()
        logger.info("Access token acquired")

        all_releases = get_albums(access_token, config.spotify_artist_id)

        # filter for only LPs
        allowed_albums = config.spotify_allowed_albums
        albums = [album for album in all_releases if album.id in allowed_albums]

        # get tracks in each album
        for album in albums:
            logger.info(f"Fetching album: {album.name}")
            tracks = get_tracks(access_token, album.id)

            # get the audio features for each track
            for track in tracks:
                audio_features = get_audio_features(access_token, track.id)
                track.features = audio_features

            album.tracks = tracks

        return AlbumList(albums=albums).to_frame()

    def save_data(self, data: pd.DataFrame, output_dir: Path) -> None:
        file_name = output_dir / f"{self.name}.csv"
        data.to_csv(file_name, index=False)
