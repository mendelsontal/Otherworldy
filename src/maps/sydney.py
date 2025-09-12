# src/maps/sydney.py
import pygame

map_data = [
    [0,1,0,1],
]

TILE_SIZE = 256
tileset = {
    0: pygame.image.load("assets/images/Structure/Houses/Brick House A.png"),
    1: pygame.image.load("assets/images/Structure/Houses/Brick House B.png"),
    2: pygame.image.load("assets/images/Structure/Houses/Paneled House A.png"),
}

def draw_map(screen, data=map_data):
    for y, row in enumerate(data):
        for x, tile in enumerate(row):
            screen.blit(tileset[tile], (x*TILE_SIZE, y*TILE_SIZE))
