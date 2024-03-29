import os

import pandas as pd
import tidybear as tb


def get_and_clean_spotify_data(data_dir: str) -> pd.DataFrame:
    spotify = pd.read_csv(os.path.join(data_dir, "Spotify.csv"))
    spotify["released"] = pd.to_datetime(spotify.released)

    spotify = spotify.loc[~spotify.name.str.contains("- Live"), :]

    one_by_one_mask = spotify.album_name.str.contains("One By One")
    spotify.loc[one_by_one_mask, "album_name"] = "One By One"

    return spotify


def get_and_clean_setlist_fm_data(data_dir: str) -> pd.DataFrame:
    concerts = pd.read_csv(os.path.join(data_dir, "Setlists FM - Concerts.csv"))
    songs = pd.read_csv(os.path.join(data_dir, "Setlists FM - Songs.csv"))
    venues = pd.read_csv(os.path.join(data_dir, "Setlists FM - Venues.csv"))

    songs["num_songs"] = songs.groupby("concert_id").song_number.transform(max)
    songs["set_position"] = (songs.song_number - 1) / songs.num_songs
    concerts["event_date"] = pd.to_datetime(concerts.event_date)

    setlists = (
        songs.loc[~songs.is_cover, :]
        .merge(concerts, left_on="concert_id", right_on="id")
        .merge(venues, left_on="venue_id", right_on="id")
        .loc[:, ["name_y", "country", "event_date", "set_position", "name_x"]]
    )

    setlists = tb.rename(
        setlists, "venue", "country", "event_date", "set_position", "name"
    )

    return setlists.dropna()


def create_full_data(data_dir: str) -> pd.DataFrame:
    spotify = get_and_clean_spotify_data(data_dir)
    setlist_fm = get_and_clean_setlist_fm_data(data_dir)

    setlist_fm["fm_name"] = setlist_fm.name.str.lower()
    setlist_fm.drop(columns=["name"], inplace=True)

    spotify_names = spotify.name.str.lower().unique()
    setlist_fm = setlist_fm.loc[setlist_fm.fm_name.isin(spotify_names)]

    final_data = setlist_fm.merge(
        spotify.assign(fm_name=lambda x: x.name.str.lower()),
        on="fm_name",
        how="right",
    ).drop("fm_name", axis=1)

    return final_data
