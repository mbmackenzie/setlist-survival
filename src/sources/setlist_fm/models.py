from datetime import datetime
from typing import Optional

import pandas as pd
import pydantic


class Venue(pydantic.BaseModel):
    """A venue model"""

    id: str
    name: str
    city: str
    state: Optional[str]
    country: str


class Song(pydantic.BaseModel):
    """A song model"""

    name: str
    is_cover: bool


class Concert(pydantic.BaseModel):
    """A concert model"""

    id: str
    url: str
    event_date: datetime
    venue: Venue
    setlist: list[Song]


class ConcertList(pydantic.BaseModel):
    concerts: list[Concert]

    def to_frames(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        concert_items, venue_items, song_items = [], [], []

        for concert in self.concerts:
            concert_items.append(
                {
                    **concert.dict(exclude={"venue", "setlist"}),
                    "venue_id": concert.venue.id,
                }
            )

            if concert.venue:
                venue_items.append(concert.venue.dict())

            if concert.setlist:
                song_items += [
                    {"concert_id": concert.id, "song_number": i, **sl.dict()}
                    for i, sl in enumerate(concert.setlist, 1)
                ]

        concert_df = pd.DataFrame(concert_items)
        venue_df = pd.DataFrame(venue_items).drop_duplicates().reset_index(drop=True)
        songs_df = pd.DataFrame(song_items)

        return concert_df, venue_df, songs_df
