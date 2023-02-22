"""The spotify user agent"""
from typing import Any
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

def parse_json(data: dict | list | Any, *, parent={}, print_data: bool = True):
    """
    Print the receieved json

    Args:
        data: dict - the json
    """
    if isinstance(data, list):
        for elem in data:
            print(f"- {elem}")
        return
    elif isinstance(data, dict):
        print("Here are the available keys:")
        if print_data:
            for key, _ in data.items():
                print(f"{key}")
        next_entry = input("Which entry would you like to see?\n")
        if next_entry == ".." and parent:
            parse_json(parent)
            return
        if next_entry in data:
            parse_json(data[next_entry], parent=data)
            return
        print("No such entry in json. Please reenter the entry")
        parse_json(data, parent=parent)
        return
    print(data)

if __name__ == "__main__":
    artist_id = input("Please enter the artist id:\n")
    artist_json = get_artist_by_id(artist_id)
    print(artist_json)
    parse_json(artist_json)
