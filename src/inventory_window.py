# src/inventory_window.py
import pygame
import os

class InventoryWindow:
    def __init__(self, font):
        # Keep original image
        self.original_bg = pygame.image.load("assets/images/UI/inventory.png").convert_alpha()
        self.background = self.original_bg  # start as original
        self.font = font

        

    def resize(self, screen):
        screen_rect = screen.get_rect()
        max_width = int(screen_rect.width * 0.8)
        max_height = int(screen_rect.height * 0.8)

        # Scale while keeping aspect ratio
        bg_rect = self.original_bg.get_rect()
        scale = min(max_width / bg_rect.width, max_height / bg_rect.height)

        new_size = (int(bg_rect.width * scale), int(bg_rect.height * scale))
        self.background = pygame.transform.smoothscale(self.original_bg, new_size)

    def draw(self, screen, player):
        # Resize each time (so it adapts to screen changes)
        self.resize(screen)

        # Center the window
        screen_rect = screen.get_rect()
        bg_rect = self.background.get_rect(center=screen_rect.center)

        # Draw the background
        screen.blit(self.background, bg_rect)

        small_font = pygame.font.Font(None, 35)
        
        # Draw player stats dynamically
        stats = player.stats
        x = bg_rect.x + 560
        y = bg_rect.y + 280
        line_height = 30

        for key in ("Title","Gold"):
            if key in player.stats:
                value = player.stats[key]
                stat_text = f"{key}: {value}"

                # shadow for readability
                shadow = small_font.render(stat_text, True, (0, 0, 0))
                screen.blit(shadow, (x+2, y+2))

                # gold color text
                stat_surf = small_font.render(stat_text, True, (212, 175, 55))
                screen.blit(stat_surf, (x, y))

                y += line_height
