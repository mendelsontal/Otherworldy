# src/save_load.py
from .utils import save_json, load_json
import os
import re

SAVE_DIR = "saves"
os.makedirs(SAVE_DIR, exist_ok=True)

def sanitize_filename(name):
    # Remove invalid filename characters
    return re.sub(r'[<>:"/\\|?*]', "_", name)

def save_game(player):
    # Use character name for filename
    name = player.name or "default"
    filename = f"{sanitize_filename(name)}.json"
    path = os.path.join(SAVE_DIR, filename)

    data = {
        "name": player.name,
        "gender": player.gender,
        "x": player.x,
        "y": player.y,
        "hair_style": getattr(player, "hair_style", "Hair1"),
        "clothing_style": getattr(player, "clothing_style", "Clothing1"),
    }
    save_json(path, data)
    print(f"Game saved: {path}")

def load_game(name):
    if not name:
        return None
    filename = f"{sanitize_filename(name)}.json"
    path = os.path.join(SAVE_DIR, filename)
    if not os.path.exists(path):
        print(f"No save found for '{name}'")
        return None
    data = load_json(path)
    return data
