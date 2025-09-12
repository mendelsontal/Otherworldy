# src/player.py
import pygame
from data import CONFIG  # absolute import
import os

class Player:
    def __init__(self, name="", gender="Male", hair_style="Medium 01 - Page", clothing_style="Clothing1", x=None, y=None, save_name=None):
        self.name = name
        self.gender = gender
        self.hair_style = hair_style
        self.clothing_style = clothing_style
        self.x = x if x is not None else CONFIG["screen_width"] // 2
        self.y = y if y is not None else CONFIG["screen_height"] // 2
        self.speed = CONFIG["player_speed"]

        # Load body
        self.body_frame = self.load_frame(f"assets/images/Characters/Body/{self.gender}/Idle.png", row=2)

        # Load hair
        self.hair_frame = self.load_frame(f"assets/images/Characters/Hair/{self.hair_style}/Idle.png", row=2)

        # Load default clothing: Torso, Legs, Feet
        self.torso_frame = self.load_frame(f"assets/images/Characters/Clothing/{self.gender}/Torso/Shirt 01 - Longsleeve Shirt/Idle.png", row=2)
        self.legs_frame = self.load_frame(f"assets/images/Characters/Clothing/{self.gender}/Legs/Pants 01 - Hose/Idle.png", row=2)
        self.feet_frame = self.load_frame(f"assets/images/Characters/Clothing/{self.gender}/Feet/Shoes 01 - Shoes/Idle.png", row=2)

        # Load head
        self.head_frame = self.load_frame(f"assets/images/Characters/Head/{self.gender}/Idle.png", row=2)

        # Combine all layers
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.update_image()

    def load_frame(self, path, row=0, col=0, frame_width=64, frame_height=64):
        """Load a specific frame from a sprite sheet"""
        if not os.path.exists(path):
            return pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        sheet = pygame.image.load(path).convert_alpha()
        rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
        return sheet.subsurface(rect)

    def update_image(self):
        """Blit all layers in correct order"""
        self.image.fill((0,0,0,0))
        # Order: body -> legs -> feet -> torso -> head -> hair
        self.image.blit(self.body_frame, (0,0))
        self.image.blit(self.legs_frame, (0,0))
        self.image.blit(self.feet_frame, (0,0))
        self.image.blit(self.torso_frame, (0,0))
        self.image.blit(self.head_frame, (0,0))
        self.image.blit(self.hair_frame, (0,0))

    def handle_input(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed

        self.x += dx
        self.y += dy

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
