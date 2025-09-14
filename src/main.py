# src/main.py
import pygame
from .menu import Menu
from .pause_menu import PauseMenu
from data import CONFIG
from .save_load import save_game, load_game
from .maps.sydney import draw_map
from .player import Player  # ensure Player.draw_status_window is available
from .inventory_window import InventoryWindow  # NEW

pygame.init()
screen = pygame.display.set_mode((CONFIG["screen_width"], CONFIG["screen_height"]))
pygame.display.set_caption("Otherworldy RPG")
font = pygame.font.Font(None, 48)

# ------------------------
# Main Menu
# ------------------------
menu = Menu(font)
menu_result, player = menu.loop(screen)
show_status = False  # track whether status window is open
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
                    # Toggle status window
                    show_status = not show_status

                elif event.key == pygame.K_i:  # Toggle inventory
                    show_inventory = not show_inventory

                elif event.key == pygame.K_ESCAPE:
                    if show_status:
                        # Close status window if open
                        show_status = False
                    else:
                        # Open pause menu
                        result, player = pause_menu.loop(screen, player)
                        if result == "menu":
                            menu_result, player = menu.loop(screen)
                            if player is None:
                                running = False
                                break
                        elif result == "quit":
                            running = False

        if not running:
            break

        # Update player only if status window is closed
        if not show_status:
            player.handle_input(keys)

        # Draw map and player
        screen.fill((0, 0, 0))
        draw_map(screen, player)

        # Draw status window if toggled
        if show_status:
            Player.draw_status_window(screen, player, font)
        elif show_inventory:
            inventory_window.draw(screen, player)

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
