import random
import time
import pygame
from window import Window
from spritesheet import *
from rect import Rect
from typing import Tuple
from animation import Animation
from particles import Particles

class Campfire:
    def __init__(self, window: Window, spritesheet: Spritesheet, pos: Tuple[int, int], size: Tuple[int, int], underground: bool=False):
        self.window = window
        self.spritesheet = spritesheet
        self.campfire = Rect(pos, size, (0, 0, 0), "CAMPFIRE", self.window.get(), spritesheet.image(CAMPFIRE_1, size=size), underground=underground)
        self.animation = Animation(self.window, self.spritesheet, 4, CAMPFIRE_1, 0.1, size)
        self.animation.start()
        self.particles = Particles(self.window, self.spritesheet, pos, 5, -0.1, 0.5, underground=underground)
        self.particles.no_gravity()

        self.cooking = []
        self.cooked = []

    
    def draw(self, offset: Tuple[int, int]=(0, 0), underground: bool=False):
        self.campfire.draw(offset=offset, underground=underground)
        self.particles.draw(offset=offset, underground=underground)
        self.particles.loop()
        self.campfire.set_texture(self.animation.get)
        if random.random() > 0.95:
            self.particles.add_particles((self.campfire.center[0], self.campfire.center[1] - self.campfire.size[1] / 4), FIRE_TEXTURE)#random.randint(CAMPFIRE_4, SMOKE))

        for item in self.cooking:
            if time.time() - item[1] > 3:
                self.cooked.append(item)
                self.cooking.remove(item)

    def add_to_fire(self, item: int):
        self.cooking.append([item, time.time()])