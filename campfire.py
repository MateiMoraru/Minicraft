import random
import pygame
from window import Window
from spritesheet import *
from rect import Rect
from typing import Tuple
from animation import Animation
from particles import Particles

class Campfire:
    def __init__(self, window: Window, spritesheet: Spritesheet, pos: Tuple[int, int], size: Tuple[int, int]):
        self.window = window
        self.spritesheet = spritesheet
        self.campfire = Rect(pos, size, (0, 0, 0), "CAMPFIRE", self.window.get(), spritesheet.image(CAMPFIRE_1, size=size))
        self.animation = Animation(self.window, self.spritesheet, 4, CAMPFIRE_1, 0.1, size)
        self.animation.start()
        self.particles = Particles(self.window, self.spritesheet, pos, 5, -0.1, 0.5)
        self.particles.no_gravity()

    
    def draw(self, offset: Tuple[int, int]=(0, 0)):
        self.campfire.draw(offset=offset)
        self.particles.draw(offset=offset)
        self.particles.loop()
        self.campfire.set_texture(self.animation.get)
        if random.random() > 0.95:
            self.particles.add_particles((self.campfire.center[0], self.campfire.center[1] - self.campfire.size[1] / 4), FIRE_TEXTURE)#random.randint(CAMPFIRE_4, SMOKE))