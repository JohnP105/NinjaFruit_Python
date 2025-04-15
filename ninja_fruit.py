import pygame
import sys
import random
import threading
import signal
import json
from typing import List, Tuple, Dict
import time
import os

from constants import *
from fruit import Fruit
from sound_manager import SoundManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ninja Fruit")
        self.clock = pygame.time.Clock()
        self.fruits: List[Fruit] = []
        self.score = 0
        self.game_over = False
        self.fruit_spawner_thread = None
        self.lock = threading.Lock()

        # Initialize managers
        self.sound_manager = SoundManager()

        # Load fonts and images
        self.title_font = pygame.font.Font(None, 48)
        self.score_font = pygame.font.Font(None, 36)
        self.load_images()

        # Create background
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.create_background()

        # Load high score
        try:
            with open("high_score.json", "r") as f:
                self.high_score = json.load(f).get("high_score", 0)
        except FileNotFoundError:
            self.high_score = 0

    def load_images(self):
        for fruit_type in FRUIT_TYPES:
            try:
                image_path = os.path.join("images", f"{fruit_type}.png")
                image = pygame.image.load(image_path).convert_alpha()
                # Scale images to appropriate size
                image = pygame.transform.scale(image, (60, 60))
                FRUIT_IMAGES[fruit_type] = image
            except pygame.error:
                print(f"Warning: Could not load image for {fruit_type}")
                # Fallback to colored circle if image loading fails
                FRUIT_IMAGES[fruit_type] = pygame.Surface((60, 60), pygame.SRCALPHA)
                pygame.draw.circle(
                    FRUIT_IMAGES[fruit_type],
                    (255, 0, 0) if fruit_type != "bomb" else (0, 0, 0),
                    (30, 30),
                    30,
                )

    def create_background(self):
        self.background.fill(BACKGROUND_COLOR)
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(
                self.background, (230, 230, 230), (x, 0), (x, SCREEN_HEIGHT), 1
            )
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(
                self.background, (230, 230, 230), (0, y), (SCREEN_WIDTH, y), 1
            )

    def spawn_fruit(self):
        while not self.game_over:
            time.sleep(FRUIT_SPAWN_INTERVAL)
            if random.random() < BOMB_SPAWN_CHANCE:
                fruit_type = "bomb"
            else:
                fruit_type = random.choice(FRUIT_TYPES)
            x = random.randint(50, SCREEN_WIDTH - 50)
            with self.lock:
                self.fruits.append(Fruit(x, fruit_type))

    def handle_slice(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]):
        with self.lock:
            for fruit in self.fruits:
                if not fruit.sliced:
                    if self.line_intersects_circle(
                        start_pos, end_pos, (fruit.x, fruit.y), fruit.radius
                    ):
                        fruit.sliced = True
                        if fruit.type != "bomb":
                            self.score += 10
                            self.sound_manager.play_sound("slice")
                            self.create_slice_effect(start_pos, end_pos)
                        else:
                            self.score = max(0, self.score - 20)
                            self.sound_manager.play_sound("bomb")

    def create_slice_effect(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]):
        effect_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.line(effect_surface, (*SLICE_COLOR, 200), start_pos, end_pos, 3)
        self.screen.blit(effect_surface, (0, 0))
        pygame.display.flip()
        time.sleep(0.1)

    def line_intersects_circle(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        center: Tuple[int, int],
        radius: int,
    ) -> bool:
        x1, y1 = start
        x2, y2 = end
        cx, cy = center

        dx = x2 - x1
        dy = y2 - y1
        fx = x1 - cx
        fy = y1 - cy

        a = dx * dx + dy * dy
        b = 2 * (fx * dx + fy * dy)
        c = fx * fx + fy * fy - radius * radius

        discriminant = b * b - 4 * a * c
        return discriminant >= 0

    def update(self):
        with self.lock:
            for fruit in self.fruits[:]:
                if not fruit.sliced:
                    fruit.y += FRUIT_SPEED
                    fruit.update()
                    if fruit.y > SCREEN_HEIGHT:
                        self.fruits.remove(fruit)
                else:
                    self.fruits.remove(fruit)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for fruit in self.fruits:
            if not fruit.sliced:
                glow_pos = (fruit.x - 40, fruit.y - 40)
                self.screen.blit(fruit.glow_surface, glow_pos)

                rotated_image = pygame.transform.rotate(fruit.image, fruit.rotation)
                scaled_size = (int(60 * fruit.scale), int(60 * fruit.scale))
                scaled_image = pygame.transform.scale(rotated_image, scaled_size)
                fruit_rect = scaled_image.get_rect(center=(fruit.x, fruit.y))
                self.screen.blit(scaled_image, fruit_rect)

        score_text = self.score_font.render(f"Score: {self.score}", True, SCORE_COLOR)
        score_shadow = self.score_font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_shadow, (12, 12))
        self.screen.blit(score_text, (10, 10))

        high_score_text = self.score_font.render(
            f"High Score: {self.high_score}", True, SCORE_COLOR
        )
        high_score_shadow = self.score_font.render(
            f"High Score: {self.high_score}", True, BLACK
        )
        self.screen.blit(high_score_shadow, (12, 52))
        self.screen.blit(high_score_text, (10, 50))

    def run(self):
        self.fruit_spawner_thread = threading.Thread(target=self.spawn_fruit)
        self.fruit_spawner_thread.daemon = True
        self.fruit_spawner_thread.start()

        def save_high_score(signum, frame):
            if self.score > self.high_score:
                with open("high_score.json", "w") as f:
                    json.dump({"high_score": self.score}, f)
            self.game_over = True
            self.sound_manager.cleanup()
            sys.exit(0)

        signal.signal(signal.SIGINT, save_high_score)

        mouse_down = False
        start_pos = None

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_high_score(None, None)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down = True
                    start_pos = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONUP and mouse_down:
                    mouse_down = False
                    end_pos = pygame.mouse.get_pos()
                    self.handle_slice(start_pos, end_pos)

            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
