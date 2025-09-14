# src/main.py
import pygame
from .menu import Menu
from .pause_menu import PauseMenu
from data import CONFIG
from .save_load import save_game, load_game
from .maps.sydney import draw_map
from .player import Player
from .inventory_window import InventoryWindow
from .item import Item

pygame.init()
screen = pygame.display.set_mode((CONFIG["screen_width"], CONFIG["screen_height"]))
pygame.display.set_caption("Otherworldy RPG")
font = pygame.font.Font(None, 48)

# Load all items at startup
Item.load_items("data/items")  # <-- load all JSONs

# ------------------------
# Main Menu
# ------------------------
menu = Menu(font)
menu_result, player = menu.loop(screen)

# Ensure we always have a player object
if player is None:
    player = Player(name="Hero")
show_status = False
show_inventory = False

inventory_window = InventoryWindow(font)

while menu_result in ("new", "load") and player is not None:
    running = True
    clock = pygame.time.Clock()
    pause_menu = PauseMenu(font)

    while running:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    show_status = not show_status
                elif event.key == pygame.K_i:
                    show_inventory = not show_inventory
                elif event.key == pygame.K_ESCAPE:
                    if show_status:
                        show_status = False
                    elif show_inventory:
                        show_inventory = False
                    else:
                        result, new_player = pause_menu.loop(screen, player)
                        player = new_player or player

                        if result == "quit":
                            running = False
                            menu_result = None  # stop main loop
                            break
                        elif result == "menu":
                            menu_result, new_player = menu.loop(screen)
                            player = new_player
                            if player is None:
                                running = False
                                menu_result = None
                                break

            # Inventory drag-and-drop
            if show_inventory and player is not None:
                inventory_window.handle_event(event, player)

        # Update player only if inventory/status closed
        if player is not None and not show_status and not show_inventory:
            player.handle_input(keys)

        # --- DRAWING ---
        screen.fill((0, 0, 0))
        if player is not None:
            draw_map(screen, player)

             # Draw HP bar at top-left corner
            player.draw_hp_bar(screen, x=20, y=20, width=200, height=20)
            
            if show_status:
                Player.draw_status_window(screen, player, font)
            elif show_inventory:
                inventory_window.draw(screen, player)

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
