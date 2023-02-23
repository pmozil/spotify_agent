"""The spotify user agent"""
from lib import (
    get_artist_by_id,
    get_artist_top_songs,
    get_artist_by_name,
    get_country_lat_lon,
    get_available_markets
)
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import folium as fl
import pycountry as pc
import json

with open("countries.json", "r", encoding="utf-8") as file:
    COUNTRIES = json.loads(file.read())

app = FastAPI(title="Spotify maps")

@app.get("/artists/by_name/{artist_name}")
async def artist_by_name(artist_name: str) -> dict:
    """
    Get artist by name
    """
    return get_artist_by_name(artist_name)

@app.get("/artists/by_name/{artist_name}/top_tracks")
async def top_tracks_by_name(
    artist_name: str, 
    country: str = "UA",
    limit: int = 1
    ) -> dict:
    """Get the artists top tracks"""
    artist_id = get_artist_by_name(artist_name)['artists']['items'][0]['id']
    return get_artist_top_songs(artist_id, country, limit)

@app.get("/artists/by_name/{artist_name}/map", response_class=HTMLResponse)
async def artist_map_by_name(
    artist_name: str,
    use_openstreet: bool = False
):
    """Create a map for the artist's best songs by country"""
    artist = get_artist_by_name(artist_name)
    artist_id = artist['artists']['items'][0]['id']
    map = fl.Map(title=f"{artist['artists']['items'][0]['name']}'s \
most populat songs by country"
    )
    pins = fl.FeatureGroup(name="Top song pins")
    for market in get_available_markets()["markets"]:
        top_tracks = get_artist_top_songs(artist_id, market)
        top_track_name = top_tracks["tracks"][0]["album"]["name"]
        print(top_track_name)
        if use_openstreet:
            loc = get_country_lat_lon(market)
            cname = pc.countries.get(alpha_2=market)
            cname = cname.name if cname is not None else "Kosovo"
        else:
            loc, cname = COUNTRIES[market]
        
        pins.add_child(
            fl.Marker(
                location=list(loc),
                popup=f"{cname}: top song is {top_track_name}",
                icon=fl.Icon(),
            )
        )
    map.add_child(pins)
    return map.get_root().render()


@app.get("/artists/by_id/{artist_id}")
async def artist_by_id(artist_id: str) -> dict:
    """
    Get artist by name
    """
    return get_artist_by_id(artist_id)

@app.get("/artists/by_id/{artist_id}/top_tracks")
async def top_tracks_by_id(
    artist_id: str, 
    country: str = "UA",
    limit: int = 1
    ) -> dict:
    """Get the artists top tracks"""
    return get_artist_top_songs(artist_id, country, limit)

@app.get("/available_markets")
async def get_markets(
        use_openstreet: bool = False
) -> dict:
    "Get available market names for spotify"
    if not use_openstreet:
        return COUNTRIES
    res = {}
    countries = get_available_markets()
    # Bruh, no Kosovo in ISO-3166-1? That's not cool
    for country in countries["markets"]:
        country_name = pc.countries.get(alpha_2=country)
        res[country] = (
            get_country_lat_lon(country),
            country_name.name if country_name is not None else "Kosovo"
        )
    return res

@app.get("/available_markets/{country_code}")
async def country_loc(
    country_code: str,
    use_openstreet: bool = False
) -> tuple | None:
    """Get country's latitude and longitude"""
    if not use_openstreet:
        try:
            return COUNTRIES[country_code]
        except KeyError:
            return None
    country_name = pc.countries.get(alpha_2=country_code)
    country_name = country_name.name if country_name is not None else "Kosovo"
    loc = get_country_lat_lon(country_code)
    return loc, country_name

def dump_data():
    res = {}
    countries = get_available_markets()
    for country in countries["markets"]:
        country_name = pc.countries.get(alpha_2=country)
        country_name = country_name.name if country_name is not None else "Kosovo"
        res[country] = (
            get_country_lat_lon(country),
            country_name
        )
    with open("countries", "w") as file:
        json.dump(res, file, indent=4)

