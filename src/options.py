import pygame
from .save_load import save_game

class OptionsMenu:
    def __init__(self, font):
        self.font = font
        self.options = ["Save", "Return to Game", "Main Menu", "Exit"]
        self.index = 0  # currently selected option

    def loop(self, screen, player):
        running = True
        while running:
            screen.fill((0, 0, 0))

            # Draw options with selection highlight
            for i, option in enumerate(self.options):
                color = (255, 255, 255) if i == self.index else (100, 100, 100)
                surf = self.font.render(option, True, color)
                screen.blit(surf, (100, 100 + i * 50))

            pygame.display.flip()

            # Handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "back"
                    elif event.key == pygame.K_UP:
                        self.index = (self.index - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.index = (self.index + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        selected = self.options[self.index]
                        if selected == "Save":
                            save_game(player)
                            return "back"
                        elif selected == "Return to Game":
                            return "back"  # returns to game
                        elif selected == "Main Menu":
                            return "menu"  # signal to return to main menu
                        elif selected == "Exit":
                            return "quit"