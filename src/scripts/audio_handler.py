import pygame.mixer
import os
from json import load

pygame.mixer.init()


class AudioHandler:
    sounds = {}
    with open('src/assets/sound/sounds.json') as file:
        data = load(file)
        for path in data:
            sounds[path] = pygame.mixer.Sound(f'src/assets/sound/{data[path]}')

    @classmethod
    def set_volume(cls, volume):
        for sound in cls.sounds:
            cls.sounds[sound].set_volume(volume)