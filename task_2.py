import requests
import dotenv
import os

API_URL = "https://api.spotify.com/v1"
AUTH_URL = "https://accounts.spotify.com/api/token"
dotenv.load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def authorize() -> str:
    """
    Authorize the user

    Returns:
        str - the client token
    """
    auth_response = requests.post(
        AUTH_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        },
    )

    return auth_response.json()["access_token"]

def get_artist_by_id(artist_id: str) -> dict:
    """
    Get the artist's info json

    Args:
        artist_id: str - the artist id

    Returns:
        dict - the artist info dict
    """
    artist_response = requests.get(
        f"{API_URL}/artists/{artist_id}",
        headers={"Authorization": f"Bearer {authorize()}"}
    )

    return artist_response.json()
