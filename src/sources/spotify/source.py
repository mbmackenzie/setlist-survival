from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .auth import get_access_token
from .fetcher import get_albums
from .fetcher import get_audio_features
from .fetcher import get_tracks
from .models import AlbumList
from src.logger import logger


INCLUDE_ALBUM_IDS = [
    "1FyNZvJ6MHO01kl3ySMPdc",
    "6KMkuqIwKkwUhUYRPL6dUc",
    "2qwN15acAl3sm3Idce5vK9",
    "5lnQLEUiVDkLbFJHXHQu9m",
    "3ilXDEG0xiajK8AbqboeJz",
    "2eprpJCYbCbPZRKVGIEJxZ",
    "28q2N44ocJECgf8sbHEDfY",
    "30ly6F6Xl0TKmyBCU50Khv",
    "4EnNuo8fG7dMoxMefbApRY",
]

# "7jy3rLJdDQY21OgRLCZ9sD"  # Foo Fighters


@dataclass
class SpotifySource:
    """Helper to ingest data from Spotify"""

    artist_id: str = "7jy3rLJdDQY21OgRLCZ9sD"
    name: str = "Spotify"

    def get_data(self) -> pd.DataFrame:
        access_token = get_access_token()
        logger.info("Access token acquired")

        all_releases = get_albums(access_token, self.artist_id)

        # filter for only LPs
        albums = [album for album in all_releases if album.id in INCLUDE_ALBUM_IDS]

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
