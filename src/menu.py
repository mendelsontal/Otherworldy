# src/menu.py
import pygame
import os
from .character_creation import run_character_creation
from .save_load import save_game, load_game
from .player import Player
from data import CONFIG
import time

SAVE_DIR = "saves"
os.makedirs(SAVE_DIR, exist_ok=True)

def get_saves():
    """Return list of tuples (filename, character_name, timestamp)"""
    files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".json")]
    saves = []
    for f in files:
        path = os.path.join(SAVE_DIR, f)
        timestamp = os.path.getmtime(path)
        name = f[:-5]  # strip .json
        saves.append((f, name, timestamp))
    # Sort by newest first
    saves.sort(key=lambda x: x[2], reverse=True)
    return saves

class Menu:
    def __init__(self, font, screen_width=CONFIG["screen_width"], screen_height=CONFIG["screen_height"]):
        self.font = font
        self.screen_width = screen_width
        self.screen_height = screen_height
        # dynamically include Load Game if saves exist
        self.update_options()

    def update_options(self):
        saves = get_saves()
        self.has_saves = bool(saves)
        self.options = ["New Game"]
        self.options.append("Load Game")
        self.options.append("Exit")
        self.selected = 0

    def loop(self, screen):
        clock = pygame.time.Clock()
        running = True

        while running:
            screen.fill((12, 12, 12))

            # Draw title
            title = self.font.render("Otherworldy RPG", True, (255, 220, 120))
            screen.blit(title, (self.screen_width//2 - title.get_width()//2, 60))

            # Draw menu options
            for i, opt in enumerate(self.options):
                color = (255,255,0) if i == self.selected else (200,200,200)
                txt = self.font.render(opt, True, color)
                screen.blit(txt, (self.screen_width//2 - txt.get_width()//2, 180 + i*60))

            pygame.display.flip()

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit", None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        choice = self.options[self.selected]
                        if choice == "Exit":
                            return "quit", None
                        elif choice == "New Game":
                            player = run_character_creation(screen, self.font, self.screen_width, self.screen_height)
                            return "new", player
                        elif choice == "Load Game":
                            player = self.load_game_menu(screen)
                            if player:
                                return "load", player

            clock.tick(60)

    def load_game_menu(self, screen):
        """Displays a menu to select a save file"""
        saves = get_saves()
        if not saves:
            return None

        selected = 0
        clock = pygame.time.Clock()
        while True:
            screen.fill((20, 20, 20))

            title = self.font.render("Select Save", True, (255, 220, 120))
            screen.blit(title, (self.screen_width//2 - title.get_width()//2, 60))

            for i, (_, name, ts) in enumerate(saves):
                color = (255,255,0) if i == selected else (200,200,200)
                date_str = time.ctime(ts)
                text = self.font.render(f"{name} - {date_str}", True, color)
                screen.blit(text, (self.screen_width//2 - text.get_width()//2, 180 + i*50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(saves)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(saves)
                    elif event.key == pygame.K_RETURN:
                        # Pass only the name to load_game, not filename
                        name_only = saves[selected][1]
                        data = load_game(name_only)
                        if data:
                            player = Player(
                                name=data.get("name", "Hero"),
                                gender=data.get("gender", "Male"),
                                hair_style=data.get("hair_style", None),
                                clothing_style=data.get("clothing_style", "Default"),
                                stats=data.get("stats") 
                            )

                            # Apply saved position (fallback to config center)
                            player.x = data.get("x", CONFIG["screen_width"] // 2)
                            player.y = data.get("y", CONFIG["screen_height"] // 2)

                            # Track which save this player came from (useful for pause menu)
                            player.save_name = name_only

                            # If Player has an update_image or similar, refresh the composed sprite
                            if hasattr(player, "update_image"):
                                player.update_image()

                            return player
                        else:
                            print(f"Failed to load save for {name_only}")
                    elif event.key == pygame.K_ESCAPE:
                        return None
                    
            clock.tick(60)

