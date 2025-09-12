# src/game.py
import pygame

class GameLoop:
    def __init__(self, player):
        self.player = player
        self.clock = pygame.time.Clock()

    def loop(self, screen):
        running = True
        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.player.handle_input(keys)

            screen.fill((50,50,50))
            self.player.draw(screen)
            pygame.display.flip()
            self.clock.tick(60)
        return "quit"
