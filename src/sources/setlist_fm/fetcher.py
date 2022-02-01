import time

import requests

from .converter import ResponseToConcertConverter
from .models import Concert
from src.logger import logger


def get_concerts(
    apikey: str,
    mbid: str,
    max_pages: int | None = None,
) -> list[Concert]:

    payload = {
        "url": f"https://api.setlist.fm/rest/1.0/artist/{mbid}/setlists",
        "headers": {"Accept": "application/json", "x-api-key": apikey},
        "params": {"p": 1},
    }

    concerts = []
    converter = ResponseToConcertConverter()

    page_number, page_has_content = 1, True
    while page_has_content:

        if max_pages is not None and page_number > max_pages:
            break

        if page_number == 1 or page_number % 10 == 0:
            logger.info(f"Fetching page {page_number}...")

        payload["params"]["p"] = page_number  # type: ignore
        response = requests.get(**payload)
        data = response.json()

        if "setlist" not in data:
            page_has_content = False
            break

        setlists = data["setlist"]
        for setlist in setlists:
            concerts.append(converter.convert(setlist))

        time.sleep(5)
        page_number += 1

    return concerts
