import json

from lib.spotify.models import AlbumList
from lib.spotify.auth import get_access_token
from lib.spotify.requests import get_albums, get_tracks, get_audio_features


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
    "1zQ6F8gMagKcPL4SoA80cx",
]


def main():

    # get access token
    access_token = get_access_token()

    # set artist ID - maybe changeable in the future
    artist_id: str = "7jy3rLJdDQY21OgRLCZ9sD"  # Foo Fighters

    # get artis's albums
    all_releases = get_albums(access_token, artist_id)

    # filter for only LPs
    albums = [album for album in all_releases if album.id in INCLUDE_ALBUM_IDS]

    # get tracks in each album
    for album in albums:
        tracks = get_tracks(access_token, album.id)

        # get the audio features for each track
        for track in tracks:
            audio_features = get_audio_features(access_token, track.id)
            track.features = audio_features

        album.tracks = tracks

    # save the data
    json_data = json.loads(AlbumList(albums=albums).json())
    with open("foo_fighter_discography.json", "w") as outfile:
        json.dump(json_data, outfile)
        outfile.close()


if __name__ == "__main__":
    main()
