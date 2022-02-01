import functools

import yaml
from pydantic import BaseModel


class Config(BaseModel):
    sources: dict[str, str]
    spotify_artist_id: str
    setlist_fm_mbid: str
    spotify_allowed_albums: list[str]


@functools.lru_cache(maxsize=1)
def load_config() -> Config:
    with open("config.yaml") as f:
        config_dict = yaml.safe_load(f)

    return Config(**config_dict)
