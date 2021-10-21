import os
import requests

AUTH_URL = "https://accounts.spotify.com/api/token"

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET_KEY = os.getenv("SPOTIFY_SECRET_KEY")


def get_access_token() -> str:

    auth_response = requests.post(
        AUTH_URL,
        {
            "grant_type": "client_credentials",
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_SECRET_KEY,
        },
    )

    auth_response_data = auth_response.json()
    return auth_response_data["access_token"]

