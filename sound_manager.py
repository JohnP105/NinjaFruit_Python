import pygame
import os
from typing import Dict
from constants import SOUND_VOLUMES


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.load_sounds()

    def load_sounds(self):
        try:
            # Load sound effects
            self.sounds["slice"] = pygame.mixer.Sound(
                os.path.join("sounds", "slice.wav")
            )
            self.sounds["bomb"] = pygame.mixer.Sound(os.path.join("sounds", "bomb.wav"))
            self.sounds["background"] = pygame.mixer.Sound(
                os.path.join("sounds", "background.wav")
            )

            # Set volume levels
            for sound_name, volume in SOUND_VOLUMES.items():
                self.sounds[sound_name].set_volume(volume)

            # Start background music
            self.sounds["background"].play(-1)  # -1 means loop indefinitely
        except pygame.error as e:
            print(f"Warning: Could not load sounds: {e}")

    def play_sound(self, sound_name: str):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def stop_background_music(self):
        if "background" in self.sounds:
            self.sounds["background"].stop()

    def cleanup(self):
        pygame.mixer.quit()
