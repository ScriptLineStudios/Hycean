import pygame.mixer
import os
from json import load

pygame.mixer.init()


class AudioHandler:
    sounds = {}
    with open('src/sfx/sounds.json') as file:
        data = load(file)
        for path in data:
            print(path)
            sounds[path] = pygame.mixer.Sound(f'src/sfx/{data[path]}')

    @classmethod
    def set_volume(cls, volume):
        for sound in cls.sounds:
            cls.sounds[sound].set_volume(volume)