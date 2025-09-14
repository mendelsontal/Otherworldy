# src/player.py
import pygame
import os
from data import CONFIG  # absolute import
from .maps import sydney

class Player:
    def __init__(self, name="", gender="Male", hair_style="Medium 01 - Page",
                 clothing_style="Clothing1", x=None, y=None, save_name=None, stats=None):
        self.name = name
        self.gender = gender
        self.hair_style = hair_style
        self.clothing_style = clothing_style
        self.x = x if x is not None else CONFIG["screen_width"] // 2
        self.y = y if y is not None else CONFIG["screen_height"] // 2
        self.speed = CONFIG["player_speed"]

        # State
        self.direction = "down"
        self.current_frame = 0
        self.frame_timer = 0

        self.on_shadow = False

        # Load animations for each layer
        self.body_frames   = self.load_spritesheet(f"assets/images/Characters/Body/{self.gender}/Walk.png")
        self.hair_frames   = self.load_spritesheet(f"assets/images/Characters/Hair/{self.hair_style}/Walk.png")
        self.head_frames   = self.load_spritesheet(f"assets/images/Characters/Head/{self.gender}/Walk.png")
        self.torso_frames  = self.load_spritesheet(f"assets/images/Characters/Clothing/{self.gender}/Torso/Shirt 01 - Longsleeve Shirt/Walk.png")
        self.legs_frames   = self.load_spritesheet(f"assets/images/Characters/Clothing/{self.gender}/Legs/Pants 01 - Hose/Walk.png")
        self.feet_frames   = self.load_spritesheet(f"assets/images/Characters/Clothing/{self.gender}/Feet/Shoes 01 - Shoes/Walk.png")

        # Character stats
        self.stats = stats or {"STR":5,"DEX":5,"AGI":5,"VIT":5,"INT":5}

        # Temporary image for blitting (composite)
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)

    def load_spritesheet(self, path, rows=4, cols=8, frame_width=64, frame_height=64):
        """Split a sprite sheet into [rows][cols] frames"""
        if not os.path.exists(path):
            return [[pygame.Surface((frame_width, frame_height), pygame.SRCALPHA) for _ in range(cols)] for _ in range(rows)]

        sheet = pygame.image.load(path).convert_alpha()
        frames = []
        for row in range(rows):
            row_frames = []
            for col in range(cols):
                rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
                row_frames.append(sheet.subsurface(rect))
            frames.append(row_frames)
        return frames

    def handle_input(self, keys):
        dx, dy = 0, 0
        moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.direction = "left"
            moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.direction = "right"
            moving = True
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
            self.direction = "up"
            moving = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
            self.direction = "down"
            moving = True

        new_x = self.x + dx
        new_y = self.y + dy

        # Check collision at player's center or feet
        from .maps.sydney import is_walkable, get_tile_type

        # Using the bottom-center of the player sprite
        foot_x = new_x + self.image.get_width() // 2
        foot_y = new_y + self.image.get_height() - 5  # a few pixels up from bottom

        # Check full movement first
        if is_walkable(foot_x, foot_y):
            self.x = new_x
            self.y = new_y
            # Store if on shadow tile
            self.on_shadow = get_tile_type(foot_x, foot_y) == "shadow"
        else:
            # Try sliding: horizontal
            foot_x_h = new_x + self.image.get_width() // 2
            foot_y_h = self.y + self.image.get_height() - 1
            if sydney.is_walkable(foot_x_h, foot_y_h):
                self.x = new_x
            # Try sliding: vertical
            foot_x_v = self.x + self.image.get_width() // 2
            foot_y_v = new_y + self.image.get_height() - 1
            if sydney.is_walkable(foot_x_v, foot_y_v):
                self.y = new_y

        # Animate walking
        if moving:
            self.frame_timer += 1
            if self.frame_timer >= 8:
                self.current_frame = (self.current_frame + 1) % 8
                self.frame_timer = 0
        else:
            self.current_frame = 0

    def draw(self, screen, offset_x=0, offset_y=0):
        # Map direction to row index
        row_map = {"down": 2, "left": 1, "right": 3, "up": 0}
        row = row_map[self.direction]

        # Clear old composite
        self.image.fill((0, 0, 0, 0))

        # Blit all layers in order
        self.image.blit(self.body_frames[row][self.current_frame], (0,0))
        self.image.blit(self.legs_frames[row][self.current_frame], (0,0))
        self.image.blit(self.feet_frames[row][self.current_frame], (0,0))
        self.image.blit(self.torso_frames[row][self.current_frame], (0,0))
        self.image.blit(self.head_frames[row][self.current_frame], (0,0))
        self.image.blit(self.hair_frames[row][self.current_frame], (0,0))

        # If on shadow tile, darken the character sprite
        draw_image = self.image
        if getattr(self, "on_shadow", False):
            dark_overlay = pygame.Surface(draw_image.get_size(), pygame.SRCALPHA)
            dark_overlay.fill((50, 50, 50, 180))  # dark gray with alpha
            draw_image = draw_image.copy()
            draw_image.blit(dark_overlay, (0,0), special_flags=pygame.BLEND_RGBA_MULT)

        # Draw sprite with camera offset
        screen.blit(draw_image, (self.x + offset_x, self.y + offset_y))
