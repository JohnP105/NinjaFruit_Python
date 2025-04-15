import pygame
import random
from typing import Dict
from constants import FRUIT_IMAGES


class Fruit:
    def __init__(self, x: int, fruit_type: str):
        self.x = x
        self.y = 0
        self.type = fruit_type
        self.sliced = False
        self.radius = 30
        self.image = FRUIT_IMAGES[fruit_type]
        self.rect = self.image.get_rect(center=(x, self.y))
        self.rotation = 0
        self.rotation_speed = random.uniform(-5, 5)
        self.scale = 1.0
        self.glow_surface = None
        self.create_glow()

    def create_glow(self):
        glow_size = 80
        self.glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        glow_color = (*[min(c + 50, 255) for c in self.image.get_at((30, 30))[:3]], 100)
        pygame.draw.circle(
            self.glow_surface,
            glow_color,
            (glow_size // 2, glow_size // 2),
            glow_size // 2,
        )

    def update(self):
        self.rotation += self.rotation_speed
        self.rect.center = (self.x, self.y)
        self.scale = min(1.0, self.scale + 0.05)  # Grow in effect
