from datetime import datetime
from typing import Optional

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
