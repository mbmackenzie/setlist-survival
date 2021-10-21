import pydantic

from datetime import datetime
from typing import Optional

from pandas import to_datetime


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


class ResponseToConcertConverter:
    """Covert the setlist response from Setlist FM to the Concert model"""

    def __init__(self):
        pass

    def convert(self, setlist_response):
        venue = self._create_venue_dict(setlist_response.get("venue"))

        songs = []
        for set_ in setlist_response.get("sets").get("set"):
            songs += [self._create_song_dict(s) for s in set_.get("song")]

        concert = self._create_concert_dict(setlist_response, venue, songs)
        return Concert(**concert)

    def _create_venue_dict(self, venue):
        return {
            "id": venue.get("id"),
            "name": venue.get("name"),
            "city": self.__multiget(venue, ["city", "name"]),
            "state": self.__multiget(venue, ["city", "state"]),
            "country": self.__multiget(venue, ["city", "country", "code"]),
        }

    def _create_song_dict(self, song):
        return {"name": song.get("name"), "is_cover": bool(song.get("cover"))}

    def _create_concert_dict(self, concert, venue, songs):
        as_dt = lambda date: to_datetime(date).to_pydatetime()

        return {
            "id": concert.get("id"),
            "url": concert.get("url"),
            "event_date": as_dt(concert.get("eventDate")),
            "venue": venue,
            "setlist": songs,
        }

    def __multiget(self, dictionary: dict, keys_to_get: list[str]):
        ret = dictionary
        for key in keys_to_get[:-1]:
            ret = ret.get(key, {})
        return ret.get(keys_to_get[-1])
