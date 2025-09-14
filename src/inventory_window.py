# src/inventory_window.py
import pygame
import os

class InventoryWindow:
    def __init__(self, font):
        # Keep original image
        self.original_bg = pygame.image.load("assets/images/UI/inventory.png").convert_alpha()
        self.background = self.original_bg  # start as original
        self.font = font

        self.rows = 6
        self.cols = 9
        self.slots = []  # list of pygame.Rect for each slot
        self.items = {}  # mapping: slot_index -> item surface

        # for dragging
        self.dragging_item = None
        self.dragging_index = None
        self.drag_offset = (0, 0)

    def resize(self, screen):
        screen_rect = screen.get_rect()
        max_width = int(screen_rect.width * 0.8)
        max_height = int(screen_rect.height * 0.8)

        # Scale while keeping aspect ratio
        bg_rect = self.original_bg.get_rect()
        scale = min(max_width / bg_rect.width, max_height / bg_rect.height, 1.0)
        new_size = (int(bg_rect.width * scale), int(bg_rect.height * scale))
        self.background = pygame.transform.smoothscale(self.original_bg, new_size)

        # --- Calculate slot rects relative to bg_rect ---
        # Assume slots start at 40,40 inside the bg and are 64x64 pixels apart (change for your art!)
        slot_w, slot_h = 64, 64
        start_x, start_y = 40, 40
        spacing = 4

        scale_x = new_size[0] / self.original_bg.get_width()
        scale_y = new_size[1] / self.original_bg.get_height()

        self.slots = []
        for r in range(self.rows):
            for c in range(self.cols):
                x = int((start_x + c * (slot_w + spacing)) * scale_x)
                y = int((start_y + r * (slot_h + spacing)) * scale_y)
                w = int(slot_w * scale_x)
                h = int(slot_h * scale_y)
                self.slots.append(pygame.Rect(x, y, w, h))

    def draw(self, screen, player):
        # Resize each time (so it adapts to screen changes)
        self.resize(screen)

        # Center the window
        screen_rect = screen.get_rect()
        bg_rect = self.background.get_rect(center=screen_rect.center)

        # Draw the background
        screen.blit(self.background, bg_rect)

        # Define fonts
        small_font = pygame.font.Font(None, 35)
        medium_font = pygame.font.Font(None, 28)

        # Draw player stats dynamically
        stats = player.stats
        x = bg_rect.x + 560
        y = bg_rect.y + 220
        line_height = 30

        for key in ("Title","Gold"):
            if key in player.stats:
                value = player.stats[key]

                if key == "Gold":
                # Bigger and golden
                    text = f"{key}: {value}"
                    shadow = medium_font.render(text, True, (0, 0, 0))
                    screen.blit(shadow, (x + 2, y + 2))
                    surf = medium_font.render(text, True, (212, 175, 55))  # gold
                    screen.blit(surf, (x, y))

                elif key == "Title":
                    # Smaller and red
                    text = f"{key}: {value}"
                    shadow = small_font.render(text, True, (0, 0, 0))
                    screen.blit(shadow, (x + 2, y + 2))
                    surf = small_font.render(text, True, (212, 175, 55))  # gold
                    screen.blit(surf, (x, y))

                y += line_height
        # --- DRAW ITEM ICONS ---
        self.draw_items(screen, bg_rect)

    def draw_items(self, screen, bg_rect):
        for idx, rect in enumerate(self.slots):
            world_rect = rect.move(bg_rect.topleft)  # align with centered bg
            if idx in self.items:
                item_surf = self.items[idx]
                screen.blit(item_surf, item_surf.get_rect(center=world_rect.center))

        # Draw dragged item on top of mouse
        if self.dragging_item:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.blit(self.dragging_item, (mouse_x + self.drag_offset[0], mouse_y + self.drag_offset[1]))
