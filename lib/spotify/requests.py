import requests
from pandas import to_datetime

from .models import Album, Track, AudioFeatures


def make_album(response: dict) -> Album:
    return Album(
        **{
            "type": response.get("album_type"),
            "id": response.get("id"),
            "name": response.get("name"),
            "released": to_datetime(response.get("release_date")),
            "num_tracks": response.get("total_tracks"),
        }
    )


def make_track(response: dict, album_id: str) -> Track:
    return Track(
        **{"album_id": album_id, "id": response.get("id"), "name": response.get("name")}
    )


def get_albums(access_token: str, artist_id: str) -> list[Album]:
    payload = {
        "url": f"https://api.spotify.com/v1/artists/{artist_id}/albums",
        "headers": {"Authorization": f"Bearer {access_token}"},
        "params": {"market": "US", "limit": 50},
    }

    response = requests.get(**payload)
    data = response.json()

    return [make_album(album) for album in data["items"]]


def get_tracks(access_token: str, album_id: str) -> list[Track]:
    payload = {
        "url": f"https://api.spotify.com/v1/albums/{album_id}/tracks",
        "headers": {"Authorization": f"Bearer {access_token}"},
        "params": {"market": "US", "limit": 50},
    }

    response = requests.get(**payload)
    data = response.json()

    return [make_track(track, album_id) for track in data["items"]]


def get_audio_features(access_token: str, track_id: str) -> AudioFeatures:
    payload = {
        "url": f"https://api.spotify.com/v1/audio-features/{track_id}",
        "headers": {"Authorization": f"Bearer {access_token}"},
        "params": {"market": "US", "limit": 50},
    }

    response = requests.get(**payload)
    data = response.json()

    return AudioFeatures(**data)

