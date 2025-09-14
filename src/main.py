# src/main.py
import pygame
from .menu import Menu
from .pause_menu import PauseMenu
from data import CONFIG
from .save_load import save_game, load_game
from .maps.sydney import draw_map

pygame.init()
screen = pygame.display.set_mode((CONFIG["screen_width"], CONFIG["screen_height"]))
pygame.display.set_caption("Otherworldy RPG")
font = pygame.font.Font(None, 48)

# ------------------------
# Main Menu
# ------------------------
menu = Menu(font)
menu_result, player = menu.loop(screen)

while menu_result in ("new", "load") and player is not None:
    running = True
    clock = pygame.time.Clock()
    pause_menu = PauseMenu(font)

    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Open pause menu
                result, player = pause_menu.loop(screen, player)
                if result == "menu":
                    # Go back to main menu
                    menu_result, player = menu.loop(screen)
                    # Reset: if menu returns a player, continue; else exit
                    if player is None:
                        running = False
                        break
                elif result == "quit":
                    running = False

        if not running:
            break

        player.handle_input(keys)
        screen.fill((0, 0, 0))
        draw_map(screen, player)
        pygame.display.flip()
        clock.tick(60)

    # After game ends, ask main menu again
    #menu_result, player = menu.loop(screen)


pygame.quit()
