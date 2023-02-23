"""The spotify user agent"""
from typing import Any
from lib import get_artist_by_id, get_artist_by_name

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
                print(f"• {key}")
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
    artist_json = get_artist_by_id(artist_id.split(',')[1])\
        if artist_id.lower().startswith("id")\
        else get_artist_by_name(artist_id.split(',')[1])
    parse_json(artist_json)

