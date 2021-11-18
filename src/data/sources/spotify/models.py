from datetime import datetime
from typing import Optional

import pydantic


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

    @property
    def is_album(self) -> bool:
        return self.type == "album"


class AlbumList(pydantic.BaseModel):
    albums: list[Album]
