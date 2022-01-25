import pydantic
from datetime import datetime

from typing import Optional

import pandas as pd
import tidybear as tb


class AudioFeatures(pydantic.BaseModel):
    duration_ms: Optional[int]
    time_signature: Optional[int]
    tempo: Optional[float]
    key: Optional[int]
    mode: Optional[int]
    danceability: Optional[float]
    energy: Optional[float]
    loudness: Optional[float]
    speechiness: Optional[float]
    acousticness: Optional[float]
    instrumentalness: Optional[float]
    liveness: Optional[float]
    valence: Optional[float]


class Track(pydantic.BaseModel):
    album_id: str
    id: str
    name: str
    features: Optional[AudioFeatures]


class Album(pydantic.BaseModel):
    type: str
    id: str
    name: str
    released: datetime
    num_tracks: int
    tracks: Optional[list[Track]]


class AlbumList(pydantic.BaseModel):
    albums: list[Album]

    def to_frame(self):
        records = []
        for album in self.albums:
            for track in album.tracks:
                as_record = self._track_to_record(album, track)
                records.append(as_record)

        df = pd.DataFrame(records)
        return tb.rename(df, id="song_id")

    def _track_to_record(self, album: Album, track: Track) -> dict:
        album_details = album.dict(include={"name", "released"})
        album_details["album_name"] = album_details.pop("name")

        return {
            **track.dict(include={"album_id", "id"}),
            **album_details,
            **track.dict(exclude={"album_id", "id", "features"}),
            **track.features.dict(),
        }

