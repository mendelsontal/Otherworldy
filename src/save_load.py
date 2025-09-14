# src/save_load.py
from .utils import save_json, load_json
import os
import re
from .player import Player
from .item import Item
from data import CONFIG

SAVE_DIR = "saves"
os.makedirs(SAVE_DIR, exist_ok=True)

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', "_", name)

def save_game(player):
    """Save the player data including full inventory grid with empty slots."""
    name = player.name or "default"
    filename = f"{sanitize_filename(name)}.json"
    path = os.path.join(SAVE_DIR, filename)

    total_slots = player.inventory_rows * player.inventory_cols
    inventory_data = [None] * total_slots  # Start with empty slots

    for idx, item in enumerate(player.inventory):
        if idx >= total_slots:
            break
        if item is None:
            inventory_data[idx] = None
        else:
            inventory_data[idx] = {
                "name": item.key,
                "amount": getattr(item, "amount", 1),
                "location": idx
            }

    data = {
        "name": player.name,
        "gender": player.gender,
        "x": player.x,
        "y": player.y,
        "hair_style": getattr(player, "hair_style", "Hair1"),
        "clothing_style": getattr(player, "clothing_style", "Clothing1"),
        "stats": player.stats,
        "inventory": inventory_data
    }

    save_json(path, data)
    print(f"Game saved: {path}")

def load_game(name):
    """Load player data including inventory with preserved empty slots."""
    if not name:
        return None

    filename = f"{sanitize_filename(name)}.json"
    path = os.path.join(SAVE_DIR, filename)
    if not os.path.exists(path):
        print(f"No save found for '{name}'")
        return None

    data = load_json(path)

    player = Player(
        name=data.get("name", "Hero"),
        gender=data.get("gender", "Male"),
        hair_style=data.get("hair_style", None),
        clothing_style=data.get("clothing_style", "Default"),
        stats=data.get("stats")
    )

    # Set player position
    player.x = data.get("x", CONFIG["screen_width"] // 2)
    player.y = data.get("y", CONFIG["screen_height"] // 2)

    # Load full inventory grid
    inventory_data = data.get("inventory", [])
    total_slots = player.inventory_rows * player.inventory_cols
    player.inventory = []

    for idx in range(total_slots):
        record = inventory_data[idx] if idx < len(inventory_data) else None
        if record is None:
            player.inventory.append(None)
        else:
            key = record.get("name")
            amount = record.get("amount", 1)
            if key in Item.items:
                new_item = Item.items[key].clone(amount=amount)
                new_item.location = idx
                player.inventory.append(new_item)
            else:
                player.inventory.append(None)

    return player
