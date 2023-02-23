"""The spotify user agent library"""
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

AUTHORIZE_TOKEN = authorize()

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
        headers={"Authorization": f"Bearer {AUTHORIZE_TOKEN}"}
    )

    return artist_response.json()

def get_artist_top_songs(
    artist_id: str, 
    country_code: str = "UA",
    limit: int = 5
) -> dict:
    """Get artist's top songs for the given country"""
    track_response = requests.get(
        f"{API_URL}/artists/{artist_id}/top-tracks?\
country={country_code}&limit={limit}",
        headers={"Authorization": f"Bearer {AUTHORIZE_TOKEN}"}
    )
    return track_response.json()

def get_artist_by_name(artist_name: str) -> dict:
    """
    Get the artist by his/her name
    """
    query = f"?q={artist_name}&type=artist&limit=1"
    artist_response = requests.get(
        f"{API_URL}/search/{query}",
        headers={"Authorization": f"Bearer {AUTHORIZE_TOKEN}"},
    )
    return artist_response.json()

def get_available_markets() -> dict:
    """Get available markets from api"""
    markets_response = requests.get(
        f"{API_URL}/markets",
        headers={"Authorization": f"Bearer {AUTHORIZE_TOKEN}"},
    )
    return markets_response.json()
