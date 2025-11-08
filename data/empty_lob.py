import sys
import json

path = "/Users/ivan/Ludice/data/game.json"

def write_empty():
    try:
        with open(path,"r") as file:
            data = json.load(file)

    except Exception as e:
        raise TypeError(f"Error : {e}")