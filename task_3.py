"""The spotify user agent"""
from lib import (
    get_artist_by_id,
    get_artist_top_songs,
    get_artist_by_name,
    get_available_markets
)
from fastapi import FastAPI
import folium as fl

app = FastAPI(title="Spotify maps")

@app.get("/artists/by_name/{artist_name}")
async def artist_by_name(artist_name: str) -> dict:
    """
    Get artist by name
    """
    return get_artist_by_name(artist_name)

@app.get("/artists/by_id/{artist_id}")
async def artist_by_id(artist_id: str) -> dict:
    """
    Get artist by name
    """
    return get_artist_by_id(artist_id)

@app.get("/artists_top_tracks/by_id/{artist_id}")
async def top_tracks_by_id(
    artist_id: str, 
    country: str = "UA",
    limit: int = 1
    ) -> dict:
    """Get the artists top tracks"""
    return get_artist_top_songs(artist_id, country, limit)

@app.get("/available_markets")
async def markets() -> dict:
    """Get spotify's available markets"""
    return get_available_markets()

