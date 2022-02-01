from datetime import datetime
from typing import Any
from typing import Optional

from pandas import to_datetime

from .models import Concert


def multiget(
    dictionary: dict[Any, Any],
    keys_to_get: list[str],
    defult: Any = None,
) -> dict[Any, Any]:
    ret = dictionary
    for key in keys_to_get[:-1]:
        ret = ret.get(key, {})
    return ret.get(keys_to_get[-1], defult)


class ResponseToConcertConverter:
    """Covert the setlist response from Setlist FM to the Concert model"""

    @classmethod
    def convert(cls, setlist_response: dict[str, Any]) -> Concert:
        venue = cls._create_venue_dict(setlist_response.get("venue"))

        songs = []
        for set_ in multiget(setlist_response, ["sets", "set"]):
            songs += [cls._create_song_dict(s) for s in set_.get("song")]

        concert = cls._create_concert_dict(setlist_response, venue, songs)
        return Concert(**concert)

    @classmethod
    def _create_venue_dict(cls, venue: Optional[dict[str, Any]]) -> dict[str, Any]:
        if venue is None:
            venue = {}

        return {
            "id": venue.get("id"),
            "name": venue.get("name"),
            "city": multiget(venue, ["city", "name"]),
            "state": multiget(venue, ["city", "state"], ""),
            "country": multiget(venue, ["city", "country", "code"], ""),
        }

    @classmethod
    def _create_song_dict(cls, song: Optional[dict[str, Any]]) -> dict[str, Any]:
        if not song:
            song = {}

        return {"name": song.get("name"), "is_cover": bool(song.get("cover"))}

    @classmethod
    def _create_concert_dict(
        cls, concert: dict[str, Any], venue: dict[str, Any], songs: list[dict[str, Any]]
    ) -> dict[str, Any]:
        def as_dt(date: Any) -> datetime:
            return to_datetime(date, format="%d-%m-%Y").to_pydatetime()

        return {
            "id": concert.get("id"),
            "url": concert.get("url"),
            "event_date": as_dt(concert.get("eventDate")),
            "venue": venue,
            "setlist": songs,
        }
